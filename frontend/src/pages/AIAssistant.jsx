import { useEffect, useState } from "react";
import { Bot, LoaderCircle, RotateCcw, Send, Sparkles, User } from "lucide-react";
import PageHeader from "../components/PageHeader";
import Card from "../components/Card";
import { listDatasets, sendAssistantChat } from "../services/api";

const WELCOME = {
  role: "assistant",
  content: "Hi! I’m your CremaBench data assistant. Ask me about your dataset, data quality, or how to get started with an analysis.",
};
const SUGGESTIONS = [
  "What can you tell me about my dataset?",
  "How should I handle missing values?",
  "Which engine should I use for analysis?",
];

export default function AIAssistant() {
  const [datasets, setDatasets] = useState([]);
  const [datasetError, setDatasetError] = useState("");
  const [datasetId, setDatasetId] = useState("");
  const [messages, setMessages] = useState([WELCOME]);
  const [draft, setDraft] = useState("");
  const [error, setError] = useState("");
  const [sending, setSending] = useState(false);

  useEffect(() => {
    listDatasets()
      .then(setDatasets)
      .catch((requestError) => setDatasetError(requestError.message));
  }, []);

  async function submit(event) {
    event.preventDefault();
    const question = draft.trim();
    if (!question || sending) return;

    const previousMessages = messages;
    setMessages([...previousMessages, { role: "user", content: question }]);
    setDraft("");
    setError("");
    setSending(true);

    try {
      const response = await sendAssistantChat(
        question,
        previousMessages.slice(1),
        datasetId ? Number(datasetId) : null,
      );
      setMessages((current) => [...current, { role: "assistant", content: response.answer }]);
    } catch (requestError) {
      setMessages(previousMessages);
      setDraft(question);
      setError(requestError.message);
    } finally {
      setSending(false);
    }
  }

  function resetChat() {
    setMessages([WELCOME]);
    setDraft("");
    setError("");
  }

  return (
    <div>
      <PageHeader
        title="AI Data Assistant"
        subtitle="Ask questions about your data and get help planning your analysis."
      />

      <Card className="max-w-4xl">
        <div className="flex flex-wrap items-center justify-between gap-3 border-b border-beige pb-4">
          <div>
            <h2 className="font-semibold">Chat with CremaBench AI</h2>
            <p className="text-sm text-taupe mt-1">
              Choose a dataset to include its profile in your question.
            </p>
          </div>
          <div className="flex items-center gap-2">
            <select
              value={datasetId}
              onChange={(event) => setDatasetId(event.target.value)}
              className="max-w-56 rounded-lg border border-beige bg-offwhite px-3 py-2 text-sm"
              aria-label="Dataset for chat context"
            >
              <option value="">Chat without a dataset</option>
              {datasets.map((dataset) => (
                <option key={dataset.id} value={dataset.id}>{dataset.original_name}</option>
              ))}
            </select>
            <button
              type="button"
              onClick={resetChat}
              className="rounded-lg border border-beige p-2 text-taupe hover:bg-sand"
              aria-label="Start a new chat"
              title="Start a new chat"
            >
              <RotateCcw size={17} />
            </button>
          </div>
        </div>

        {datasetError && (
          <p role="alert" className="mt-3 text-sm text-coffee">
            Could not load datasets: {datasetError}
          </p>
        )}

        <div className="my-4 min-h-72 max-h-[55vh] space-y-4 overflow-y-auto rounded-lg bg-sand/50 p-4">
          {messages.map((message, index) => {
            const isAssistant = message.role === "assistant";
            const Icon = isAssistant ? Bot : User;
            return (
              <div
                key={index}
                className={"flex items-start gap-3 " + (isAssistant ? "" : "flex-row-reverse")}
              >
                <span className="mt-1 rounded-full bg-offwhite p-2 text-coffee">
                  <Icon size={16} />
                </span>
                <p
                  className={
                    "max-w-[85%] rounded-xl px-4 py-3 text-sm leading-6 whitespace-pre-wrap " +
                    (isAssistant ? "bg-white text-espresso" : "bg-coffee text-white")
                  }
                >
                  {message.content}
                </p>
              </div>
            );
          })}
          {sending && (
            <div className="flex items-center gap-2 text-sm text-taupe" role="status">
              <LoaderCircle size={16} className="animate-spin" /> Thinking…
            </div>
          )}
        </div>

        {error && (
          <p role="alert" className="mb-3 rounded-lg bg-red-50 px-3 py-2 text-sm text-red-800">
            {error}
          </p>
        )}

        {messages.length === 1 && (
          <div className="mb-3 flex flex-wrap gap-2">
            {SUGGESTIONS.map((suggestion) => (
              <button
                type="button"
                key={suggestion}
                onClick={() => setDraft(suggestion)}
                className="flex items-center gap-1 rounded-full border border-beige px-3 py-1.5 text-xs text-taupe hover:bg-sand"
              >
                <Sparkles size={13} /> {suggestion}
              </button>
            ))}
          </div>
        )}

        <form onSubmit={submit} className="flex items-end gap-2">
          <textarea
            value={draft}
            onChange={(event) => setDraft(event.target.value)}
            onKeyDown={(event) => {
              if (event.key === "Enter" && !event.shiftKey) {
                event.preventDefault();
                event.currentTarget.form.requestSubmit();
              }
            }}
            placeholder="Ask a question… (Enter to send, Shift+Enter for a new line)"
            rows={2}
            maxLength={2000}
            className="min-h-12 flex-1 resize-y rounded-lg border border-beige bg-white px-3 py-2 text-sm outline-none focus:border-coffee"
            aria-label="Message"
          />
          <button
            type="submit"
            disabled={sending || !draft.trim()}
            className="flex items-center gap-2 rounded-lg bg-coffee px-4 py-3 text-sm font-medium text-white hover:bg-espresso disabled:cursor-not-allowed disabled:opacity-50"
          >
            <Send size={16} /> Send
          </button>
        </form>
        <p className="mt-2 text-xs text-taupe">
          Dataset profile details are sent to the configured AI provider when a dataset is selected.
        </p>
      </Card>
    </div>
  );
}
