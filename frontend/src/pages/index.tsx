import { useState } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { AlertCircle } from "lucide-react"



export function LandingPage() {
  const [username, setUsername] = useState("")
  const [password, setPassword] = useState("")
  const [error, setError] = useState("")
  const [isLoading, setIsLoading] = useState(false)

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault()
    setError("No User Found")
  }

  const handleDemoLogin = (role: "admin" | "user") => {
    
  }



  return (
    <div className='w-full h-full  flex justify-center items-center container'>

        <Card className="w-full max-w-md shadow-2xl border-border/50">
          <CardHeader className="space-y-2">
            <CardTitle className="text-2xl">Shopwise</CardTitle>
            <CardDescription>Sign in to your account to continue</CardDescription>
          </CardHeader>
          <CardContent className="space-y-6">
            {/* Login Form */}
            <form onSubmit={handleLogin} className="space-y-4">
              {error && (
                <div className="flex items-start gap-3 p-3 bg-destructive/10 border border-destructive/30 rounded-lg">
                  <AlertCircle className="w-5 h-5 text-destructive mt-0.5 flex-shrink-0" />
                  <p className="text-sm text-destructive">{error}</p>
                </div>
              )}

              <div className="space-y-2">
                <Label htmlFor="username" className="text-foreground">
                  Username
                </Label>
                <Input
                  id="username"
                  type="username"
                  placeholder="Enter your username"
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
                  disabled={isLoading}
                  className="bg-input border-border"
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="password" className="text-foreground">
                  Password
                </Label>
                <Input
                  id="password"
                  type="password"
                  placeholder="Enter your password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  disabled={isLoading}
                  className="bg-input border-border"
                />
              </div>

              <Button
                type="submit"
                disabled={isLoading || !username || !password}
                className="w-full bg-primary hover:bg-primary/90 text-primary-foreground"
              >
                {isLoading ? "Signing in..." : "Sign in"}
              </Button>
            </form>

            {/* Divider */}
            <div className="relative">
              <div className="absolute inset-0 flex items-center">
                <div className="w-full border-t border-border"></div>
              </div>
              <div className="relative flex justify-center text-sm">
                <span className="px-2 bg-card text-muted-foreground">Or try a demo account</span>
              </div>
            </div>

            {/* Demo Login Section */}
            <div className="space-y-3">
              <p className="text-sm text-muted-foreground text-center">Quick access with demo credentials</p>

              <div className="space-y-2.5">
                <Button
                  type="button"
                  onClick={() => handleDemoLogin("admin")}
                  variant="outline"
                  className="w-full border-border  cursor-pointer"
                  disabled={isLoading}
                >
                  <div className="flex flex-col items-start text-left">
                    <span className="font-semibold">Login as Admin</span>
                  </div>
                </Button>

                <Button
                  type="button"
                  onClick={() => handleDemoLogin("user")}
                  variant="outline"
                  className="w-full border-border  cursor-pointer"
                  disabled={isLoading}
                >
                  <div className="flex flex-col items-start text-left">
                    <span className="font-semibold">Login as User</span>
                  </div>
                </Button>
              </div>
            </div>
          </CardContent>
        </Card>

    </div>

  )
}
