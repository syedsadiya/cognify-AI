import { useEffect, useState } from "react";
import { getHealth } from "./services/api";

export default function App() {
  const [health, setHealth] = useState(null);
  const [error, setError] = useState("");

  useEffect(() => {
    getHealth().then(setHealth).catch((e) => setError(e.message));
  }, []);

  return (
    <main className="min-h-screen flex items-center justify-center p-6">
      <div className="bg-sand rounded-2xl shadow-card p-8 w-full max-w-xl">
        <h1 className="text-3xl font-bold">CremaBench</h1>
        <p className="text-taupe mt-1">Intelligent Data. Smarter Performance.</p>

        <h2 className="mt-6 font-semibold">Backend status</h2>
        {error && <p className="text-coffee mt-2">{error}</p>}
        {!health && !error && <p className="text-taupe mt-2">Checking...</p>}
        {health && (
          <ul className="mt-3 space-y-2">
            {health.engines.map((e) => (
              <li key={e.name} className="flex justify-between bg-offwhite rounded-lg px-4 py-2">
                <span className="capitalize">{e.name}</span>
                <span className={e.available ? "text-coffee font-medium" : "text-taupe"}>
                  {e.available ? `v${e.version}` : "not installed"}
                </span>
              </li>
            ))}
          </ul>
        )}
        <button className="mt-6 bg-coffee text-offwhite rounded-lg px-5 py-2">
          Get Started
        </button>
      </div>
    </main>
  );
}
