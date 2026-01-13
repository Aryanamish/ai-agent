import { useState} from "react";
import { Header } from "./Header";
import { Sidebar, type ChatHistoryItem, type UserProfile } from "./Sidebar";

interface AppLayoutProps {
  children: React.ReactNode;
  orgName: string;
  chatHistory?: ChatHistoryItem[];
  user?: UserProfile;
  onNewChat?: () => void;
  onSelectChat?: (chatId: string) => void;
  onLogout?: () => void;
  orgSlug:string
}





export function AppLayout({
  children,
  orgName,
  orgSlug,
}: AppLayoutProps) {
  
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);
  const [isSidebarExpanded, setIsSidebarExpanded] = useState<boolean>(localStorage.getItem("sidebarExpanded") === 'true');

  const handleOpenSidebar = () => setIsSidebarOpen(true);
  const handleCloseSidebar = () => setIsSidebarOpen(false);
  const handleToggleExpand = () => setIsSidebarExpanded((prev) => !prev);


  return (
    <div className="flex h-screen w-full overflow-hidden">
      <Sidebar
        orgSlug={orgSlug}
        isOpen={isSidebarOpen}
        isExpanded={isSidebarExpanded}
        onToggleExpand={handleToggleExpand}
        onClose={handleCloseSidebar}
      />
      <div className="flex-1 flex flex-col min-w-0">
        <Header orgSlug={orgSlug} onMenuClick={handleOpenSidebar} orgName={orgName} />
        <main className="flex-1 overflow-hidden">{children}</main>
      </div>
    </div>
  );
}
