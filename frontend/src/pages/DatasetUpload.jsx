import { useRef, useState } from "react";
import { Link } from "react-router-dom";
import { UploadCloud } from "lucide-react";
import PageHeader from "../components/PageHeader";
import Card from "../components/Card";
import { uploadDataset } from "../services/api";

const ALLOWED = [".csv", ".xlsx", ".parquet"];
const MAX_MB = 200;

export default function DatasetUpload() {
  const inputRef = useRef(null);
  const [file, setFile] = useState(null);
  const [progress, setProgress] = useState(0);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  const [result, setResult] = useState(null);
  const [dragging, setDragging] = useState(false);

  function pick(f) {
    setResult(null);
    setError("");
    setProgress(0);
    setFile(null);
    if (!f) return;

    const name = f.name.toLowerCase();
    let ok = false;
    for (const ext of ALLOWED) {
      if (name.endsWith(ext)) ok = true;
    }
    if (!ok) {
      setError("Unsupported file type. Please choose a CSV, XLSX or Parquet file.");
      return;
    }
    if (f.size > MAX_MB * 1024 * 1024) {
      setError("File is too large. Maximum size is " + MAX_MB + " MB.");
      return;
    }
    setFile(f);
  }

  async function upload() {
    setBusy(true);
    setError("");
    setProgress(0);
    try {
      const data = await uploadDataset(file, setProgress);
      setResult(data);
      setFile(null);
    } catch (e) {
      setError(e.message);
    } finally {
      setBusy(false);
    }
  }

  function onDrop(e) {
    e.preventDefault();
    setDragging(false);
    pick(e.dataTransfer.files[0]);
  }

  return (
    <div>
      <PageHeader title="Dataset Upload" subtitle="Upload a CSV, Excel (.xlsx) or Parquet file." />

      <Card className="max-w-2xl">
        <div
          onDragOver={(e) => { e.preventDefault(); setDragging(true); }}
          onDragLeave={() => setDragging(false)}
          onDrop={onDrop}
          onClick={() => inputRef.current.click()}
          className={
            "cursor-pointer rounded-xl border-2 border-dashed p-10 text-center " +
            (dragging ? "border-coffee bg-beige/40" : "border-beige bg-offwhite")
          }
        >
          <UploadCloud className="mx-auto text-coffee mb-2" size={36} />
          <p className="font-medium">Drag a file here or click to browse</p>
          <p className="text-sm text-taupe mt-1">CSV, XLSX or Parquet, up to {MAX_MB} MB</p>
          <input
            ref={inputRef}
            type="file"
            accept=".csv,.xlsx,.parquet"
            className="hidden"
            onChange={(e) => pick(e.target.files[0])}
          />
        </div>

        {file && (
          <div className="mt-4 flex items-center justify-between gap-3">
            <p className="text-sm truncate">
              {file.name} <span className="text-taupe">({(file.size / 1024 / 1024).toFixed(2)} MB)</span>
            </p>
            <button
              onClick={upload}
              disabled={busy}
              className="bg-coffee text-offwhite rounded-lg px-5 py-2 hover:bg-espresso disabled:opacity-50"
            >
              {busy ? "Uploading..." : "Upload"}
            </button>
          </div>
        )}

        {busy && (
          <div className="mt-4">
            <div className="h-2 bg-offwhite rounded-full overflow-hidden">
              <div className="h-full bg-coffee transition-all" style={{ width: progress + "%" }} />
            </div>
            <p className="text-xs text-taupe mt-1">
              {progress < 100 ? "Uploading " + progress + "%" : "Validating and profiling..."}
            </p>
          </div>
        )}

        {error && <p className="mt-4 text-coffee font-medium">{error}</p>}

        {result && (
          <div className="mt-4 bg-offwhite rounded-lg p-4">
            <p className="font-medium">Uploaded {result.original_name}</p>
            <p className="text-sm text-taupe">
              {result.row_count.toLocaleString()} rows, {result.column_count} columns
            </p>
            <Link to={"/app/explorer?id=" + result.id} className="inline-block mt-2 text-coffee font-medium">
              Open in Dataset Explorer
            </Link>
          </div>
        )}
      </Card>
    </div>
  );
}
