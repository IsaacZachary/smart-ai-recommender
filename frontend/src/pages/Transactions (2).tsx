
import React, { useState, useEffect } from "react";
import { Terminal } from "lucide-react";
import { toast } from "sonner";
import { Button } from "@/components/ui/button";
import { Table, TableHeader, TableRow, TableHead, TableBody, TableCell } from "@/components/ui/table";
import { Skeleton } from "@/components/ui/skeleton";
import { ThemeToggle } from "@/components/ThemeToggle";

interface Transaction {
  id: string;
  phoneNumber: string;
  amount: number;
  status: "completed" | "pending" | "failed";
  createdAt: string;
}

const Transactions = () => {
  const [transactions, setTransactions] = useState<Transaction[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchTransactions = async () => {
      setIsLoading(true);
      setError(null);
      
      try {
        // This would be replaced with an actual API call
        // const response = await axios.get("/transactions");
        // setTransactions(response.data);
        
        // For now, use mock data
        await new Promise(resolve => setTimeout(resolve, 1500));
        setTransactions(generateMockTransactions());
      } catch (err) {
        console.error("Failed to fetch transactions:", err);
        setError("Failed to load transactions. Please try again later.");
        toast.error("Could not load transaction history");
      } finally {
        setIsLoading(false);
      }
    };
    
    fetchTransactions();
  }, []);
  
  const formatDate = (dateString: string): string => {
    return new Date(dateString).toLocaleString();
  };
  
  const formatAmount = (amount: number): string => {
    return `KSh ${amount.toFixed(2)}`;
  };
  
  const getStatusClass = (status: string): string => {
    switch(status) {
      case "completed": return "text-green-500";
      case "pending": return "text-yellow-500";
      case "failed": return "text-red-500";
      default: return "";
    }
  };

  return (
    <div className="container mx-auto px-4 py-8 max-w-7xl">
      <div className="flex justify-between items-center mb-8">
        <div className="flex items-center">
          <Terminal className="h-6 w-6 text-primary mr-2" />
          <h1 className="text-xl font-mono font-bold text-primary">&gt; transaction_history</h1>
        </div>
        <ThemeToggle />
      </div>
      
      <div className="bg-card rounded-lg p-6 border border-border">
        <h2 className="text-primary mb-4 font-mono">&gt; m-pesa_logs</h2>
        
        {isLoading ? (
          <div className="space-y-4">
            <div className="flex items-center space-x-4">
              <Skeleton className="h-4 w-1/4" />
              <Skeleton className="h-4 w-1/4" />
              <Skeleton className="h-4 w-1/4" />
              <Skeleton className="h-4 w-1/4" />
            </div>
            {[...Array(5)].map((_, i) => (
              <div key={i} className="flex items-center space-x-4">
                <Skeleton className="h-12 w-full" />
              </div>
            ))}
          </div>
        ) : error ? (
          <div className="text-center py-8">
            <p className="text-muted-foreground mb-4">{error}</p>
            <Button 
              onClick={() => window.location.reload()} 
              variant="outline"
              className="font-mono"
            >
              $ retry()
            </Button>
          </div>
        ) : transactions.length === 0 ? (
          <div className="text-center py-8">
            <p className="text-muted-foreground font-mono">No transaction history found.</p>
            <p className="text-sm text-muted-foreground mt-2 font-mono">
              Support the tool with M-Pesa to see transactions here.
            </p>
          </div>
        ) : (
          <div className="overflow-x-auto">
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead className="font-mono">Transaction ID</TableHead>
                  <TableHead className="font-mono">Phone Number</TableHead>
                  <TableHead className="font-mono">Amount</TableHead>
                  <TableHead className="font-mono">Status</TableHead>
                  <TableHead className="font-mono">Date</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {transactions.map((transaction) => (
                  <TableRow key={transaction.id}>
                    <TableCell className="font-mono text-xs">{transaction.id}</TableCell>
                    <TableCell className="font-mono">{transaction.phoneNumber}</TableCell>
                    <TableCell className="font-mono">{formatAmount(transaction.amount)}</TableCell>
                    <TableCell className={`font-mono ${getStatusClass(transaction.status)}`}>
                      {transaction.status}
                    </TableCell>
                    <TableCell className="font-mono">{formatDate(transaction.createdAt)}</TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </div>
        )}
      </div>
    </div>
  );
};

// Mock data generator
const generateMockTransactions = (): Transaction[] => {
  const statuses: ("completed" | "pending" | "failed")[] = ["completed", "pending", "failed"];
  
  return Array.from({ length: 10 }, (_, i) => ({
    id: `TX${Math.random().toString(36).substring(2, 10).toUpperCase()}`,
    phoneNumber: `254${Math.floor(Math.random() * 900000000) + 100000000}`,
    amount: Math.floor(Math.random() * 1000) + 50,
    status: statuses[Math.floor(Math.random() * statuses.length)],
    createdAt: new Date(Date.now() - Math.floor(Math.random() * 30) * 24 * 60 * 60 * 1000).toISOString()
  }));
};

export default Transactions;
