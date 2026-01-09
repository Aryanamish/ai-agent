import { useState } from "react";
import { Header } from "./Header";
import { Sidebar, type ChatHistoryItem, type UserProfile } from "./Sidebar";

interface AppLayoutProps {
  children: React.ReactNode;
  storeName: string;
  chatHistory?: ChatHistoryItem[];
  user?: UserProfile;
  onNewChat?: () => void;
  onSelectChat?: (chatId: string) => void;
  onLogout?: () => void;
}

// Default sample data
const defaultChatHistory: ChatHistoryItem[] = [
  { id: "1", title: "Product recommendations", timestamp: new Date() },
  { id: "2", title: "Order status inquiry", timestamp: new Date() },
  { id: "3", title: "Return policy questions", timestamp: new Date() },
  { id: "4", title: "Size guide help", timestamp: new Date() },
  { id: "5", title: "Shipping options", timestamp: new Date() },
];

const defaultUser: UserProfile = {
  name: "John Doe",
  email: "john@example.com",
};

export function AppLayout({
  children,
  storeName,
  chatHistory = defaultChatHistory,
  user = defaultUser,
  onNewChat = () => console.log("New chat"),
  onSelectChat = (id) => console.log("Select chat:", id),
  onLogout = () => console.log("Logout"),
}: AppLayoutProps) {
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);
  const [isSidebarExpanded, setIsSidebarExpanded] = useState(false);

  const handleOpenSidebar = () => setIsSidebarOpen(true);
  const handleCloseSidebar = () => setIsSidebarOpen(false);
  const handleToggleExpand = () => setIsSidebarExpanded((prev) => !prev);

  return (
    <div className="flex h-screen w-full overflow-hidden">
      <Sidebar
        isOpen={isSidebarOpen}
        isExpanded={isSidebarExpanded}
        onToggleExpand={handleToggleExpand}
        onClose={handleCloseSidebar}
        onNewChat={onNewChat}
        onSelectChat={onSelectChat}
        onLogout={onLogout}
        chatHistory={chatHistory}
        user={user}
      />
      <div className="flex-1 flex flex-col min-w-0">
        <Header onMenuClick={handleOpenSidebar} />
        <main className="flex-1 overflow-hidden">{children}</main>
      </div>
    </div>
  );
}
