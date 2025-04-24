
import React, { useState, useEffect } from "react";
import { toast } from "sonner";
import { Terminal } from "lucide-react";
import { InputTerminal } from "@/components/InputTerminal";
import { ChatResponseBox } from "@/components/ChatResponseBox";
import { ProductGrid } from "@/components/ProductGrid";
import { TipWithMpesaModal } from "@/components/TipWithMpesaModal";
import { ThemeToggle } from "@/components/ThemeToggle";
import { Button } from "@/components/ui/button";

const Recommendations = () => {
  const [query, setQuery] = useState("");
  const [conversation, setConversation] = useState<Array<{type: "user" | "ai", message: string}>>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [products, setProducts] = useState<Product[]>([]);
  const [showTipModal, setShowTipModal] = useState(false);

  // Handle user query submission
  const handleQuerySubmit = async (input: string) => {
    if (!input.trim()) return;
    
    setIsLoading(true);
    // Add user message to conversation
    setConversation(prev => [...prev, { type: "user", message: input }]);
    
    try {
      // Simulate API call to the recommendation engine
      await new Promise(resolve => setTimeout(resolve, 1500));
      
      // Simulate AI response
      const aiResponse = generateAIResponse(input);
      setConversation(prev => [...prev, { type: "ai", message: aiResponse }]);
      
      // Simulate fetching product recommendations
      const recommendedProducts = await fetchMockProducts(input);
      setProducts(recommendedProducts);
      
      toast.success("Recommendations loaded successfully");
    } catch (error) {
      console.error("Error fetching recommendations:", error);
      toast.error("Failed to get recommendations. Please try again.");
      setConversation(prev => [
        ...prev, 
        { type: "ai", message: "I'm having trouble processing that request. Could you try again?" }
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="container mx-auto px-4 py-8 max-w-7xl">
      <div className="flex justify-between items-center mb-8">
        <div className="flex items-center">
          <Terminal className="h-6 w-6 text-primary mr-2" />
          <h1 className="text-xl font-mono font-bold text-primary">&gt; product_recommender</h1>
        </div>
        <ThemeToggle />
      </div>

      <div className="space-y-8">
        <section className="bg-card rounded-lg p-6 border border-border">
          <h2 className="text-primary mb-4 font-mono">&gt; input_query</h2>
          <InputTerminal 
            onQuerySubmit={handleQuerySubmit} 
            isLoading={isLoading} 
          />
        </section>

        {conversation.length > 0 && (
          <section className="bg-card rounded-lg p-6 border border-border">
            <h2 className="text-primary mb-4 font-mono">&gt; conversation_log</h2>
            <ChatResponseBox conversation={conversation} isLoading={isLoading} />
          </section>
        )}

        {products.length > 0 && (
          <>
            <section className="bg-card rounded-lg p-6 border border-border">
              <div className="flex justify-between items-center mb-4">
                <h2 className="text-primary font-mono">&gt; recommendations</h2>
                <Button 
                  variant="outline" 
                  onClick={() => setShowTipModal(true)}
                  className="font-mono text-sm"
                >
                  $ tip_with_mpesa()
                </Button>
              </div>
              <ProductGrid products={products} />
            </section>
          </>
        )}
      </div>

      <TipWithMpesaModal 
        isOpen={showTipModal} 
        onClose={() => setShowTipModal(false)}
      />
    </div>
  );
};

// Mock functions to simulate backend interaction
const generateAIResponse = (query: string): string => {
  const responses = [
    `Based on your search for "${query}", I've found some great options that might interest you. Here are my top recommendations:`,
    `I analyzed your request for "${query}" and found several products that match your criteria. Take a look at these options:`,
    `Looking for "${query}"? I've curated some excellent choices based on quality, price, and user reviews:`,
  ];
  return responses[Math.floor(Math.random() * responses.length)];
};

const fetchMockProducts = async (query: string): Promise<Product[]> => {
  // This would be replaced with an actual API call
  const mockProducts: Product[] = [
    {
      id: "1",
      name: "Premium Laptop Pro",
      description: "High-performance laptop with 16GB RAM, 512GB SSD, and dedicated graphics",
      price: 129999,
      rating: 4.7,
      image: "https://placehold.co/300x200",
      vendor: "TechStore",
      vendorUrl: "https://example.com/product-1"
    },
    {
      id: "2",
      name: "Wireless Noise-Cancelling Headphones",
      description: "Studio-quality sound with 30-hour battery life and premium comfort",
      price: 24999,
      rating: 4.9,
      image: "https://placehold.co/300x200",
      vendor: "AudioWorld",
      vendorUrl: "https://example.com/product-2"
    },
    {
      id: "3",
      name: "Smart Home Hub",
      description: "Control all your smart devices from one central interface with voice commands",
      price: 15999,
      rating: 4.5,
      image: "https://placehold.co/300x200",
      vendor: "SmartLife",
      vendorUrl: "https://example.com/product-3"
    },
    {
      id: "4",
      name: "4K Ultra HD Smart TV",
      description: "55-inch display with vibrant colors and smart streaming capabilities",
      price: 59999,
      rating: 4.6,
      image: "https://placehold.co/300x200",
      vendor: "ViewMax",
      vendorUrl: "https://example.com/product-4"
    },
  ];
  
  return mockProducts;
};

// Product type definition
interface Product {
  id: string;
  name: string;
  description: string;
  price: number;
  rating: number;
  image: string;
  vendor: string;
  vendorUrl: string;
}

export default Recommendations;
