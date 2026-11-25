import { useEffect, useState } from "react";
import PageHeader from "../components/PageHeader";
import StatCard from "../components/StatCard";
import Card from "../components/Card";
import { getDashboardSummary } from "../services/api";

export default function Dashboard() {
  const [data, setData] = useState(null);
  const [error, setError] = useState("");

  useEffect(() => {
    getDashboardSummary().then(setData).catch((e) => setError(e.message));
  }, []);

  return (
    <div>
      <PageHeader title="Dashboard" subtitle="Overview of your datasets and benchmark activity." />

      {error && <p className="text-coffee mb-4">Could not load data: {error}</p>}
      {!data && !error && <p className="text-taupe">Loading...</p>}

      {data && (
        <>
          <div className="grid gap-4 sm:grid-cols-3">
            <StatCard label="Datasets processed" value={data.total_datasets} />
            <StatCard label="Benchmark runs" value={data.total_benchmark_runs} />
            <StatCard label="Available engines" value={data.available_engines.length} />
          </div>

          <div className="grid gap-4 lg:grid-cols-2 mt-4">
            <Card title="Engines">
              <ul className="flex flex-wrap gap-2">
                {data.available_engines.map((name) => (
                  <li key={name} className="bg-offwhite rounded-full px-3 py-1 text-sm capitalize">
                    {name}
                  </li>
                ))}
              </ul>
            </Card>

            <Card title="Recent benchmark runs">
              {data.recent_runs.length === 0 ? (
                <p className="text-taupe text-sm">No benchmark runs yet.</p>
              ) : (
                <ul className="space-y-2 text-sm">
                  {data.recent_runs.map((run) => (
                    <li key={run.id} className="flex justify-between bg-offwhite rounded-lg px-3 py-2">
                      <span>{run.operation}</span>
                      <span className="text-taupe">{run.status}</span>
                    </li>
                  ))}
                </ul>
              )}
            </Card>
          </div>
        </>
      )}
    </div>
  );
}
