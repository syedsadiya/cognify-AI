import { useEffect, useState } from "react";
import { Menu } from "lucide-react";
import { getHealth } from "../services/api";

export default function Topbar({ onMenu }) {
  const [online, setOnline] = useState(null);

  useEffect(() => {
    getHealth()
      .then(() => setOnline(true))
      .catch(() => setOnline(false));
  }, []);

  let label = "Checking API...";
  let dot = "bg-taupe";
  if (online === true) {
    label = "API online";
    dot = "bg-coffee";
  } else if (online === false) {
    label = "API offline";
    dot = "bg-beige";
  }

  return (
    <header className="sticky top-0 z-20 flex items-center justify-between bg-offwhite/90 backdrop-blur border-b border-beige/60 px-4 md:px-8 py-3">
      <button className="md:hidden" onClick={onMenu} aria-label="Open menu">
        <Menu size={22} />
      </button>
      <p className="hidden md:block text-sm text-taupe">AI-powered multi-engine analytics</p>
      <div className="flex items-center gap-2 text-sm">
        <span className={"inline-block w-2.5 h-2.5 rounded-full " + dot} />
        <span>{label}</span>
      </div>
    </header>
  );
}
