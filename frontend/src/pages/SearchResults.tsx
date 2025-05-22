import React, { useEffect, useState } from "react";
import { useLocation, Link, useNavigate } from "react-router-dom";
import { Search } from "lucide-react";
import GoogleLogo from "../components/Logo";
import { useIsMobile } from "../hooks/use-mobile";
import { useSearch } from "@/hooks/use-search";

const SearchResults = () => {
  const location = useLocation();
  const searchParams = new URLSearchParams(location.search);
  const query = searchParams.get("q") || "";
  const isMobile = useIsMobile();
  const [inputValue, setInputValue] = useState(query);
  const navigate = useNavigate();

  const handleSearch = (e?: React.FormEvent) => {
    e?.preventDefault();
    if (inputValue.trim()) {
      navigate(`/search?q=${encodeURIComponent(inputValue.trim())}`);
    }
  };

  const {
    results,
    loading,
    error,
    search,
    page,
    setPage,
    limit,
    total,
    time,
  } = useSearch();

  // Gọi API khi query thay đổi
  useEffect(() => {
    if (query) {
      search(query, 1); // reset về trang 1 khi query mới
    }
  }, [query]);

  // Gọi API khi trang thay đổi (với cùng query)
  useEffect(() => {
    if (query) {
      search(query, page);
    }
  }, [query, page]);

  const totalPages = Math.ceil(total / limit);

  return (
    <div className="min-h-screen flex flex-col">
      {/* Header with search bar */}
      <div className="border-b pb-4">
        <div className="container mx-auto px-4 py-3 flex items-center">
          <Link to="/" className="mr-8">
            <GoogleLogo small />
          </Link>

          <div className="flex-1">
            <div className="relative flex items-center max-w-2xl ml-0">
              <form
                onSubmit={handleSearch}
                className="relative flex items-center max-w-2xl ml-0 w-full"
              >
                <input
                  type="text"
                  value={inputValue}
                  onChange={(e) => setInputValue(e.target.value)}
                  className="w-full py-2 pl-4 pr-10 border border-gray-200 rounded-full shadow-sm hover:shadow-md focus:shadow-md focus:outline-none"
                />
                <button type="submit" className="absolute right-3 text-blue-500">
                  <Search size={18} />
                </button>
              </form>
            </div>
          </div>
        </div>
      </div>

      {/* Search results */}
      <main className="flex-1">
        <div className="container mx-auto px-4 py-4">
          <div className={`max-w-2xl  ${isMobile ? "ml-0" : "ml-40"}`}>
            <h1 className="text-2xl font-bold mb-4">Kết quả tìm kiếm cho: {query}</h1>
            <p className="text-sm text-gray-500 mb-5">About {total} results ({time}s)</p>

            {/* Xử lý loading */}
            {loading ? (
              <div className="flex justify-center items-center h-40">
                <svg
                  className="animate-spin h-8 w-8 text-blue-500"
                  xmlns="http://www.w3.org/2000/svg"
                  fill="none"
                  viewBox="0 0 24 24"
                >
                  <circle
                    className="opacity-25"
                    cx="12"
                    cy="12"
                    r="10"
                    stroke="currentColor"
                    strokeWidth="4"
                  ></circle>
                  <path
                    className="opacity-75"
                    fill="currentColor"
                    d="M4 12a8 8 0 018-8v4a4 4 0 00-4 4H4z"
                  ></path>
                </svg>
              </div>
            ) : error ? (
              <p className="text-red-500">Có lỗi xảy ra: {error}</p>
            ) : results.length === 0 ? (
              <p className="text-gray-500">Không tìm thấy kết quả nào phù hợp.</p>
            ) : (
              <div className="space-y-6">
                {results.map((result, index) => (
                  <div key={index} className="max-w-2xl">
                    <div className="text-xs text-gray-600 mb-1">{result.url}</div>
                    <a
                      href={result.url}
                      className="text-xl text-blue-800 hover:underline font-medium block mb-1"
                    >
                      {result.title}
                    </a>
                    <p className="text-sm text-gray-700 mb-2">{result.snippet}</p>

                    {result.categories && (
                      <div className="flex flex-wrap gap-2 mt-2">
                        {result.categories.map((cat, i) => (
                          <span key={i} className="text-xs text-blue-600 hover:underline">
                            {cat}
                          </span>
                        ))}
                      </div>
                    )}
                  </div>
                ))}
              </div>
            )}

            {/* Pagination */}
            {!loading && results.length > 0 && (
              <div className="flex justify-center mt-8">
                <nav className="flex items-center gap-1">
                  <button
                    onClick={() => setPage((prev) => Math.max(prev - 1, 1))}
                    disabled={page === 1}
                    className="px-3 py-1 rounded hover:bg-gray-100 disabled:opacity-50"
                  >
                    Previous
                  </button>

                  {Array.from({ length: Math.min(5, totalPages) }, (_, i) => {
                    const pageNum =
                      page <= 3
                        ? i + 1
                        : page >= totalPages - 2
                        ? totalPages - 4 + i
                        : page - 2 + i;

                    if (pageNum < 1 || pageNum > totalPages) return null;

                    return (
                      <button
                        key={pageNum}
                        onClick={() => setPage(pageNum)}
                        className={`px-3 py-1 rounded ${
                          page === pageNum ? "bg-blue-100 text-blue-800" : "hover:bg-gray-100"
                        }`}
                      >
                        {pageNum}
                      </button>
                    );
                  })}

                  <button
                    onClick={() => setPage((prev) => Math.min(prev + 1, totalPages))}
                    disabled={page === totalPages}
                    className="px-3 py-1 rounded hover:bg-gray-100 disabled:opacity-50"
                  >
                    Next
                  </button>
                </nav>
              </div>
            )}
          </div>
        </div>
      </main>
    </div>
  );
};

export default SearchResults;
