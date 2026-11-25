import { Link } from "react-router-dom";
import { Coffee, Database, Bot, Gauge, Trophy } from "lucide-react";

const FEATURES = [
  { icon: Database, title: "Four engines", text: "Pandas, Polars, DuckDB and FireDucks behind one interface." },
  { icon: Gauge, title: "Fair benchmarks", text: "Warm-ups, repetitions, medians and validated outputs." },
  { icon: Bot, title: "AI assistant", text: "Ask questions in plain English and confirm the plan first." },
  { icon: Trophy, title: "Smart recommendations", text: "Engine suggestions based on measured results only." },
];

export default function Landing() {
  return (
    <div className="min-h-screen">
      <header className="flex items-center justify-between px-6 md:px-12 py-5">
        <div className="flex items-center gap-2 text-xl font-bold">
          <Coffee className="text-coffee" /> CremaBench
        </div>
        <Link to="/app/dashboard" className="text-coffee font-medium">Open app</Link>
      </header>

      <section className="text-center px-6 py-16 md:py-24 max-w-3xl mx-auto">
        <h1 className="text-4xl md:text-5xl font-bold">Intelligent Data. Smarter Performance.</h1>
        <p className="text-taupe mt-4 text-lg">
          Upload a dataset, compare four processing engines on your own workload,
          and find out which one really fits.
        </p>
        <Link
          to="/app/dashboard"
          className="inline-block mt-8 bg-coffee text-offwhite rounded-lg px-6 py-3 font-medium hover:bg-espresso"
        >
          Get Started
        </Link>
      </section>

      <section className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4 px-6 md:px-12 pb-16 max-w-6xl mx-auto">
        {FEATURES.map((f) => {
          const Icon = f.icon;
          return (
            <div key={f.title} className="bg-sand rounded-2xl shadow-card p-5">
              <Icon className="text-coffee mb-3" />
              <h3 className="font-semibold">{f.title}</h3>
              <p className="text-sm text-taupe mt-1">{f.text}</p>
            </div>
          );
        })}
      </section>
    </div>
  );
}
