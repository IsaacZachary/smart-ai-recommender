
import { useState } from "react";
import { Link, useLocation } from "react-router-dom";
import { Menu, Terminal, X } from "lucide-react";
import { Button } from "@/components/ui/button";

export const Navbar = () => {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const location = useLocation();
  
  const isActive = (path: string) => location.pathname === path;

  return (
    <nav className="sticky top-0 z-50 w-full bg-card/50 backdrop-blur-xl border-b border-border">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          <div className="flex items-center">
            <Link to="/" className="flex items-center gap-2 text-xl font-bold text-primary">
              <Terminal className="h-6 w-6" />
              <span className="font-mono">terminal_ai</span>
            </Link>
          </div>

          {/* Desktop Navigation */}
          <div className="hidden md:flex items-center space-x-4">
            <Link 
              to="/recommendations" 
              className={`${isActive('/recommendations') ? 'text-primary' : 'text-foreground'} hover:text-primary font-mono`}
            >
              /recommendations
            </Link>
            <Link 
              to="/transactions" 
              className={`${isActive('/transactions') ? 'text-primary' : 'text-foreground'} hover:text-primary font-mono`}
            >
              /transactions
            </Link>
          </div>

          {/* Mobile menu button */}
          <div className="md:hidden">
            <Button variant="ghost" size="icon" onClick={() => setIsMenuOpen(!isMenuOpen)}>
              {isMenuOpen ? <X className="h-6 w-6" /> : <Menu className="h-6 w-6" />}
            </Button>
          </div>
        </div>

        {/* Mobile Navigation */}
        {isMenuOpen && (
          <div className="md:hidden">
            <div className="px-2 pt-2 pb-3 space-y-1 sm:px-3">
              <Link
                to="/recommendations"
                className={`block px-3 py-2 ${isActive('/recommendations') ? 'text-primary' : 'text-foreground'} hover:text-primary font-mono`}
                onClick={() => setIsMenuOpen(false)}
              >
                /recommendations
              </Link>
              <Link
                to="/transactions"
                className={`block px-3 py-2 ${isActive('/transactions') ? 'text-primary' : 'text-foreground'} hover:text-primary font-mono`}
                onClick={() => setIsMenuOpen(false)}
              >
                /transactions
              </Link>
            </div>
          </div>
        )}
      </div>
    </nav>
  );
};
