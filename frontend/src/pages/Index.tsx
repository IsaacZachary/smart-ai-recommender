
import { Button } from "@/components/ui/button";
import { Link } from "react-router-dom";

const Index = () => {
  return (
    <div className="min-h-screen">
      <main>
        {/* Hero Section */}
        <section className="relative py-20 bg-gradient-to-b from-secondary/10 to-background">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="text-center space-y-6">
              <h1 className="inline-flex items-center text-4xl sm:text-5xl md:text-6xl font-bold text-foreground">
                <span className="text-primary mr-2">&gt;</span>
                <span className="terminal-cursor">AI Product Recommender_</span>
              </h1>
              <p className="text-xl text-muted-foreground font-mono max-w-2xl mx-auto">
                [system]: Intelligent product recommendations powered by advanced AI algorithms. 
                Seamless M-Pesa integration for instant purchases.
              </p>
              <div className="flex justify-center gap-4">
                <Button size="lg" variant="default" asChild className="font-mono">
                  <Link to="/recommendations">$ get-recommendations</Link>
                </Button>
                <Button size="lg" variant="secondary" asChild className="font-mono">
                  <Link to="/transactions">$ view-transactions</Link>
                </Button>
              </div>
            </div>
          </div>
        </section>

        {/* Features Section */}
        <section className="py-16">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="grid md:grid-cols-3 gap-8">
              <div className="p-6 bg-card rounded border border-border">
                <h3 className="text-xl font-semibold mb-3 text-primary">&gt; smart_recommend()</h3>
                <p className="text-muted-foreground">
                  AI-powered suggestions based on advanced algorithms and data analysis.
                </p>
              </div>
              <div className="p-6 bg-card rounded border border-border">
                <h3 className="text-xl font-semibold mb-3 text-primary">&gt; mpesa_pay()</h3>
                <p className="text-muted-foreground">
                  Quick and secure payments using M-Pesa mobile money service.
                </p>
              </div>
              <div className="p-6 bg-card rounded border border-border">
                <h3 className="text-xl font-semibold mb-3 text-primary">&gt; fetch_history()</h3>
                <p className="text-muted-foreground">
                  Complete transaction logs and payment history tracking.
                </p>
              </div>
            </div>
          </div>
        </section>
      </main>
    </div>
  );
};

export default Index;
