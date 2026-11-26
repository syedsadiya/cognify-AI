from types import SimpleNamespace
from app.api import assistant


def test_chat_requires_openai_key(client, monkeypatch):
    monkeypatch.setattr(assistant.settings, "openai_api_key", "")

    response = client.post("/api/assistant/chat", json={"message": "Hello"})

    assert response.status_code == 503
    assert "OPENAI_API_KEY" in response.json()["detail"]


def test_chat_returns_ai_answer(client, monkeypatch):
    class FakeCompletions:
        def create(self, **kwargs):
            assert kwargs["messages"][-1] == {"role": "user", "content": "Hello"}
            return SimpleNamespace(
                choices=[SimpleNamespace(message=SimpleNamespace(content="Hi there!"))]
            )

    class FakeOpenAI:
        def __init__(self, api_key):
            assert api_key == "test-key"
            self.chat = SimpleNamespace(completions=FakeCompletions())

    monkeypatch.setattr(assistant.settings, "openai_api_key", "test-key")
    monkeypatch.setattr(assistant, "OpenAI", FakeOpenAI)

    response = client.post("/api/assistant/chat", json={"message": "Hello"})

    assert response.status_code == 200
    assert response.json() == {"answer": "Hi there!"}


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
        def __init__(self, api_key):
            self.chat = SimpleNamespace(completions=FakeCompletions())

    monkeypatch.setattr(assistant.settings, "openai_api_key", "test-key")
    monkeypatch.setattr(assistant, "OpenAI", FakeOpenAI)

    response = client.post(
        "/api/assistant/chat",
        json={"message": "How many rows?", "dataset_id": dataset.id},
    )
    db.close()

    assert response.status_code == 200
    assert response.json() == {"answer": "One row."}
