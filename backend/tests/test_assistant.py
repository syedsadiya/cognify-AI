from types import SimpleNamespace
from app.api import assistant


def test_chat_requires_provider_key(client, monkeypatch):
    monkeypatch.setattr(assistant.settings, "openai_api_key", "")
    monkeypatch.setattr(assistant.settings, "xai_api_key", "")

    response = client.post("/api/assistant/chat", json={"message": "Hello"})

    assert response.status_code == 503
    assert "XAI_API_KEY" in response.json()["detail"]


def test_chat_uses_grok_and_returns_answer(client, monkeypatch):
    class FakeCompletions:
        def create(self, **kwargs):
            assert kwargs["model"] == "grok-4.7"
            assert kwargs["messages"][-1] == {"role": "user", "content": "Hello"}
            return SimpleNamespace(
                choices=[SimpleNamespace(message=SimpleNamespace(content="Hi there!"))]
            )

    class FakeOpenAI:
        def __init__(self, api_key, base_url):
            assert api_key == "test-xai-key"
            assert base_url == "https://api.x.ai/v1"
            self.chat = SimpleNamespace(completions=FakeCompletions())

    monkeypatch.setattr(assistant.settings, "xai_api_key", "test-xai-key")
    monkeypatch.setattr(assistant.settings, "xai_model", "grok-4.7")
    monkeypatch.setattr(assistant.settings, "xai_base_url", "https://api.x.ai/v1")
    monkeypatch.setattr(assistant, "OpenAI", FakeOpenAI)

    response = client.post("/api/assistant/chat", json={"message": "Hello"})

    assert response.status_code == 200
    assert response.json() == {"answer": "Hi there!"}


def test_chat_falls_back_to_openai(client, monkeypatch):
    class FakeCompletions:
        def create(self, **kwargs):
            assert kwargs["model"] == "gpt-test"
            return SimpleNamespace(
                choices=[SimpleNamespace(message=SimpleNamespace(content="OpenAI answer"))]
            )

    class FakeOpenAI:
        def __init__(self, api_key, **kwargs):
            assert api_key == "test-openai-key"
            assert kwargs == {}
            self.chat = SimpleNamespace(completions=FakeCompletions())

    monkeypatch.setattr(assistant.settings, "xai_api_key", "")
    monkeypatch.setattr(assistant.settings, "openai_api_key", "test-openai-key")
    monkeypatch.setattr(assistant.settings, "openai_model", "gpt-test")
    monkeypatch.setattr(assistant, "OpenAI", FakeOpenAI)

    response = client.post("/api/assistant/chat", json={"message": "Hello"})

    assert response.status_code == 200
    assert response.json() == {"answer": "OpenAI answer"}


def test_chat_includes_selected_dataset_profile(client, monkeypatch, session_factory, tmp_path):
    from app.db.models import Dataset
    from app.services import dataset_service

    dataset = Dataset(
        original_name="sales.csv",
        stored_name="sales.csv",
        file_type="csv",
        size_bytes=1,
        row_count=1,
        column_count=1,
    )
    db = session_factory()
    db.add(dataset)
    db.commit()
    db.refresh(dataset)

    csv_path = tmp_path / "sales.csv"
    csv_path.write_text("revenue\n42\n")
    monkeypatch.setattr(dataset_service, "dataset_path", lambda _: csv_path)

    class FakeCompletions:
        def create(self, **kwargs):
            assert "sales.csv" in kwargs["messages"][0]["content"]
            assert '"rows": 1' in kwargs["messages"][0]["content"]
            return SimpleNamespace(
                choices=[SimpleNamespace(message=SimpleNamespace(content="One row."))]
            )

    class FakeOpenAI:
        def __init__(self, api_key, base_url):
            self.chat = SimpleNamespace(completions=FakeCompletions())

    monkeypatch.setattr(assistant.settings, "xai_api_key", "test-xai-key")
    monkeypatch.setattr(assistant.settings, "xai_base_url", "https://api.x.ai/v1")
    monkeypatch.setattr(assistant, "OpenAI", FakeOpenAI)

    response = client.post(
        "/api/assistant/chat",
        json={"message": "How many rows?", "dataset_id": dataset.id},
    )
    db.close()

    assert response.status_code == 200
    assert response.json() == {"answer": "One row."}
