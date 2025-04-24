
import React, { useState, useRef, useEffect } from "react";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { ArrowRight } from "lucide-react";

interface InputTerminalProps {
  onQuerySubmit: (query: string) => void;
  isLoading: boolean;
}

export const InputTerminal: React.FC<InputTerminalProps> = ({ onQuerySubmit, isLoading }) => {
  const [query, setQuery] = useState("");
  const inputRef = useRef<HTMLInputElement>(null);
  
  // Focus input on component mount
  useEffect(() => {
    if (inputRef.current) {
      inputRef.current.focus();
    }
  }, []);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (query.trim() && !isLoading) {
      onQuerySubmit(query);
      setQuery("");
    }
  };

  return (
    <form onSubmit={handleSubmit} className="relative">
      <div className="flex items-center">
        <span className="text-primary mr-2 font-mono">$</span>
        <div className="relative flex-grow">
          <Input
            ref={inputRef}
            type="text"
            className="pl-2 pr-12 font-mono bg-background/50 border-border focus-visible:ring-primary"
            placeholder="Ask for product recommendations..."
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            disabled={isLoading}
          />
          <div className="absolute right-2 top-1/2 -translate-y-1/2">
            <Button 
              type="submit" 
              size="icon" 
              variant="ghost" 
              className="h-7 w-7 text-primary"
              disabled={isLoading || !query.trim()}
            >
              <ArrowRight className="h-4 w-4" />
            </Button>
          </div>
        </div>
      </div>
      <p className="text-xs text-muted-foreground mt-2 font-mono">
        Try: "Need a good laptop for coding" or "Best headphones under 5000 KSH"
      </p>
    </form>
  );
};
