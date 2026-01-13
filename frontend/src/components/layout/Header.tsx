import { Button } from "@/components/ui/button";
import { ThemeSignal } from "@/signals";
import { Sun, Moon,Download } from "lucide-react"
import API from "@/lib/Axios";

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
  orgName: string;
  orgSlug:string;
}

export function Header({ onMenuClick, orgName, orgSlug }: HeaderProps) {
  let showDownloadButton = !(window.location.href.endsWith("/chat") || window.location.href.endsWith("/chat/"));
  const download = async ()=>{
    if(!showDownloadButton){
      return;
    }

    // making API call again because i dont want to deal with props drilling right now
    // ideally this should be handles by a stateManager or tanStack query type library.
    const urlPaths = window.location.href.split("/");
    const chatSlug = urlPaths.pop()
    const response = await API.get(`/${orgSlug}/api/chat/history/${chatSlug}`);
    const jsonString = JSON.stringify(response.data, null, 2);
    const blob = new Blob([jsonString], { type: "application/json" });
    const url = URL.createObjectURL(blob);

    const anchor = document.createElement("a");
    anchor.href = url;
    anchor.download = `shopwise-chat-history-${chatSlug}.json`;
    document.body.appendChild(anchor);
    anchor.click();

    document.body.removeChild(anchor);
    URL.revokeObjectURL(url);

  }
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
          {orgName}
        </h1>
      </div>
      <div className='flex gap-4'>
        {showDownloadButton && <Download onClick={download} />}
      <span>
        {ThemeSignal.value === 'dark' ? <Sun onClick={() => ThemeSignal.value = 'light'} /> : <Moon onClick={() => ThemeSignal.value = 'dark'} />}
      </span>
      </div>
    </header>
  );
}
