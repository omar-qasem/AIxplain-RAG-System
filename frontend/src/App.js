import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css'; // Assuming Tailwind CSS is imported here

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8001';

function App() {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [searched, setSearched] = useState(false);
  const [stats, setStats] = useState({ documents: 2287 }); // Default to 2287 as seen in the image

  useEffect(() => {
    // Fetch health stats on mount
    axios.get(`${BACKEND_URL}/api/health`)
      .then(res => setStats({ documents: res.data.documents_loaded }))
      .catch(err => {
        console.error("Error fetching health data:", err);
        // Keep default value if fetch fails
      });
  }, []);

  const handleSearch = async () => {
    if (!query.trim()) {
      setError('Please enter a search query');
      return;
    }

    setLoading(true);
    setError('');
    setSearched(true);
    setResults([]);

    try {
      const response = await axios.post(`${BACKEND_URL}/api/search`, {
        query: query,
        top_k: 5
      });

      setResults(response.data);
    } catch (err) {
      setError(err.response?.data?.detail || 'An error occurred while searching. Check if the backend is running and data is loaded.');
      setResults([]);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyPress = (event) => {
    if (event.key === 'Enter') {
      handleSearch();
    }
  };

  // Helper component for the gradient text
  const GradientText = ({ children, className = '' }) => (
    <span className={`bg-clip-text text-transparent bg-gradient-to-r from-green-400 to-blue-500 ${className}`}>
      {children}
    </span>
  );

  return (
    <div className="min-h-screen bg-black text-white relative overflow-hidden">
      {/* Background Grid and Gradient Border - Simplified for Tailwind */}
      <div className="absolute inset-0 z-0 opacity-10" style={{ backgroundImage: 'repeating-linear-gradient(0deg, #1f2937 0, #1f2937 1px, transparent 1px, transparent 50px), repeating-linear-gradient(90deg, #1f2937 0, #1f2937 1px, transparent 1px, transparent 50px)' }}></div>
      <div className="absolute inset-0 z-10 pointer-events-none" style={{
        border: '3px solid',
        borderImageSource: 'linear-gradient(to right, #00ff00, #00ffff)',
        borderImageSlice: 1,
        borderImageWidth: '0 0 3px 0',
        boxShadow: '0 0 50px rgba(0, 255, 255, 0.2)'
      }}></div>

      <div className="relative z-20 container mx-auto px-4 py-8">
        {/* Header and Document Count */}
        <header className="flex justify-between items-start mb-20">
          <div>
            <h1 className="text-3xl font-bold">
              <GradientText className="from-green-400 to-green-600">RAG System</GradientText>
            </h1>
            <p className="text-sm text-gray-400">Government Regulations & AI Governance</p>
          </div>
          <div className="text-center p-3 rounded-xl bg-green-900 bg-opacity-30 border border-green-500 shadow-lg" style={{ boxShadow: '0 0 15px rgba(0, 255, 0, 0.5)' }}>
            <p className="text-2xl font-bold text-green-400">{stats.documents.toLocaleString()}</p>
            <p className="text-xs text-green-600">DOCUMENTS</p>
          </div>
        </header>

        {/* Main Search Area */}
        <main className="flex flex-col items-center pt-20">
          <h2 className="text-7xl font-extrabold mb-4">
            The <GradientText className="from-green-400 to-blue-500">Intelligent Search</GradientText>
          </h2>
          <p className="text-xl font-semibold mb-8">
            for <GradientText className="from-green-400 to-green-600">Regulatory Intelligence</GradientText>
          </p>
          <p className="text-center text-gray-400 max-w-xl mb-16">
            Everything you need to search, retrieve, and analyze government regulations and AI governance documents at scale, with zero friction.
          </p>

          {/* Search Input */}
          <div className="w-full max-w-3xl flex p-1 rounded-full border-2" style={{
            background: 'linear-gradient(to right, #00ff00, #00ffff)',
            padding: '2px', // Simulating the border effect
          }}>
            <div className="flex flex-grow bg-black rounded-full p-1">
              <input
                type="text"
                className="flex-grow bg-transparent text-white placeholder-gray-500 px-6 py-4 text-lg focus:outline-none"
                placeholder="Search regulations, standards, governance documents..."
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                onKeyPress={handleKeyPress}
                disabled={loading}
              />
              <button
                onClick={handleSearch}
                className="flex items-center justify-center px-8 py-4 rounded-full text-lg font-semibold transition-all duration-300"
                style={{
                  background: 'linear-gradient(to right, #00ff00, #00ffff)',
                  color: 'black',
                  boxShadow: '0 0 10px rgba(0, 255, 255, 0.5)',
                }}
                disabled={loading}
              >
                {loading ? (
                  <svg className="animate-spin h-5 w-5 text-black" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                ) : (
                  <>
                    <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 mr-2" viewBox="0 0 20 20" fill="currentColor">
                      <path fillRule="evenodd" d="M8 4a4 4 0 100 8 4 4 0 000-8zM2 8a6 6 0 1110.89 3.476l4.817 4.817a1 1 0 01-1.414 1.414l-4.816-4.816A6 6 0 012 8z" clipRule="evenodd" />
                    </svg>
                    Search
                  </>
                )}
              </button>
            </div>
          </div>

          {/* Error Message */}
          {error && (
            <p className="mt-8 text-red-500 p-4 bg-red-900 bg-opacity-30 rounded-lg max-w-3xl w-full text-center border border-red-500">
              {error}
            </p>
          )}

          {/* Search Results */}
          {searched && !loading && results.length > 0 && (
            <div className="mt-16 w-full max-w-5xl">
              <h3 className="text-2xl font-bold mb-6">
                <GradientText>Top {results.length} Results</GradientText>
              </h3>
              <div className="space-y-6">
                {results.map((doc, index) => (
                  <div key={index} className="p-6 rounded-xl bg-gray-900 border border-gray-700 shadow-lg hover:border-green-500 transition-all duration-300">
                    <div className="flex justify-between items-start mb-3">
                      <h4 className="text-xl font-semibold text-green-400">{doc.source}</h4>
                      <a href={doc.url} target="_blank" rel="noopener noreferrer" className="text-blue-400 hover:text-blue-300 text-sm flex items-center">
                        View Document
                        <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4 ml-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
                        </svg>
                      </a>
                    </div>
                    <p className="text-gray-300 leading-relaxed line-clamp-4">{doc.content}</p>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* No Results Message */}
          {searched && !loading && results.length === 0 && !error && (
            <p className="mt-16 text-gray-500 text-xl">No documents found for your query. Try a different search term.</p>
          )}
        </main>
      </div>
    </div>
  );
}

export default App;
