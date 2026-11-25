import { useEffect, useState } from "react";
import { Link, useSearchParams } from "react-router-dom";
import { Download, Trash2 } from "lucide-react";
import PageHeader from "../components/PageHeader";
import Card from "../components/Card";
import StatCard from "../components/StatCard";
import DataTable from "../components/DataTable";
import { listDatasets, getPreview, getProfile, deleteDataset, downloadUrl } from "../services/api";

const STAT_NAMES = ["count", "mean", "std", "min", "25%", "50%", "75%", "max"];

function round(value) {
  if (value === null || value === undefined) return null;
  return Math.round(value * 100) / 100;
}

export default function DatasetExplorer() {
  const [params, setParams] = useSearchParams();
  const [datasets, setDatasets] = useState(null);
  const [preview, setPreview] = useState(null);
  const [profile, setProfile] = useState(null);
  const [error, setError] = useState("");

  const selectedId = params.get("id") || (datasets && datasets.length > 0 ? String(datasets[0].id) : "");

  function loadList() {
    listDatasets().then(setDatasets).catch((e) => setError(e.message));
  }

  useEffect(loadList, []);

  useEffect(() => {
    if (!selectedId) return;
    setPreview(null);
    setProfile(null);
    setError("");
    getPreview(selectedId).then(setPreview).catch((e) => setError(e.message));
    getProfile(selectedId).then(setProfile).catch((e) => setError(e.message));
  }, [selectedId]);

  async function remove() {
    if (!window.confirm("Delete this dataset? This cannot be undone.")) return;
    try {
      await deleteDataset(selectedId);
      setParams({});
      setPreview(null);
      setProfile(null);
      loadList();
    } catch (e) {
      setError(e.message);
    }
  }

  if (datasets && datasets.length === 0) {
    return (
      <div>
        <PageHeader title="Dataset Explorer" subtitle="Preview, profile and inspect your data." />
        <Card>
          <p className="text-taupe">No datasets yet.</p>
          <Link to="/app/upload" className="text-coffee font-medium">Upload your first dataset</Link>
        </Card>
      </div>
    );
  }

  const statRows = [];
  if (profile) {
    for (const col of Object.keys(profile.statistics)) {
      const row = [col];
      for (const stat of STAT_NAMES) row.push(round(profile.statistics[col][stat]));
      statRows.push(row);
    }
  }

  return (
    <div>
      <PageHeader title="Dataset Explorer" subtitle="Preview, profile and inspect your data." />

      {error && <p className="text-coffee mb-4">{error}</p>}
      {!datasets && !error && <p className="text-taupe">Loading...</p>}

      {datasets && datasets.length > 0 && (
        <div className="flex flex-wrap items-center gap-3 mb-4">
          <select
            value={selectedId}
            onChange={(e) => setParams({ id: e.target.value })}
            className="rounded-lg border border-beige bg-offwhite px-3 py-2"
          >
            {datasets.map((d) => (
              <option key={d.id} value={d.id}>{d.original_name}</option>
            ))}
          </select>
          <a
            href={downloadUrl(selectedId)}
            className="flex items-center gap-2 bg-coffee text-offwhite rounded-lg px-4 py-2 hover:bg-espresso"
          >
            <Download size={16} /> Download
          </a>
          <button
            onClick={remove}
            className="flex items-center gap-2 border border-coffee text-coffee rounded-lg px-4 py-2 hover:bg-sand"
          >
            <Trash2 size={16} /> Delete
          </button>
        </div>
      )}

      {profile && (
        <>
          <div className="grid gap-4 grid-cols-2 lg:grid-cols-4">
            <StatCard label="Rows" value={profile.rows.toLocaleString()} />
            <StatCard label="Columns" value={profile.columns_count} />
            <StatCard label="Missing values" value={profile.total_missing.toLocaleString()} />
            <StatCard label="Duplicate rows" value={profile.duplicate_rows.toLocaleString()} />
          </div>

          <Card title="Columns" className="mt-4">
            <DataTable
              columns={["Column", "Type", "Missing", "Missing %", "Unique"]}
              rows={profile.columns.map((c) => [c.name, c.dtype, c.missing, c.missing_pct + "%", c.unique])}
            />
          </Card>
        </>
      )}

      {preview && (
        <Card title={"Preview (first " + preview.rows.length + " of " + preview.total_rows.toLocaleString() + " rows)"} className="mt-4">
          <DataTable columns={preview.columns} rows={preview.rows} />
        </Card>
      )}

      {profile && statRows.length > 0 && (
        <Card title="Statistical summary" className="mt-4">
          <DataTable columns={["Column", ...STAT_NAMES]} rows={statRows} />
        </Card>
      )}
    </div>
  );
}
