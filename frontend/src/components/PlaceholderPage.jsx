import PageHeader from "./PageHeader";
import Card from "./Card";

export default function PlaceholderPage({ title, description, phase }) {
  return (
    <div>
      <PageHeader title={title} subtitle={description} />
      <Card>
        <p className="text-taupe">This page will be built in {phase}.</p>
      </Card>
    </div>
  );
}
