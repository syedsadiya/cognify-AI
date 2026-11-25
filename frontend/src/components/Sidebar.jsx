import { NavLink, Link } from "react-router-dom";
import {
  LayoutDashboard, Upload, Table2, Bot, Cpu, BarChart3,
  Trophy, History, FileText, Settings as SettingsIcon, Coffee, X,
} from "lucide-react";

const ITEMS = [
  { to: "/app/dashboard", label: "Dashboard", icon: LayoutDashboard },
  { to: "/app/upload", label: "Dataset Upload", icon: Upload },
  { to: "/app/explorer", label: "Dataset Explorer", icon: Table2 },
  { to: "/app/assistant", label: "AI Data Assistant", icon: Bot },
  { to: "/app/workspace", label: "Processing Workspace", icon: Cpu },
  { to: "/app/benchmark", label: "Benchmark Comparison", icon: BarChart3 },
  { to: "/app/recommendation", label: "Engine Recommendation", icon: Trophy },
  { to: "/app/history", label: "Benchmark History", icon: History },
  { to: "/app/reports", label: "Reports and Exports", icon: FileText },
  { to: "/app/settings", label: "Settings", icon: SettingsIcon },
];

export default function Sidebar({ open, onClose }) {
  return (
    <>
      {open && (
        <div className="fixed inset-0 bg-espresso/50 z-30 md:hidden" onClick={onClose} />
      )}
      <aside
        className={
          "fixed inset-y-0 left-0 w-64 bg-espresso text-offwhite z-40 flex flex-col transition-transform " +
          (open ? "translate-x-0" : "-translate-x-full md:translate-x-0")
        }
      >
        <div className="flex items-center justify-between px-5 py-5">
          <Link to="/" className="flex items-center gap-2 text-lg font-bold">
            <Coffee size={22} className="text-beige" />
            CremaBench
          </Link>
          <button className="md:hidden" onClick={onClose} aria-label="Close menu">
            <X size={20} />
          </button>
        </div>

        <nav className="flex-1 overflow-y-auto px-3 pb-4 space-y-1">
          {ITEMS.map((item) => {
            const Icon = item.icon;
            return (
              <NavLink
                key={item.to}
                to={item.to}
                onClick={onClose}
                className={({ isActive }) =>
                  "flex items-center gap-3 rounded-lg px-3 py-2 text-sm transition-colors " +
                  (isActive ? "bg-coffee text-offwhite" : "text-beige hover:bg-coffee/50")
                }
              >
                <Icon size={18} />
                {item.label}
              </NavLink>
            );
          })}
        </nav>

        <p className="px-5 py-4 text-xs text-taupe">Intelligent Data. Smarter Performance.</p>
      </aside>
    </>
  );
}
