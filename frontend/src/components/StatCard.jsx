export default function StatCard({ label, value }) {
  return (
    <div className="bg-sand rounded-2xl shadow-card p-5">
      <p className="text-sm text-taupe">{label}</p>
      <p className="text-3xl font-bold mt-1">{value}</p>
    </div>
  );
}
