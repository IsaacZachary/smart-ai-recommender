
import React from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { ArrowRight } from "lucide-react";

interface ProductProps {
  product: {
    id: string;
    name: string;
    description: string;
    price: number;
    rating: number;
    image: string;
    vendor: string;
    vendorUrl: string;
  };
}

export const ProductCard: React.FC<ProductProps> = ({ product }) => {
  const formatPrice = (price: number): string => {
    return `KSh ${(price / 100).toFixed(2).replace(/\.00$/, '')}`;
  };

  return (
    <Card className="transition-all hover:border-primary overflow-hidden h-full flex flex-col bg-card/60 backdrop-blur">
      <div className="aspect-w-16 aspect-h-9 overflow-hidden bg-muted w-full">
        <img 
          src={product.image} 
          alt={product.name} 
          className="w-full h-full object-cover"
        />
      </div>
      
      <CardHeader className="p-4">
        <CardTitle className="text-base font-mono">{product.name}</CardTitle>
        <CardDescription className="text-xs font-mono flex items-center mt-1">
          <span className="flex items-center">
            {Array(5).fill(0).map((_, i) => (
              <span key={i} className={`text-xs ${i < Math.floor(product.rating) ? 'text-primary' : 'text-muted-foreground'}`}>★</span>
            ))}
            <span className="ml-1 text-muted-foreground">({product.rating})</span>
          </span>
          <span className="ml-auto font-mono text-primary font-semibold">
            {formatPrice(product.price)}
          </span>
        </CardDescription>
      </CardHeader>
      
      <CardContent className="p-4 pt-0 flex-grow">
        <p className="text-sm text-muted-foreground font-mono line-clamp-3">
          {product.description}
        </p>
      </CardContent>
      
      <CardFooter className="p-4 pt-0">
        <Button asChild variant="outline" className="w-full font-mono text-xs sm:text-sm">
          <a href={product.vendorUrl} target="_blank" rel="noopener noreferrer" className="flex items-center justify-between">
            <span>View on {product.vendor}</span>
            <ArrowRight className="h-4 w-4 ml-2" />
          </a>
        </Button>
      </CardFooter>
    </Card>
  );
};
