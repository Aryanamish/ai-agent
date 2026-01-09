import { Button } from "@/components/ui/button";
import {StoreNameSignal, ThemeSignal} from "@/signals";
import { Sun,Moon } from "lucide-react"

const MenuIcon = () => (
  <svg
    xmlns="http://www.w3.org/2000/svg"
    width="16"
    height="16"
    viewBox="0 0 24 24"
    fill="none"
    stroke="currentColor"
    strokeWidth="2"
    strokeLinecap="round"
    strokeLinejoin="round"
  >
    <line x1="4" x2="20" y1="12" y2="12" />
    <line x1="4" x2="20" y1="6" y2="6" />
    <line x1="4" x2="20" y1="18" y2="18" />
  </svg>
);

interface HeaderProps {
  onMenuClick: () => void;
}

export function Header({ onMenuClick }: HeaderProps) {
  return (
    <header className="h-14 border-b border-border bg-card items-center px-4 gap-3 flex justify-between">
      <div>

      {/* Mobile menu button */}
      <Button
        variant="ghost"
        size="icon"
        className="lg:hidden"
        onClick={onMenuClick}
        aria-label="Open menu"
      >
        <MenuIcon />
      </Button>

      {/* Store name */}
      <h1 className="text-lg font-semibold text-foreground truncate">
        {StoreNameSignal.value}
      </h1>
      </div>
      <span>
        {ThemeSignal.value === 'dark' ? <Sun onClick={()=>ThemeSignal.value = 'light'} /> : <Moon onClick={()=>ThemeSignal.value = 'dark'} />}
      </span>
    </header>
  );
}
