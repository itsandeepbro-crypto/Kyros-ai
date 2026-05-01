/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import { useState, useEffect, useRef } from 'react';
import { 
  Terminal, 
  Smartphone, 
  Cpu, 
  Zap, 
  Settings, 
  History, 
  Play, 
  Send, 
  FileCode, 
  Youtube, 
  MessageSquare, 
  Globe, 
  Command,
  Download,
  CheckCircle2,
  AlertCircle
} from 'lucide-react';
import { motion, AnimatePresence } from 'motion/react';

// Simulated Intent Parser for the Web Demo
const parseWebIntent = (text: string) => {
  const t = text.toLowerCase();
  if (t.includes('youtube')) {
    if (t.includes('search')) return { type: 'YouTube Search', detail: t.split('search')[1].split('on')[0].trim(), icon: <Youtube className="w-4 h-4 text-red-500" /> };
    return { type: 'Open YouTube', detail: 'Native App Launch', icon: <Youtube className="w-4 h-4 text-red-500" /> };
  }
  if (t.includes('whatsapp')) return { type: 'WhatsApp Messaging', detail: 'Contact Lookup via JSON', icon: <MessageSquare className="w-4 h-4 text-green-500" /> };
  if (t.includes('battery')) return { type: 'System Control', detail: 'Termux Battery Probe', icon: <Zap className="w-4 h-4 text-yellow-500" /> };
  if (t.includes('flashlight')) return { type: 'System Control', detail: 'Hardware Torch API', icon: <Zap className="w-4 h-4 text-yellow-500" /> };
  if (t.includes('google')) return { type: 'Web Intelligence', detail: 'Chrome Intent Search', icon: <Globe className="w-4 h-4 text-blue-500" /> };
  if (t.includes('file')) return { type: 'File Manager', detail: 'NV Storage I/O', icon: <FileCode className="w-4 h-4 text-purple-500" /> };
  return { type: 'Gemini AI Fallback', detail: 'LLM Reasoning', icon: <Cpu className="w-4 h-4 text-emerald-500" /> };
};

const Header = () => (
  <header className="border-b border-white/10 py-6 px-8 flex justify-between items-center bg-[#0a0a0a]/80 backdrop-blur-md sticky top-0 z-50">
    <div className="flex items-center gap-3">
      <div className="w-10 h-10 bg-cyan-500 rounded-lg flex items-center justify-center shadow-[0_0_20px_rgba(6,182,212,0.5)]">
        <Cpu className="text-black w-6 h-6" />
      </div>
      <div>
        <h1 className="font-sans font-bold text-xl tracking-tighter text-white uppercase italic">KYROS</h1>
        <p className="font-mono text-[10px] text-cyan-500/70 tracking-widest uppercase">Android Automation OS</p>
      </div>
    </div>
    <div className="flex gap-6 font-mono text-[11px] text-white/40 uppercase tracking-widest">
      <span className="flex items-center gap-2"><Smartphone className="w-3 h-3" /> Termux Native</span>
      <span className="flex items-center gap-2 text-cyan-500"><Zap className="w-3 h-3 animate-pulse" /> Live v1.0.4</span>
    </div>
  </header>
);

const TerminalLine = ({ text, type = 'input' }: { text: string; type?: 'input' | 'output' | 'system' }) => (
  <motion.div 
    initial={{ opacity: 0, x: -5 }}
    animate={{ opacity: 1, x: 0 }}
    className={`mb-2 font-mono text-xs ${
      type === 'input' ? 'text-white' : 
      type === 'system' ? 'text-cyan-500/60 font-italic' : 
      'text-white/60'
    }`}
  >
    <span className="opacity-30 mr-2">{type === 'input' ? 'λ' : type === 'system' ? '::' : '>'}</span>
    {text}
  </motion.div>
);

export default function App() {
  const [inputValue, setInputValue] = useState('');
  const [terminalLines, setTerminalLines] = useState<{text: string, type: 'input' | 'output' | 'system'}[]>([
    { text: 'KYROS Intelligence Initialization sequence complete.', type: 'system' },
    { text: 'Listening for Android Automation commands...', type: 'system' }
  ]);
  const [detectedIntent, setDetectedIntent] = useState<any>(null);
  const terminalRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (terminalRef.current) {
      terminalRef.current.scrollTop = terminalRef.current.scrollHeight;
    }
  }, [terminalLines]);

  const handleCommand = (e: React.FormEvent) => {
    e.preventDefault();
    if (!inputValue.trim()) return;

    const newLines = [...terminalLines, { text: inputValue, type: 'input' } as const];
    const intent = parseWebIntent(inputValue);
    
    setDetectedIntent(intent);
    
    // Simulate thinking
    setTimeout(() => {
      setTerminalLines([...newLines, 
        { text: `Intent Parsed: ${intent.type} -> ${intent.detail}`, type: 'system' },
        { text: `Executing automation hook... [SUCCESS]`, type: 'output' }
      ]);
      setInputValue('');
    }, 400);
  };

  return (
    <div className="min-h-screen bg-[#050505] text-white font-sans selection:bg-cyan-500/30">
      <Header />

      <main className="max-w-7xl mx-auto p-8 grid lg:grid-cols-12 gap-8">
        
        {/* Left: Setup & Hardware Status */}
        <div className="lg:col-span-4 space-y-6">
          <div className="bg-[#111] border border-white/5 p-6 rounded-2xl">
            <div className="flex items-center gap-3 mb-6">
              <Download className="w-5 h-5 text-cyan-500" />
              <h2 className="text-sm font-semibold uppercase tracking-wider italic text-white/80">Installation Protocol</h2>
            </div>
            
            <div className="space-y-4">
              {[
                { title: 'Terminal API', detail: 'Install Termux:API from F-Droid' },
                { title: 'System Prep', detail: 'pkg install python termux-api' },
                { title: 'Cloud Brain', detail: 'Add Gemini API Key to config.json' },
                { title: 'Launch', detail: 'python kyros.py' }
              ].map((step, idx) => (
                <div key={idx} className="flex gap-4 group">
                  <div className="flex flex-col items-center">
                    <div className="w-6 h-6 rounded-full border border-white/10 flex items-center justify-center text-[10px] font-mono group-hover:border-cyan-500/50 group-hover:text-cyan-500 transition-colors">
                      0{idx + 1}
                    </div>
                    {idx !== 3 && <div className="w-px h-full bg-white/5 my-2" />}
                  </div>
                  <div>
                    <h3 className="text-xs font-medium text-white/90">{step.title}</h3>
                    <p className="text-[10px] text-white/40 mt-0.5">{step.detail}</p>
                  </div>
                </div>
              ))}
            </div>
          </div>

          <div className="bg-[#111] border border-white/5 p-6 rounded-2xl group overflow-hidden relative">
            <div className="flex items-center gap-3 mb-6 relative z-10">
              <Smartphone className="w-5 h-5 text-emerald-500" />
              <h2 className="text-sm font-semibold uppercase tracking-wider italic text-white/80">Hardware Integration</h2>
            </div>
            
            <div className="grid grid-cols-2 gap-4 relative z-10">
              <div className="p-3 bg-white/5 rounded-xl border border-white/5">
                <p className="text-[9px] text-white/40 uppercase mb-1">Root Access</p>
                <div className="flex items-center gap-1.5 text-[11px] text-emerald-400 font-mono">
                  <AlertCircle className="w-3 h-3" /> NOT REQUIRED
                </div>
              </div>
              <div className="p-3 bg-white/5 rounded-xl border border-white/5">
                <p className="text-[9px] text-white/40 uppercase mb-1">Android API</p>
                <div className="flex items-center gap-1.5 text-[11px] text-cyan-400 font-mono">
                  <CheckCircle2 className="w-3 h-3" /> INTENT v2
                </div>
              </div>
            </div>
            
            {/* Aesthetic Grid Mask */}
            <div className="absolute inset-0 opacity-[0.03] pointer-events-none" style={{ background: 'linear-gradient(90deg, #fff 1px, transparent 0), linear-gradient(#fff 1px, transparent 0)', backgroundSize: '20px 20px' }} />
          </div>
        </div>

        {/* Right: Simulated Terminal */}
        <div className="lg:col-span-8 flex flex-col h-[700px]">
          <div className="bg-[#0a0a0a] border border-white/10 rounded-3xl flex flex-col flex-1 overflow-hidden shadow-2xl">
            {/* Terminal Top Bar */}
            <div className="border-b border-white/5 bg-[#111] py-3 px-6 flex items-center justify-between">
              <div className="flex items-center gap-2">
                <div className="w-2.5 h-2.5 rounded-full bg-red-500/20 border border-red-500/40" />
                <div className="w-2.5 h-2.5 rounded-full bg-yellow-500/20 border border-yellow-500/40" />
                <div className="w-2.5 h-2.5 rounded-full bg-green-500/20 border border-green-500/40" />
              </div>
              <div className="flex items-center gap-4 text-[10px] font-mono text-white/20 uppercase tracking-widest">
                <span>KYROS_SIMULATOR_CORE_v1.0.0</span>
                <span className="flex items-center gap-1"><History className="w-3 h-3" /> 12ms Response</span>
              </div>
            </div>

            {/* Terminal Body */}
            <div 
              ref={terminalRef}
              className="flex-1 overflow-y-auto p-8 scrollbar-hide bg-[radial-gradient(circle_at_top_right,rgba(6,182,212,0.05),transparent_40%)]"
            >
              <AnimatePresence>
                {terminalLines.map((line, i) => (
                  <TerminalLine key={i} text={line.text} type={line.type} />
                ))}
              </AnimatePresence>
            </div>

            {/* Intent Badge */}
            <AnimatePresence>
              {detectedIntent && (
                <motion.div 
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0 }}
                  className="mx-8 mb-4 px-4 py-3 bg-white/5 border border-white/10 rounded-xl flex items-center justify-between"
                >
                  <div className="flex items-center gap-3">
                    <div className="p-2 bg-white/5 rounded-lg border border-white/10">
                      {detectedIntent.icon}
                    </div>
                    <div>
                      <p className="text-[9px] text-white/40 uppercase font-mono mb-0.5">Parsed Intent detected</p>
                      <h4 className="text-xs font-bold text-white tracking-wide">{detectedIntent.type}</h4>
                    </div>
                  </div>
                  <div className="text-right">
                    <p className="text-[9px] text-white/40 uppercase font-mono mb-0.5">Payload Routing</p>
                    <p className="text-[10px] font-mono text-cyan-400">{detectedIntent.detail}</p>
                  </div>
                </motion.div>
              )}
            </AnimatePresence>

            {/* Input Bar */}
            <form onSubmit={handleCommand} className="p-6 border-t border-white/5 bg-[#0d0d0d]">
              <div className="relative group">
                <div className="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
                  <Command className="w-4 h-4 text-white/20 group-focus-within:text-cyan-500 transition-colors" />
                </div>
                <input 
                  type="text"
                  value={inputValue}
                  onChange={(e) => setInputValue(e.target.value)}
                  placeholder="Ask KYROS to automate something... (e.g. 'open youtube')"
                  className="w-full bg-white/5 border border-white/10 rounded-2xl py-4 pl-12 pr-12 text-sm focus:outline-none focus:ring-1 focus:ring-cyan-500/50 focus:border-cyan-500/50 transition-all font-mono placeholder:text-white/10"
                />
                <button 
                  type="submit"
                  className="absolute inset-y-2 right-2 px-4 bg-white/5 hover:bg-white/10 border border-white/10 rounded-xl flex items-center justify-center group/btn transition-colors"
                >
                  <Send className="w-4 h-4 text-white/40 group-hover/btn:text-cyan-500 transition-colors" />
                </button>
              </div>
              <div className="mt-4 flex items-center justify-between text-[9px] uppercase tracking-[0.2em] text-white/20 px-2 font-mono">
                <div className="flex gap-4">
                  <span>ESC to Clear</span>
                  <span>TAB for History</span>
                </div>
                <div className="flex items-center gap-1.5">
                  <div className="w-1.5 h-1.5 rounded-full bg-cyan-500 animate-pulse" />
                  Kernel Ready
                </div>
              </div>
            </form>
          </div>

          {/* Quick Shortcuts */}
          <div className="mt-6 flex flex-wrap gap-2">
            {[
              "search news on google",
              "send whatsapp to Rahul",
              "flashlight on",
              "create file logs.txt",
              "battery status"
            ].map(cmd => (
              <button 
                key={cmd}
                onClick={() => {
                  setInputValue(cmd);
                  // Optional: auto-trigger
                }}
                className="px-3 py-1.5 bg-white/5 hover:bg-white/10 border border-white/5 rounded-full text-[10px] text-white/40 hover:text-white/80 transition-all font-mono"
              >
                {cmd}
              </button>
            ))}
          </div>
        </div>
      </main>

      <footer className="max-w-7xl mx-auto p-12 mt-12 border-t border-white/5 flex flex-col items-center">
        <div className="flex gap-8 mb-8">
           <div className="text-center">
              <p className="text-[10px] text-white/30 uppercase tracking-[0.3em] font-mono mb-2">Automated</p>
              <h4 className="text-lg font-bold italic">500+ TASK HOOKS</h4>
           </div>
           <div className="w-px h-12 bg-white/5" />
           <div className="text-center">
              <p className="text-[10px] text-white/30 uppercase tracking-[0.3em] font-mono mb-2">Security</p>
              <h4 className="text-lg font-bold italic">SANDBOXED I/O</h4>
           </div>
           <div className="w-px h-12 bg-white/5" />
           <div className="text-center">
              <p className="text-[10px] text-white/30 uppercase tracking-[0.3em] font-mono mb-2">Latency</p>
              <h4 className="text-lg font-bold italic">0.05ms PARSING</h4>
           </div>
        </div>
        <p className="text-[10px] text-white/20 font-mono tracking-widest uppercase">
          Build for Android Termux Environment • 2026 KYROS Systems Inc.
        </p>
      </footer>
    </div>
  );
}
