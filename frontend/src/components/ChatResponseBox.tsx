
import React, { useRef, useEffect } from "react";
import { Skeleton } from "@/components/ui/skeleton";

interface ChatResponseBoxProps {
  conversation: Array<{type: "user" | "ai"; message: string}>;
  isLoading: boolean;
}

export const ChatResponseBox: React.FC<ChatResponseBoxProps> = ({ conversation, isLoading }) => {
  const chatEndRef = useRef<HTMLDivElement>(null);

  // Auto scroll to bottom when conversation updates
  useEffect(() => {
    if (chatEndRef.current) {
      chatEndRef.current.scrollIntoView({ behavior: "smooth" });
    }
  }, [conversation]);

  return (
    <div className="max-h-96 overflow-y-auto space-y-4 font-mono">
      {conversation.map((entry, index) => (
        <div 
          key={index} 
          className={`flex ${entry.type === 'user' ? 'justify-end' : 'justify-start'}`}
        >
          <div 
            className={`${
              entry.type === 'user' 
                ? 'bg-secondary text-secondary-foreground rounded-tl-lg rounded-bl-lg rounded-br-lg' 
                : 'bg-muted text-foreground rounded-tr-lg rounded-bl-lg rounded-br-lg'
            } px-4 py-3 max-w-[85%] md:max-w-[70%]`}
          >
            {entry.type === 'user' ? (
              <span className="text-primary-foreground font-bold">&gt; </span>
            ) : (
              <span className="text-primary font-bold">&lt; </span>
            )}
            {entry.message}
          </div>
        </div>
      ))}
      
      {isLoading && (
        <div className="flex">
          <div className="bg-muted text-foreground rounded-tr-lg rounded-bl-lg rounded-br-lg px-4 py-3 max-w-[85%] md:max-w-[70%]">
            <span className="text-primary font-bold">&lt; </span>
            <Skeleton className="h-4 w-32 bg-muted-foreground/20 inline-block" />
            <div className="mt-2">
              <Skeleton className="h-4 w-64 bg-muted-foreground/20" />
              <Skeleton className="h-4 w-48 bg-muted-foreground/20 mt-1" />
              <Skeleton className="h-4 w-56 bg-muted-foreground/20 mt-1" />
            </div>
          </div>
        </div>
      )}
      
      <div ref={chatEndRef} />
    </div>
  );
};
