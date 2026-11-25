import { useEffect, useState } from "react";
import PageHeader from "../components/PageHeader";
import Card from "../components/Card";
import { getSettings, saveSetting } from "../services/api";

const FIELDS = [
  { key: "default_engine", label: "Default engine", options: ["auto", "pandas", "polars", "duckdb", "fireducks"] },
  { key: "repetitions", label: "Benchmark repetitions", options: ["3", "5", "10"] },
  { key: "warmup_runs", label: "Warm-up runs", options: ["1", "2", "3"] },
];

export default function Settings() {
  const [values, setValues] = useState(null);
  const [message, setMessage] = useState("");

  useEffect(() => {
    getSettings().then(setValues).catch((e) => setMessage(e.message));
  }, []);

  function change(key, value) {
    setValues({ ...values, [key]: value });
  }

  async function save() {
    try {
      for (const field of FIELDS) {
        await saveSetting(field.key, values[field.key]);
      }
      setMessage("Settings saved.");
    } catch (e) {
      setMessage(e.message);
    }
  }

  return (
    <div>
      <PageHeader title="Settings" subtitle="Defaults used for processing and benchmarks." />
      <Card className="max-w-xl">
        {!values && <p className="text-taupe">{message || "Loading..."}</p>}
        {values && (
          <div className="space-y-4">
            {FIELDS.map((field) => (
              <label key={field.key} className="block">
                <span className="text-sm text-taupe">{field.label}</span>
                <select
                  value={values[field.key]}
                  onChange={(e) => change(field.key, e.target.value)}
                  className="mt-1 w-full rounded-lg border border-beige bg-offwhite px-3 py-2"
                >
                  {field.options.map((opt) => (
                    <option key={opt} value={opt}>{opt}</option>
                  ))}
                </select>
              </label>
            ))}
            <button onClick={save} className="bg-coffee text-offwhite rounded-lg px-5 py-2 hover:bg-espresso">
              Save settings
            </button>
            {message && <p className="text-sm text-taupe">{message}</p>}
          </div>
        )}
      </Card>
    </div>
  );
}
