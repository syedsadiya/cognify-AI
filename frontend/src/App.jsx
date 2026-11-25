import { Routes, Route, Navigate } from "react-router-dom";
import Layout from "./components/Layout";
import Landing from "./pages/Landing";
import Dashboard from "./pages/Dashboard";
import DatasetUpload from "./pages/DatasetUpload";
import DatasetExplorer from "./pages/DatasetExplorer";
import AIAssistant from "./pages/AIAssistant";
import ProcessingWorkspace from "./pages/ProcessingWorkspace";
import BenchmarkComparison from "./pages/BenchmarkComparison";
import EngineRecommendation from "./pages/EngineRecommendation";
import BenchmarkHistory from "./pages/BenchmarkHistory";
import Reports from "./pages/Reports";
import Settings from "./pages/Settings";

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<Landing />} />
      <Route path="/app" element={<Layout />}>
        <Route index element={<Navigate to="dashboard" replace />} />
        <Route path="dashboard" element={<Dashboard />} />
        <Route path="upload" element={<DatasetUpload />} />
        <Route path="explorer" element={<DatasetExplorer />} />
        <Route path="assistant" element={<AIAssistant />} />
        <Route path="workspace" element={<ProcessingWorkspace />} />
        <Route path="benchmark" element={<BenchmarkComparison />} />
        <Route path="recommendation" element={<EngineRecommendation />} />
        <Route path="history" element={<BenchmarkHistory />} />
        <Route path="reports" element={<Reports />} />
        <Route path="settings" element={<Settings />} />
      </Route>
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  );
}
