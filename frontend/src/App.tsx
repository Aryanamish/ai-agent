import { useState, useEffect } from 'react'
import useWebSocket, { ReadyState } from 'react-use-websocket'
import { Button } from '@/components/ui/button'

function App() {
  // Retrieve URL from environment variables
  const WS_URL = import.meta.env.VITE_WS_URL || 'ws://127.0.0.1:8000/ws/'

  const [streamedText, setStreamedText] = useState("")
  
  const { sendMessage, lastMessage, readyState } = useWebSocket(WS_URL, {
    shouldReconnect: () => true,
  })

  useEffect(() => {
    if (lastMessage !== null) {
      try {
        const data = JSON.parse(lastMessage.data)
        
        if (data.type === 'stream') {
            setStreamedText(prev => prev + data.content)
        } else if (data.type === 'info') {
            // Optional: handle info messages
            console.log("System:", data.content)
        } else if (data.type === 'end') {
            console.log("Stream ended")
        }
      } catch (e) {
        console.error("Error parsing message", e)
      }
    }
  }, [lastMessage])

  const connectionStatus = {
    [ReadyState.CONNECTING]: 'Connecting',
    [ReadyState.OPEN]: 'Open',
    [ReadyState.CLOSING]: 'Closing',
    [ReadyState.CLOSED]: 'Closed',
    [ReadyState.UNINSTANTIATED]: 'Uninstantiated',
  }[readyState]

  const handleSend = () => {
      setStreamedText("") // Reset for new stream
      sendMessage(JSON.stringify({ message: "Start Streaming" }))
  }

  return (
    <div className="min-h-screen bg-background p-8">
      <div className="max-w-2xl mx-auto space-y-6">
        <div className="space-y-2">
            <h1 className="text-3xl font-bold tracking-tight">Real-time Stream</h1>
            <div className="flex items-center gap-2 text-sm text-muted-foreground">
                <span>Status:</span>
                <span className={`font-medium ${readyState === ReadyState.OPEN ? 'text-green-600' : 'text-yellow-600'}`}>
                    {connectionStatus}
                </span>
            </div>
        </div>

        <div className="border rounded-lg p-6 bg-card text-card-foreground shadow-sm min-h-[200px] whitespace-pre-wrap font-mono text-sm leading-relaxed">
            {streamedText || <span className="text-muted-foreground/50 italic">AI response will appear here...</span>}
        </div>

        <div className="flex gap-4">
            <Button 
                onClick={handleSend} 
                disabled={readyState !== ReadyState.OPEN}
            >
                Trigger AI Stream
            </Button>
            <Button 
                variant="outline" 
                onClick={() => setStreamedText("")}
            >
                Clear
            </Button>
        </div>
      </div>
    </div>
  )
}

export default App
