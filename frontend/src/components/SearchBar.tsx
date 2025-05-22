
import React, { useState } from "react";
import { Search, Mic } from "lucide-react";
import { useNavigate } from "react-router-dom";

const SearchBar = () => {
  const [searchQuery, setSearchQuery] = useState("");
  const navigate = useNavigate();

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    if (searchQuery.trim()) {
      console.log("Search query:", searchQuery);
      navigate(`/search?q=${encodeURIComponent(searchQuery.trim())}`);
    }
  };

  return (
    <div className="w-full max-w-2xl mx-auto px-4">
      <form onSubmit={handleSearch}>
        <div className="relative flex items-center w-full">
          <div className="absolute left-4 text-gray-500">
            <Search size={18} />
          </div>
          
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full py-3 pl-12 pr-10 border border-gray-200 rounded-full hover:shadow-md focus:shadow-md focus:outline-none transition-shadow duration-200"
            aria-label="Search"
          />
          
          {searchQuery && (
            <button
              type="button"
              onClick={() => setSearchQuery("")}
              className="absolute right-16 text-gray-500 hover:text-gray-700"
              aria-label="Clear search"
            >
              <span className="text-xl font-light">×</span>
            </button>
          )}
          
          <button
            type="button"
            className="absolute right-4 text-blue-500 hover:text-blue-600"
            aria-label="Voice search"
          >
            <Mic size={18} />
          </button>
        </div>
        
        <div className="flex justify-center mt-6">
          <button
            type="submit"
            className="px-4 py-2 bg-gray-200 hover:bg-gray-300 text-sm text-gray-700 rounded-md"
          >
            Vietnamnet Search
          </button>
        </div>
      </form>
    </div>
  );
};

export default SearchBar;
