import React, { useState } from 'react';
import apiService, { RecommendationRequest, TipRequest, Product } from '@/lib/api';

const APITest: React.FC = () => {
  const [query, setQuery] = useState('');
  const [response, setResponse] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const testRecommendation = async () => {
    try {
      setLoading(true);
      setError(null);
      
      const request: RecommendationRequest = {
        query,
        context: null
      };
      
      const result = await apiService.getRecommendations(request);
      setResponse(result);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setLoading(false);
    }
  };

  const testTip = async () => {
    try {
      setLoading(true);
      setError(null);
      
      const request: TipRequest = {
        phone_number: '+254759325915',
        amount: 100
      };
      
      const result = await apiService.initiateTip(request);
      setResponse(result);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setLoading(false);
    }
  };

  const renderProduct = (product: Product) => (
    <div key={product.vendor_url} className="border rounded-lg p-4 mb-4">
      <div className="flex gap-4">
        <img 
          src={product.image_url} 
          alt={product.name}
          className="w-32 h-32 object-cover rounded"
        />
        <div className="flex-1">
          <h3 className="text-lg font-semibold">{product.name}</h3>
          <p className="text-gray-600 text-sm mb-2">{product.description}</p>
          <div className="flex items-center gap-2 mb-2">
            <span className="text-lg font-bold">
              {product.price.currency} {product.price.value.toFixed(2)}
            </span>
            <span className="text-sm text-gray-500">
              (Confidence: {(product.confidence_score * 100).toFixed(1)}%)
            </span>
          </div>
          {product.specs.length > 0 && (
            <div className="text-sm text-gray-600">
              <h4 className="font-semibold mb-1">Specifications:</h4>
              <ul className="list-disc list-inside">
                {product.specs.map((spec, index) => (
                  <li key={index}>
                    {spec.key}: {spec.value}
                  </li>
                ))}
              </ul>
            </div>
          )}
          <a 
            href={product.vendor_url}
            target="_blank"
            rel="noopener noreferrer"
            className="text-blue-500 hover:text-blue-700 text-sm mt-2 inline-block"
          >
            View on {new URL(product.vendor_url).hostname}
          </a>
        </div>
      </div>
    </div>
  );

  return (
    <div className="p-4 space-y-4">
      <h2 className="text-2xl font-bold">API Test Component</h2>
      
      <div className="space-y-2">
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Enter your query (e.g., 'cheap phone under $200')"
          className="w-full p-2 border rounded"
        />
        
        <div className="space-x-2">
          <button
            onClick={testRecommendation}
            disabled={loading}
            className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 disabled:opacity-50"
          >
            Test Recommendation
          </button>
          
          <button
            onClick={testTip}
            disabled={loading}
            className="px-4 py-2 bg-green-500 text-white rounded hover:bg-green-600 disabled:opacity-50"
          >
            Test M-Pesa Tip
          </button>
        </div>
      </div>

      {loading && (
        <div className="text-gray-600">Searching for products...</div>
      )}

      {error && (
        <div className="text-red-500">
          Error: {error}
        </div>
      )}

      {response && (
        <div className="mt-4">
          {response.clarification && (
            <div className="bg-yellow-50 border-l-4 border-yellow-400 p-4 mb-4">
              <p className="text-yellow-700">{response.clarification}</p>
            </div>
          )}
          
          {response.products && response.products.length > 0 ? (
            <div>
              <h3 className="text-xl font-semibold mb-4">
                Found {response.products.length} products
              </h3>
              <div className="space-y-4">
                {response.products.map(renderProduct)}
              </div>
            </div>
          ) : (
            <div className="text-gray-600">
              No products found. Try a different search query.
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default APITest; 