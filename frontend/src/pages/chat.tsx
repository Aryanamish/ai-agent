import { useEffect, useRef, useState } from "react";
import { Textarea } from "@/components/ui/textarea";
import { cn } from "@/lib/utils";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Send, } from "lucide-react";
import API from "@/lib/Axios";
import { useParams,useOutletContext,useLoaderData } from "react-router";

interface IntemsSuggested{
  name: string,
        price: number,
        image: string,
}
interface ChatMessage {
  message: {
    type: "answer",
    content: {
      airesponse: string,
      item_suggested: IntemsSuggested[],

    }
  } | {
    type: "status",
    content: {
      airesponse: string,
    }
  } | {
    type: "usermessage",
    prompt: string
  };
  timestamp: string;
}




const RenderMessage = function ({ msg }: { msg: ChatMessage }) {
  try{

  if (msg.message.type === 'usermessage') {
    return <div className="w-full text-right">
      <span className="bg-muted p-4 rounded-lg">
          {msg.message.prompt}
      </span>
    </div>
  } else if (msg.message.type === 'answer') {
    return <div className="p-4 rounded-lg flex flex-col gap-1 w-full max-w-full overflow-hidden">
      {msg.message.content.airesponse.split("\n").map((p)=><p key={p}>{p}</p>)}
      <RenderProduct item_suggested={msg.message.content.item_suggested} />
    </div>
  } else if (msg.message.type === 'status') {
    return <div className="p-4 rounded-lg text-left italic">
      <p>
        {msg.message.content.airesponse}
      </p>
    </div>
  } else {
    return <div className="text-red-500 border p-3">Something went wrong</div>
  }
  }catch(e){
    console.error("Error rendering message:", e);
  }
}
const RenderProduct = function ({ item_suggested }: { item_suggested: IntemsSuggested[] }) {
  if (!item_suggested || item_suggested.length === 0) return null;

  return (
    <div className="w-full overflow-x-auto pb-2 -mx-1 px-1">
      <div className="flex gap-4 snap-x snap-mandatory w-max">
        {item_suggested.map((item, idx) => {
          return (
            <Card key={idx} className="w-[200px] flex-none snap-center">
              <div className="h-[150px] w-full overflow-hidden rounded-t-lg bg-muted">
                <img 
                  src={item.image} 
                  alt={item.name}
                  className="h-full w-full object-cover transition-transform hover:scale-105"
                />
              </div>
              <CardContent className="p-3">
                <p className="text-sm font-medium line-clamp-2 min-h-[2.5rem]" title={item.name}>
                  {item.name}
                </p>
                <p className="mt-1 font-bold text-sm">
                  ₹{item.price}
                </p>
              </CardContent>
            </Card>
          )
        })}
      </div>
    </div>
  )
}


const createChatRoom = async (slug: string, name:string) => {
  const data = await API.post(`${slug}/api/chat/create/`, {name: name});
  const chatRoomId = data.data.chat_room_id;
  history.pushState({}, "", `/${slug}/chat/${chatRoomId}`);
  return chatRoomId;
}

export default function Chat({  chatRoomId, initialMessage }: { chatRoomId?: string, initialMessage?: ChatMessage[] }) {
  const { slug } = useOutletContext<{slug:string}>();

  const [messages, setMessages] = useState<ChatMessage[]>(initialMessage || [])
  const [stream, setStream] = useState<string|null>(null);
  const [error, setError] = useState<string | null>(null);
  const [roomId, setRoomId] = useState<string | undefined>(chatRoomId);
  const textRef = useRef<HTMLTextAreaElement>(null);
  const chatAreaRef = useRef<HTMLDivElement>(null);
  
  useEffect(()=>{
    if(chatAreaRef.current){
      chatAreaRef.current.scrollTop = chatAreaRef.current.scrollHeight;
    }
  }, [messages])
  const sendMessage = async () => {

    if (!textRef.current) {
      return;
    }
    const msg = textRef.current.value.trim();
    if (msg === "") {
      return;
    }
    let chatRoomId = roomId;
    if (!roomId) {
      chatRoomId = await createChatRoom(slug, msg);
      setRoomId(chatRoomId);
    }
    setError(null);
    const newMessage: ChatMessage = {
      message: {
        type: "usermessage",
        prompt: msg
      },
      timestamp: new Date().toISOString()
    }
    textRef.current.value = ""
    setMessages(prev => [...prev, newMessage]);

    setStream("Thinking...")
    await API.stream(`/${slug}/api/chat/`, { ...newMessage, chat_room_id: chatRoomId },
      { headers: { "Content-type": "application/json" }, },
      (data: any) => {
        console.log(data);
        if (data.type === "status") {
          
          setStream(s => `${s}.  ${data.content.airesponse}`);
        }else if(data.type === "error"){
          setError("Something Went Wrong: " + data.content.airesponse);
          setStream(null)
        }else if(data.type === "answer"){
          setStream(null)
          setMessages(prev=>[...prev, {message: data, timestamp: new Date().toISOString()}]);
        }
      },
      (endMsg) => { console.log(endMsg) },
      (errorMsg) => { console.error(errorMsg) });



    setTimeout(() => {
      if (chatAreaRef.current) {
        chatAreaRef.current.scrollTop = chatAreaRef.current.scrollHeight;
      }
    }, 100);
  }



  const onKeypress = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  }
  return <div className="flex justify-center h-full py-7" key={roomId}>
    <div className={cn("h-full flex items-center w-full flex-col", messages.length > 1 ? "justify-between" : "justify-center")}>
      <div className="w-full flex flex-col gap-2 overflow-auto items-center pb-5 pt-5" ref={chatAreaRef}>
        <div className="w-3xl flex flex-col gap-10">

          {messages.map((msg, index) => {
            return <>
              <div key={index} className={`flex items-start space-x-4 w-full`}>
                <RenderMessage msg={msg} />
              </div>
            </>
          })}
          {stream !== null && <div className="flex items-start space-x-4 text-muted-foreground text-sm">
            <div className="p-4 rounded-lg text-left">
              <p>{stream}</p>
            </div>
          </div>}
          {error !== null && <div className="text-red-500 p-4 border rounded-sm bg-red-800/2">{error}</div>}
        </div>

      </div>
      <div className=" relative w-3xl">
        <Textarea className="w-full h-14" placeholder="Type your message here..." ref={textRef} onKeyDown={onKeypress}></Textarea>
        <Button className="absolute top-4 right-3" onClick={sendMessage}><Send /></Button>
      </div>
    </div>
  </div>
}


export function ChatWrapper() {
  const room = useLoaderData() as {data:ChatMessage[]};
  const params = useParams();
  const chatRoomId = params.chatRoomId;
  
  if (!chatRoomId) {
    return <div className="text-red-500">Chat Room ID is missing in the URL</div>
  }

  return <Chat key={chatRoomId} chatRoomId={chatRoomId} initialMessage={room.data}></Chat>
}