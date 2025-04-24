
import React from "react";
import { ProductCard } from "@/components/ProductCard";

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

interface ProductGridProps {
  products: Product[];
}

export const ProductGrid: React.FC<ProductGridProps> = ({ products }) => {
  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
      {products.map(product => (
        <ProductCard key={product.id} product={product} />
      ))}
    </div>
  );
};
