"use client"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Card } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { ScrollArea } from "@/components/ui/scroll-area"
import { Sheet, SheetContent, SheetTrigger } from "@/components/ui/sheet"
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"
import {
  Menu,
  Send,
  Rocket,
  Briefcase,
  Wallet,
  BarChart3,
  TrendingUp,
  Settings,
  Moon,
  Sun,
  PanelRightOpen,
  Globe,
  User,
  CreditCard,
  Shield,
  Key,
  DollarSign,
  Coins,
} from "lucide-react"
import { useTheme } from "next-themes"

interface Message {
  id: string
  content: string
  sender: "user" | "assistant"
  timestamp: Date
}

export default function SwarmAI() {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: "1",
      content: "Welcome to Genesis | Ai Neural Link! Your crypto airdrop and faucet management system is ready.",
      sender: "assistant",
      timestamp: new Date(),
    },
  ])
  const [inputValue, setInputValue] = useState("")
  const [activeSection, setActiveSection] = useState("chat")
  const [rightDrawerOpen, setRightDrawerOpen] = useState(false)
  const { theme, setTheme } = useTheme()

  const sidebarItems = [
    { id: "crawler", label: "Web Crawler", icon: Globe },
    { id: "deploy", label: "Deploy Swarm", icon: Rocket },
    { id: "portfolio", label: "Portfolio", icon: Briefcase },
    { id: "wallets", label: "Wallets", icon: Wallet },
    { id: "analytics", label: "Analytics", icon: BarChart3 },
    { id: "graphs", label: "Graphs", icon: TrendingUp },
  ]

  const handleSendMessage = () => {
    if (!inputValue.trim()) return

    const newMessage: Message = {
      id: Date.now().toString(),
      content: inputValue,
      sender: "user",
      timestamp: new Date(),
    }

    setMessages((prev) => [...prev, newMessage])
    setInputValue("")

    // Simulate assistant response
    setTimeout(() => {
      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        content: "I received your message. How can I assist you with your swarm operations?",
        sender: "assistant",
        timestamp: new Date(),
      }
      setMessages((prev) => [...prev, assistantMessage])
    }, 1000)
  }

  const handleWebCrawler = async () => {
    try {
      const response = await fetch("/api/exec", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          action: "crawl",
          payload: { target: "faucets" },
        }),
      })
      const result = await response.json()

      // Add crawler logs to chat
      const crawlerMessage: Message = {
        id: Date.now().toString(),
        content: `🕷️ Web Crawler initiated for faucets. Status: ${result.status || "Processing..."}`,
        sender: "assistant",
        timestamp: new Date(),
      }
      setMessages((prev) => [...prev, crawlerMessage])

      console.log("Crawler result:", result)
    } catch (error) {
      console.error("Crawler failed:", error)
      const errorMessage: Message = {
        id: Date.now().toString(),
        content: "❌ Web Crawler failed to start. Please check your connection.",
        sender: "assistant",
        timestamp: new Date(),
      }
      setMessages((prev) => [...prev, errorMessage])
    }
  }

  const handleDeploySwarm = async () => {
    try {
      const response = await fetch("/api/exec", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ action: "deploy_swarm" }),
      })
      const result = await response.json()
      console.log("Deploy result:", result)
    } catch (error) {
      console.error("Deploy failed:", error)
    }
  }

  return (
    <div className="flex h-screen bg-black text-white">
      {/* Left Sidebar */}
      <div className="hidden md:flex w-64 glass-morph flex-col m-2 rounded-xl">
        <div className="p-6 border-b border-green-500/30">
          <h1 className="text-2xl font-bold text-white">
            Swarm{" "}
            <span className="text-green-400" style={{ textShadow: "0 0 8px rgba(34, 197, 94, 0.2)" }}>
              AI
            </span>
          </h1>
          <p className="text-xs text-cyan-300/70 mt-1">Crypto Management Platform</p>
        </div>
        <nav className="flex-1 p-4 space-y-3">
          {sidebarItems.map((item) => {
            const Icon = item.icon
            return (
              <Button
                key={item.id}
                variant="ghost"
                className={`w-full justify-start gap-3 h-12 rounded-lg transition-all duration-300 ${
                  activeSection === item.id
                    ? "glass-morph text-green-400 border-green-500/50 shadow-lg shadow-green-500/20"
                    : "text-white/80 hover:text-green-400 hover:bg-white/5 hover:border-green-500/30 border border-transparent"
                }`}
                onClick={() => {
                  setActiveSection(item.id)
                  if (item.id === "crawler") {
                    handleWebCrawler()
                  }
                  if (item.id === "deploy") {
                    handleDeploySwarm()
                  }
                  if (["portfolio", "wallets", "analytics", "graphs"].includes(item.id)) {
                    setRightDrawerOpen(true)
                  }
                }}
              >
                <Icon className="h-5 w-5" />
                <span className="font-medium">{item.label}</span>
              </Button>
            )
          })}
        </nav>
      </div>

      {/* Mobile Sidebar */}
      <Sheet>
        <SheetTrigger asChild>
          <Button variant="ghost" size="icon" className="md:hidden fixed top-4 left-4 z-50 glass-morph text-green-400">
            <Menu className="h-4 w-4" />
          </Button>
        </SheetTrigger>
        <SheetContent side="left" className="w-64 p-0 glass-morph border-green-500/30">
          <div className="p-4 border-b border-green-500/30">
            <h1 className="text-xl font-bold text-white">
              Swarm{" "}
              <span className="text-green-400" style={{ textShadow: "0 0 8px rgba(34, 197, 94, 0.2)" }}>
                AI
              </span>
            </h1>
          </div>
          <nav className="p-4 space-y-2">
            {sidebarItems.map((item) => {
              const Icon = item.icon
              return (
                <Button
                  key={item.id}
                  variant="ghost"
                  className={`w-full justify-start gap-3 ${
                    activeSection === item.id ? "text-green-400" : "text-white/80"
                  }`}
                  onClick={() => {
                    setActiveSection(item.id)
                    if (item.id === "crawler") {
                      handleWebCrawler()
                    }
                    if (item.id === "deploy") {
                      handleDeploySwarm()
                    }
                  }}
                >
                  <Icon className="h-4 w-4" />
                  {item.label}
                </Button>
              )
            })}
          </nav>
        </SheetContent>
      </Sheet>

      {/* Main Chat Area */}
      <div className="flex-1 flex flex-col m-2 ml-0 rounded-xl glass-morph-cyan overflow-hidden">
        {/* Header */}
        <div className="border-b border-cyan-500/30 p-4 flex items-center justify-between">
          <h2 className="text-lg font-semibold text-white">Genesis | Ai Neural Link</h2>
          <div className="flex items-center gap-2">
            <Button
              variant="ghost"
              size="icon"
              onClick={() => setRightDrawerOpen(!rightDrawerOpen)}
              className="hidden md:flex text-cyan-400 hover:text-cyan-300 hover:bg-white/5"
            >
              <PanelRightOpen className="h-4 w-4" />
            </Button>

            {/* Account Settings Dropdown */}
            <DropdownMenu>
              <DropdownMenuTrigger asChild>
                <Button
                  variant="ghost"
                  size="icon"
                  className="text-green-400 hover:text-green-300 hover:bg-white/5 glass-morph"
                >
                  <User className="h-4 w-4" />
                </Button>
              </DropdownMenuTrigger>
              <DropdownMenuContent align="end" className="w-56 glass-morph border-green-500/30 text-white">
                <DropdownMenuLabel className="text-green-400">Account Settings</DropdownMenuLabel>
                <DropdownMenuSeparator className="bg-green-500/30" />

                <DropdownMenuItem className="text-white hover:text-green-400 hover:bg-white/5">
                  <CreditCard className="mr-2 h-4 w-4" />
                  <span>Payment Methods</span>
                </DropdownMenuItem>

                <DropdownMenuItem className="text-white hover:text-green-400 hover:bg-white/5">
                  <Wallet className="mr-2 h-4 w-4" />
                  <span>Wallet Connections</span>
                </DropdownMenuItem>

                <DropdownMenuItem className="text-white hover:text-green-400 hover:bg-white/5">
                  <DollarSign className="mr-2 h-4 w-4" />
                  <span>Airdrop Settings</span>
                </DropdownMenuItem>

                <DropdownMenuItem className="text-white hover:text-green-400 hover:bg-white/5">
                  <Coins className="mr-2 h-4 w-4" />
                  <span>Faucet Management</span>
                </DropdownMenuItem>

                <DropdownMenuItem className="text-white hover:text-green-400 hover:bg-white/5">
                  <Key className="mr-2 h-4 w-4" />
                  <span>API Keys</span>
                </DropdownMenuItem>

                <DropdownMenuItem className="text-white hover:text-green-400 hover:bg-white/5">
                  <Shield className="mr-2 h-4 w-4" />
                  <span>Security</span>
                </DropdownMenuItem>

                <DropdownMenuSeparator className="bg-green-500/30" />

                <DropdownMenuItem className="text-white hover:text-green-400 hover:bg-white/5">
                  <Settings className="mr-2 h-4 w-4" />
                  <span>General Settings</span>
                </DropdownMenuItem>

                {/* Theme Toggle */}
                <DropdownMenuItem
                  className="text-white hover:text-cyan-400 hover:bg-white/5"
                  onClick={() => setTheme(theme === "dark" ? "light" : "dark")}
                >
                  {theme === "dark" ? <Sun className="mr-2 h-4 w-4" /> : <Moon className="mr-2 h-4 w-4" />}
                  <span>{theme === "dark" ? "Light Mode" : "Dark Mode"}</span>
                </DropdownMenuItem>
              </DropdownMenuContent>
            </DropdownMenu>
          </div>
        </div>

        {/* Messages */}
        <ScrollArea className="flex-1 p-4">
          <div className="space-y-4 max-w-4xl mx-auto">
            {messages.map((message) => (
              <div key={message.id} className={`flex ${message.sender === "user" ? "justify-end" : "justify-start"}`}>
                <div
                  className={`max-w-[80%] p-4 rounded-xl transition-all duration-300 ${
                    message.sender === "user" ? "text-white" : "text-white"
                  }`}
                >
                  <p className="text-sm leading-relaxed">{message.content}</p>
                  <p className="text-xs opacity-60 mt-2 text-cyan-300">{message.timestamp.toLocaleTimeString()}</p>
                </div>
              </div>
            ))}
          </div>
        </ScrollArea>

        {/* Input Area */}
        <div className="border-t border-cyan-500/30 p-4">
          <div className="max-w-4xl mx-auto flex gap-3">
            <Input
              placeholder="Enter neural command..."
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              onKeyPress={(e) => e.key === "Enter" && handleSendMessage()}
              className="flex-1 glass-morph border-green-500/30 text-white placeholder:text-white/50 focus:border-green-500/70 focus:ring-green-500/20 rounded-lg h-12"
            />
            <Button
              onClick={handleSendMessage}
              size="icon"
              className="neon-border bg-gradient-to-r from-green-500 to-cyan-500 hover:from-green-400 hover:to-cyan-400 text-black font-bold h-12 w-12 rounded-lg"
            >
              <Send className="h-5 w-5" />
            </Button>
          </div>
        </div>
      </div>

      {/* Right Drawer */}
      <Sheet open={rightDrawerOpen} onOpenChange={setRightDrawerOpen}>
        <SheetContent side="right" className="w-80 glass-morph border-cyan-500/30 text-white">
          <div className="p-4">
            <h3 className="text-lg font-semibold mb-4 text-green-400">
              {activeSection === "portfolio" && "Portfolio Analytics"}
              {activeSection === "wallets" && "Wallet Management"}
              {activeSection === "analytics" && "System Analytics"}
              {activeSection === "graphs" && "Performance Graphs"}
            </h3>

            {activeSection === "portfolio" && (
              <div className="space-y-4">
                <Card className="glass-morph border-green-500/30 p-4">
                  <h4 className="font-medium mb-2 text-cyan-300">Total Portfolio Value</h4>
                  <p className="text-2xl font-bold text-green-400 neon-glow">$12,345.67</p>
                  <p className="text-xs text-green-300/70 mt-1">+2.34% (24h)</p>
                </Card>
                <div className="text-sm text-cyan-300/70">Advanced portfolio analytics loading...</div>
              </div>
            )}

            {activeSection === "wallets" && (
              <div className="space-y-4">
                <Card className="glass-morph border-green-500/30 p-4">
                  <h4 className="font-medium mb-2 text-cyan-300">Connected Wallets</h4>
                  <p className="text-sm text-green-400">3 wallets active</p>
                  <div className="mt-2 space-y-1">
                    <div className="text-xs text-white/70">• MetaMask: Connected</div>
                    <div className="text-xs text-white/70">• WalletConnect: Active</div>
                    <div className="text-xs text-white/70">• Hardware: Secured</div>
                  </div>
                </Card>
              </div>
            )}

            {activeSection === "analytics" && (
              <div className="space-y-4">
                <Card className="glass-morph border-green-500/30 p-4">
                  <h4 className="font-medium mb-2 text-cyan-300">Success Rate</h4>
                  <p className="text-2xl font-bold text-green-400 neon-glow">87.3%</p>
                  <p className="text-xs text-green-300/70 mt-1">Swarm efficiency</p>
                </Card>
                <Card className="glass-morph border-green-500/30 p-4">
                  <h4 className="font-medium mb-2 text-cyan-300">Active Swarms</h4>
                  <p className="text-xl font-bold text-cyan-400">12</p>
                </Card>
              </div>
            )}

            {activeSection === "graphs" && (
              <div className="space-y-4">
                <Card className="glass-morph border-green-500/30 p-4">
                  <h4 className="font-medium mb-2 text-cyan-300">Performance Matrix</h4>
                  <div className="h-32 glass-morph border-green-500/20 rounded-lg flex items-center justify-center">
                    <p className="text-sm text-green-400">Neural network visualization</p>
                  </div>
                </Card>
              </div>
            )}
          </div>
        </SheetContent>
      </Sheet>
    </div>
  )
}
