import { createFileRoute } from "@tanstack/react-router";
import { useState, useEffect } from "react";
import { SendIcon, Bot, User } from "lucide-react";

import {
  ResizableHandle,
  ResizablePanel,
  ResizablePanelGroup,
} from "@/components/ui/resizable";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Textarea } from "@/components/ui/textarea";
import { Button } from "@/components/ui/button";
import { Card, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import { AppLayout } from "@/components/layout";

export const Route = createFileRoute("/$storeName/chat")({
  component: ChatPage,
});

interface Message {
  id: string;
  role: "user" | "agent";
  content: string;
  timestamp: Date;
}

interface Product {
  id: string;
  name: string;
  price: string;
  description: string;
  image?: string;
}

function ChatPage() {
  const { storeName } = Route.useParams();
  const [messages, setMessages] = useState<Message[]>([
    {
      id: "1",
      role: "agent",
      content: `Hello! I'm your assistant for ${storeName}. How can I help you find the perfect product today?`,
      timestamp: new Date(),
    },
  ]);
  const [input, setInput] = useState("");
  const [recommendedProducts, setRecommendedProducts] = useState<Product[]>([]);

  // Auto-scroll to bottom of chat
  useEffect(() => {
    const anchor = document.getElementById("scroll-anchor");
    if (anchor) {
      anchor.scrollIntoView({ behavior: "smooth" });
    }
  }, [messages]);

  const handleSendMessage = () => {
    if (!input.trim()) return;

    const userMsg: Message = {
      id: Date.now().toString(),
      role: "user",
      content: input,
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, userMsg]);
    setInput("");

    // Mock response for now
    setTimeout(() => {
      const agentMsg: Message = {
        id: (Date.now() + 1).toString(),
        role: "agent",
        content: "I'm looking into that for you. Here is a suggestion based on your request.",
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, agentMsg]);
      
      // Mock product recommendation
      if (recommendedProducts.length === 0) {
        setRecommendedProducts([
          {
            id: "p1",
            name: "Premium Wireless Headphones",
            price: "$299.99",
            description: "High-fidelity audio with active noise cancellation.",
          }
        ]);
      }
    }, 1000);
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  return (
    <AppLayout storeName='ab'>

    <div className="h-[calc(100vh-4rem)] w-full flex flex-col">
      <ResizablePanelGroup direction="horizontal" className="flex-1 items-stretch rounded-lg overflow-hidden bg-background">
        
        {/* Left Panel: Recommended Products */}
        <ResizablePanel defaultSize={60} minSize={20}  className="hidden md:block">
          <div className="flex flex-col h-full bg-muted/10 border-r">
            <div className="p-4 border-b bg-background/50 backdrop-blur-sm">
              <h2 className="font-semibold flex items-center gap-2">
                Recommended Products
              </h2>
            </div>
            
            <ScrollArea className="flex-1 p-4">
              {recommendedProducts.length === 0 ? (
                <div className="text-sm text-muted-foreground text-center py-10 px-4">
                  Ask me about products to see recommendations here.
                </div>
              ) : (
                <div className="space-y-4">
                  {recommendedProducts.map((product) => (
                    <Card key={product.id} className="overflow-hidden">
                      <div className="aspect-video bg-muted flex items-center justify-center text-muted-foreground">
                        {/* Placeholder for Product Image */}
                        No Image
                      </div>
                      <CardHeader className="p-4">
                        <div className="flex justify-between items-start gap-2">
                          <CardTitle className="text-base truncate" title={product.name}>{product.name}</CardTitle>
                          <span className="font-bold text-sm">{product.price}</span>
                        </div>
                        <CardDescription className="line-clamp-2 text-xs">
                          {product.description}
                        </CardDescription>
                      </CardHeader>
                    </Card>
                  ))}
                </div>
              )}
            </ScrollArea>
          </div>
        </ResizablePanel>

        <ResizableHandle withHandle />

        {/* Right Panel: Chat Interface */}
        <ResizablePanel defaultSize={40} minSize={40}>
          <div className="flex flex-col h-full bg-background relative">
            {/* Chat Messages */}
            <div className="flex-1 px-4 py-8 overflow-auto">
                {messages.map((msg) => (
                  <div key={msg.id} className="flex gap-4 group">
                    <Avatar className={`h-8 w-8 mt-1 border ${msg.role === 'agent' ? 'bg-primary/10' : 'bg-muted'}`}>
                      <AvatarFallback className="bg-transparent text-xs">
                         {msg.role === 'agent' ? <Bot size={16} /> : <User size={16} />}
                      </AvatarFallback>
                    </Avatar>
                    
                    <div className="flex-1 space-y-1">
                      <div className="flex items-center gap-2">
                        <span className="font-semibold text-sm">
                          {msg.role === 'agent' ? 'AI Agent' : 'You'}
                        </span>
                        <span className="text-xs text-muted-foreground opacity-0 group-hover:opacity-100 transition-opacity">
                          {msg.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                        </span>
                      </div>
                      <div className="text-sm leading-relaxed whitespace-pre-wrap text-foreground/90">
                        {msg.content}
                      </div>
                    </div>
                  </div>
                ))}
            </div>

            {/* Input Area */}
            <div className="p-4 bg-background border-t">
              <div className="max-w-3xl mx-auto relative flex flex-col gap-2">
                <div className="relative">
                  <Textarea
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    onKeyDown={handleKeyDown}
                    placeholder="Ask anything about our products..."
                    className="min-h-[60px] max-h-[200px] resize-none pr-12 text-sm shadow-sm"
                    rows={1}
                  />
                  <Button
                    onClick={handleSendMessage}
                    size="icon"
                    className="absolute right-2 bottom-2 h-8 w-8 transition-all"
                    variant={input.trim() ? "default" : "ghost"}
                    disabled={!input.trim()}
                  >
                    <SendIcon className="h-4 w-4" />
                  </Button>
                </div>
                <div className="text-center">
                   <p className="text-[10px] text-muted-foreground">
                      AI can make mistakes. Please check important info.
                   </p>
                </div>
              </div>
            </div>
          </div>
        </ResizablePanel>
      </ResizablePanelGroup>
    </div>
    </AppLayout>

  );
}
