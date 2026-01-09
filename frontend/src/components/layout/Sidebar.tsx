import { useState } from "react";
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";
import { SquarePen } from "lucide-react";

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
  id: string;
  title: string;
  timestamp: Date;
}

export interface UserProfile {
  name: string;
  email: string;
  avatar?: string;
}

interface SidebarProps {
  isOpen: boolean;
  isExpanded: boolean;
  onToggleExpand: () => void;
  onClose: () => void;
  onNewChat: () => void;
  onSelectChat: (chatId: string) => void;
  onLogout: () => void;
  chatHistory: ChatHistoryItem[];
  user: UserProfile;
}

export function Sidebar({
  isOpen,
  isExpanded,
  onToggleExpand,
  onClose,
  onNewChat,
  onSelectChat,
  onLogout,
  chatHistory,
  user,
}: SidebarProps) {
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
            onClick={onNewChat}
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
            {chatHistory.map((chat) => (
              <Button
                key={chat.id}
                variant="ghost"
                className={cn(
                  "w-full justify-start",
                  !isExpanded && "justify-center px-0"
                )}
                onClick={() => onSelectChat(chat.id)}
                title={chat.title}
              >
                <MessageSquareIcon />
                {isExpanded && (
                  <span className="truncate flex-1 text-left">{chat.title}</span>
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
            {user.avatar ? (
              <img
                src={user.avatar}
                alt={user.name}
                className="w-8 h-8 rounded-full object-cover"
              />
            ) : (
              <div className="w-8 h-8 rounded-full bg-primary/10 flex items-center justify-center">
                <UserIcon />
              </div>
            )}
            {isExpanded && (
              <div className="flex-1 min-w-0">
                <p className="text-sm font-medium truncate">{user.name}</p>
                <p className="text-xs text-muted-foreground truncate">
                  {user.email}
                </p>
              </div>
            )}
          </div>
          <Button
            variant="ghost"
            className={cn(
              "w-full text-destructive hover:text-destructive hover:bg-destructive/10",
              !isExpanded && "justify-center px-0"
            )}
            onClick={onLogout}
          >
            <LogOutIcon />
            {isExpanded && <span>Logout</span>}
          </Button>
        </div>
      </aside>
    </>
  );
}
