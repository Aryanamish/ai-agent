import { useEffect, useRef, useState } from "react";
import { Textarea } from "@/components/ui/textarea";
import { cn } from "@/lib/utils";
import { Button } from "@/components/ui/button";
import { Send, } from "lucide-react";
import API from "@/lib/Axios";
import { useParams } from "react-router";

interface ChatMessage {
  message: {
    type: "answer",
    content: {
      airesponse: string,
      item_suggested: number[],

    }
  } | {
    type: "question",
    content: {
      question: string,
      options: string[],
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
  sender: "user" | "agent";
  timestamp: string;
}

const DummyMessages: ChatMessage[] = [
  {
    message: {
      type: "answer",
      content: {
        airesponse: "Hello! How can I assist you today?",
        item_suggested: []
      }
    },
    sender: "agent",
    timestamp: "2023-10-01T10:00:00Z"
  },
  {
    message: {
      type: "usermessage",
      prompt: "I am looking for a black shirt.",
    },
    sender: "user",
    timestamp: "2023-10-01T10:05:00Z"
  },
  {
    message: {
      type: "answer",
      content: {
        airesponse: "Show me black shirts.",
        item_suggested: [101, 102]
      }
    },
    sender: "agent",
    timestamp: "2023-10-01T10:05:00Z"
  }
]


const RenderMessage = function ({ msg }: { msg: ChatMessage }) {
  try{

  if (msg.message.type === 'usermessage') {
    return <div className="p-4 rounded-lg bg-muted text-right">
      <p>
        {msg.message.prompt}
      </p>
    </div>
  } else if (msg.message.type === 'answer') {
    return <div className="p-4 rounded-lg text-left flex flex-col gap-1">
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
    debugger;
  }
}
const RenderProduct = function ({ item_suggested }: { item_suggested: number[] }) {
  return <ul className="list-disc list-inside">
    Products
  </ul>
}


const createChatRoom = async (slug: string) => {
  const data = await API.get(`${slug}/api/chat/create/`);
  const chatRoomId = data.data.chat_room_id;
  debugger;
  history.pushState({}, "", `/${slug}/chat/${chatRoomId}`);
  return chatRoomId;
}

export default function Chat({ slug, chatRoomId, initialMessage }: { slug: string, chatRoomId?: string, initialMessage?: ChatMessage[] }) {
  const [messages, setMessages] = useState<ChatMessage[]>(initialMessage || [])
  const [stream, setStream] = useState<string>("");
  const [roomId, setRoomId] = useState<string | undefined>(chatRoomId);
  const textRef = useRef<HTMLTextAreaElement>(null);
  const chatAreaRef = useRef<HTMLDivElement>(null);
  

  const sendMessage = async () => {

    if (!textRef.current) {
      return;
    }
    const msg = textRef.current.value.trim();
    if (msg === "") {
      return;
    }
    if (!roomId) {
      const chatRoomId = await createChatRoom(slug);
      setRoomId(chatRoomId);
    }
    const newMessage: ChatMessage = {
      message: {
        type: "usermessage",
        prompt: msg
      },
      sender: "user",
      timestamp: new Date().toISOString()
    }
    textRef.current.value = ""
    setMessages(prev => [...prev, newMessage]);


    const data = await API.stream(`/${slug}/api/chat/`, { ...newMessage, chat_room_id: roomId },
      { headers: { "Content-type": "application/json" }, },
      (data: any) => {
        if (data.type === "status") {
          setStream(s => s + " " + data.content.airesponse);
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
  return <div className="flex justify-center h-full py-7">
    <div className={cn("h-full flex items-center w-full flex-col", messages.length > 1 ? "justify-between" : "justify-center")}>
      <div className="w-full flex flex-col gap-2 overflow-auto items-center pb-5 pt-5" ref={chatAreaRef}>
        <div className="w-3xl flex flex-col gap-5">

          {messages.map((msg, index) => {
            return <>
              <div key={index} className={`flex items-start space-x-4 ${msg.sender === "user" ? "flex-row-reverse space-x-reverse" : ""}`}>
                <RenderMessage msg={msg} />
              </div>
            </>
          })}
          {stream && <div className="flex items-start space-x-4">
            <div className="p-4 rounded-lg text-left italic">
              <p>{stream}</p>
            </div>
          </div>}
        </div>

      </div>
      <div className=" relative w-3xl">
        <Textarea className="w-full h-14" placeholder="Type your message here..." ref={textRef} onKeyDown={onKeypress}></Textarea>
        <Button className="absolute top-4 right-3" onClick={sendMessage}><Send /></Button>
      </div>
    </div>
  </div>
}


export function ChatWrapper({ slug }: { slug: string }) {
  const params = useParams();
  const chatRoomId = params.chatRoomId;
  const [messages, setMessages] = useState<ChatMessage[] | null>(null);
  useEffect(()=>{
    const controller = new AbortController();
    API.get(`/${slug}/api/chat/history/${chatRoomId}/`, {signal:controller.signal}).then((data)=>{
      const res = data.data as ChatMessage[];
      setMessages(res);
    })
    return ()=>{controller.abort();}
  },[])
  if (!chatRoomId) {
    return <div className="text-red-500">Chat Room ID is missing in the URL</div>
  }
  if(messages){

    return <Chat slug={slug} chatRoomId={chatRoomId} initialMessage={messages}></Chat>
  }
  return <>Loading...</>
}