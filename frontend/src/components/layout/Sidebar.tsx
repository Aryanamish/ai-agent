import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";
import { SquarePen } from "lucide-react";
import API from "@/lib/Axios";
import { useNavigate } from "react-router";
import { useEffect,useState } from "react";
import { Skeleton } from "@/components/ui/skeleton";

// Icons as simple SVG components
const ChevronLeftIcon = () => (
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
    <path d="m15 18-6-6 6-6" />
  </svg>
);

const ChevronRightIcon = () => (
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
    <path d="m9 18 6-6-6-6" />
  </svg>
);

const PlusIcon = () => (
  <SquarePen />
);

const MessageSquareIcon = () => (
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
    <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z" />
  </svg>
);

const UserIcon = () => (
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
    <path d="M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2" />
    <circle cx="12" cy="7" r="4" />
  </svg>
);

const LogOutIcon = () => (
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
    <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4" />
    <polyline points="16 17 21 12 16 7" />
    <line x1="21" x2="9" y1="12" y2="12" />
  </svg>
);

const XIcon = () => (
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
    <path d="M18 6 6 18" />
    <path d="m6 6 12 12" />
  </svg>
);

export interface ChatHistoryItem {
  slug: string;
  name: string;
  timestamp: Date;
}

export interface UserProfile {
  username: string;
  email: string;
  first_name: string;
  last_name: string;
}

interface SidebarProps {
  isOpen: boolean;
  isExpanded: boolean;
  onToggleExpand: () => void;
  onClose: () => void;
  orgSlug: string;
}

export function Sidebar({
  isOpen,
  isExpanded,
  orgSlug,
  onToggleExpand,
  onClose
}: SidebarProps) {
  //TODO history will not be uptodatd when new chat is created. do some props drilling or global state management
  const [chatHistory, setChatHistory] = useState<ChatHistoryItem[]|null>(null);
  const navigate = useNavigate()
  const [userProfile, setUserProfile] = useState<UserProfile|null>();
  const logout = async ()=>{
    await API.post("/admin/logout/");
    window.location.href = "/admin/login/";
  }
  const chatClicked = (chatSlug:string)=>{
    navigate(`/${orgSlug}/chat/${chatSlug}`);
  }
  const newChat = ()=>{
    navigate(`/${orgSlug}/chat/`);
  }
  useEffect(()=>{
    const controller = new AbortController();
    API.get(`${orgSlug}/api/chat/history/`, {signal: controller.signal}).then(data=>{
      setChatHistory(data.data);
    })
    API.get("/api/user/", {signal: controller.signal}).then(rsp=>{
      setUserProfile(rsp.data);
    })
    return ()=>{
      controller.abort();
    }
  },[])
    useEffect(()=>{
    localStorage.setItem("sidebarExpanded", isExpanded.toString());
    console.log(isExpanded)
  }, [isExpanded])
  return (
    <>
      {/* Mobile overlay */}
      {isOpen && (
        <div
          className="fixed inset-0 bg-black/50 z-40 lg:hidden"
          onClick={onClose}
        />
      )}

      {/* Sidebar */}
      <aside
        className={cn(
          "fixed left-0 top-0 h-full bg-card border-r border-border z-50 flex flex-col transition-all duration-300",
          // Mobile: slide in/out
          "lg:relative lg:translate-x-0",
          isOpen ? "translate-x-0" : "-translate-x-full",
          // Width based on expanded state
          isExpanded ? "w-64" : "w-16"
        )}
      >
        {/* Toggle button - desktop only */}
        <div className="hidden lg:flex justify-end p-2">
          <Button
            variant="ghost"
            size="icon-sm"
            onClick={onToggleExpand}
            aria-label={isExpanded ? "Collapse sidebar" : "Expand sidebar"}
          >
            {isExpanded ? <ChevronLeftIcon /> : <ChevronRightIcon />}
          </Button>
        </div>

        {/* Close button - mobile only */}
        <div className="flex lg:hidden justify-end p-2">
          <Button
            variant="ghost"
            size="icon-sm"
            onClick={onClose}
            aria-label="Close sidebar"
          >
            <XIcon />
          </Button>
        </div>

        {/* New Chat Button */}
        <div className="p-2">
          <Button
            variant="default"
            className={cn("w-full", !isExpanded && "justify-center px-0")}
            onClick={newChat}
          >
            <PlusIcon />
            {isExpanded && <span>New Chat</span>}
          </Button>
        </div>

        {/* Chat History Section */}
        <div className="flex-1 overflow-hidden flex flex-col">
          {isExpanded && (
            <div className="px-3 py-2">
              <span className="text-xs font-medium text-muted-foreground uppercase tracking-wider">
                History
              </span>
            </div>
          )}
          <div className="flex-1 overflow-y-auto px-2 space-y-1">
            {chatHistory === null ? <div className='flex flex-col gap-2'>
              <Skeleton className="h-8 w-full" />
              <Skeleton className="h-8 w-full" />
              <Skeleton className="h-8 w-full" />
            </div> : chatHistory.map((chat) => (
              <Button
                key={chat.slug}
                variant="ghost"
                className={cn(
                  "w-full justify-start cursor-pointer",
                  !isExpanded && "justify-center px-0"
                )}
                onClick={()=>chatClicked(chat.slug)}
                title={chat.name}
              >
                <MessageSquareIcon />
                {isExpanded && (
                  <span className="truncate flex-1 text-left">{chat.name}</span>
                )}
              </Button>
            ))}
          </div>
        </div>

        {/* User Profile Section */}
        <div className="border-t border-border p-2 space-y-2">
          <div
            className={cn(
              "flex items-center gap-2 p-2 rounded-md",
              isExpanded ? "justify-start" : "justify-center"
            )}
          >
            {userProfile ? 
            <>
              <div className="w-8 h-8 rounded-full bg-primary/10 flex items-center justify-center">
                <UserIcon />
              </div>
            
            {isExpanded && (
              <div className="flex-1 min-w-0">
                <p className="text-sm font-medium truncate">{userProfile.first_name} {userProfile.last_name}</p>
                <p className="text-xs text-muted-foreground truncate">{userProfile.email}</p>
                
              </div>
            )}
            </>:
            <>
            <Skeleton className="w-8 h-8 rounded-full" />
            {isExpanded && 
              <div className="flex-1 min-w-0">
                <Skeleton className="h-4 w-full mb-2" />
                <Skeleton className="h-3 w-3/4" />
              </div>
            }
            </>
            }

          </div>
          <Button
            variant="ghost"
            className={cn(
              "w-full text-destructive hover:text-destructive hover:bg-destructive/10",
              !isExpanded && "justify-center px-0"
            )}
            onClick={logout}
          >
            <LogOutIcon />
            {isExpanded && <span>Logout</span>}
          </Button>
        </div>
      </aside>
    </>
  );
}
