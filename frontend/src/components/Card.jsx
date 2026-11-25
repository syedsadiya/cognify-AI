export default function Card({ title, children, className = "" }) {
  return (
    <section className={"bg-sand rounded-2xl shadow-card p-5 " + className}>
      {title && <h2 className="font-semibold mb-3">{title}</h2>}
      {children}
    </section>
  );
}
