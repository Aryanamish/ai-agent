import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { cn } from "@/lib/utils";
import { Send } from "lucide-react";
import { useRef, useState } from "react";
import API from "@/lib/Axios";
import  Chat from "./chat";

export default function NewChat({ slug}: { slug: string}) {
  const textRef = useRef<HTMLTextAreaElement>(null);
  const [chatRoomId, setChatRoomId] = useState<string | null>(null);
  const [chatMessage, setChatMessage] = useState<string|null>(null);
  const createChatRoom = async ()=>{
    if (!textRef.current) {
      return;
    }
    const msg = textRef.current.value.trim();
    if (msg === "") {
      return;
    }
    const data = await API.get(`${slug}/api/chat/create/`);
    const chatRoomId = data.data.chat_room_id;
    setChatRoomId(chatRoomId);
    setChatMessage(msg);
    history.pushState({}, "", `/${slug}/chat/${chatRoomId}`);
  }
  const onKeypress = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      createChatRoom();
    }
  }
  if(chatRoomId && chatMessage){
    return <Chat slug={slug} chatRoomId={chatRoomId} initialMessage={chatMessage} ></Chat>
  }
  return <div className="flex justify-center h-full py-7">
      <div className={cn("h-full flex items-center w-full flex-col justify-center")}>
        <div className=" relative w-3xl">
          <Textarea className="w-full h-14" placeholder="Type your message here..." ref={textRef} onKeyDown={onKeypress}></Textarea>
          <Button className="absolute top-4 right-3" onClick={createChatRoom}><Send /></Button>
        </div>
      </div>
    </div>
}