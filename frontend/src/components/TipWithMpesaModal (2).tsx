
import React, { useState } from "react";
import { Dialog, DialogContent, DialogDescription, DialogFooter, DialogHeader, DialogTitle } from "@/components/ui/dialog";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { toast } from "sonner";

interface TipWithMpesaModalProps {
  isOpen: boolean;
  onClose: () => void;
}

export const TipWithMpesaModal: React.FC<TipWithMpesaModalProps> = ({ isOpen, onClose }) => {
  const [phoneNumber, setPhoneNumber] = useState("");
  const [amount, setAmount] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!phoneNumber.trim() || !amount.trim() || isNaN(Number(amount))) {
      toast.error("Please provide a valid phone number and amount");
      return;
    }

    setIsSubmitting(true);
    
    try {
      // This would be an actual API call to your Express backend
      await new Promise(resolve => setTimeout(resolve, 2000));
      
      toast.success(`M-Pesa STK Push initiated! Check your phone ${phoneNumber} to complete the transaction.`);
      onClose();
      
      // Reset form
      setPhoneNumber("");
      setAmount("");
    } catch (error) {
      toast.error("Failed to initiate payment. Please try again.");
      console.error("Payment error:", error);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <Dialog open={isOpen} onOpenChange={onClose}>
      <DialogContent className="sm:max-w-[425px] bg-card">
        <DialogHeader>
          <DialogTitle className="text-primary font-mono">$ support_free_tool()</DialogTitle>
          <DialogDescription className="font-mono">
            Your appreciation helps maintain this free tool. No obligation!
          </DialogDescription>
        </DialogHeader>
        
        <form onSubmit={handleSubmit}>
          <div className="space-y-4 py-4">
            <div className="space-y-2">
              <label htmlFor="phone" className="text-sm font-medium font-mono">
                M-Pesa Phone Number
              </label>
              <Input
                id="phone"
                type="tel"
                placeholder="254XXXXXXXXX"
                value={phoneNumber}
                onChange={(e) => setPhoneNumber(e.target.value)}
                disabled={isSubmitting}
                className="font-mono"
              />
            </div>
            
            <div className="space-y-2">
              <label htmlFor="amount" className="text-sm font-medium font-mono">
                Amount (KSh)
              </label>
              <Input
                id="amount"
                type="number"
                placeholder="100"
                min="10"
                value={amount}
                onChange={(e) => setAmount(e.target.value)}
                disabled={isSubmitting}
                className="font-mono"
              />
            </div>
          </div>
          
          <DialogFooter>
            <Button variant="outline" onClick={onClose} disabled={isSubmitting}>
              Cancel
            </Button>
            <Button type="submit" disabled={isSubmitting}>
              {isSubmitting ? "Processing..." : "Send Tip"}
            </Button>
          </DialogFooter>
        </form>
      </DialogContent>
    </Dialog>
  );
};
