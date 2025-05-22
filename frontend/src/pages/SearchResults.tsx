import React, { useState } from "react";
import { useLocation, Link } from "react-router-dom";
import { Search } from "lucide-react";
import GoogleLogo from "../components/Logo";
import { useIsMobile } from "../hooks/use-mobile";
const SearchResults = () => {
  const location = useLocation();
  const searchParams = new URLSearchParams(location.search);
  const query = searchParams.get("q") || "";
  const [currentPage, setCurrentPage] = useState(1);
  const resultsPerPage = 5;
  const isMobile = useIsMobile();
  // Mock search results
  const allResults = [
    {
      title: "Thị tức 24h",
      url: "https://www.24h.com.vn/bong-da",
      description: "Tin bóng đá mới nhất: Real Madrid tính toán mua Nico Williams, canh bạc chuyển nhượng thời Alonso...",
      categories: ["Bóng đá Việt Nam", "LỊCH THI ĐẤU BÓNG ĐÁ", "Điểm tin bóng đá", "Thể thao"]
    },
    {
      title: "Bongdaphus.vn: Tạp chí Bóng Đá, Báo Bóng Đá, kết quả, lịch...",
      url: "https://bongdaphus.vn",
      description: "Cập nhật tiền tực 24h tin tức, lịch thi đấu, TRỰC TIẾP kết quả, tỷ lệ, soi kéo, video clip..."
      
    },
    // Thêm nhiều kết quả mẫu khác ở đây...
    ...Array(15).fill(null).map((_, i) => ({
      title: `Kết quả bổ sung ${i + 1}`,
      url: `https://example.com/result-${i + 1}`,
      description: `Mô tả cho kết quả bổ sung ${i + 1} về chủ đề ${query}`
    }))
  ];

  // Tính toán kết quả hiển thị trên trang hiện tại
  const indexOfLastResult = currentPage * resultsPerPage;
  const indexOfFirstResult = indexOfLastResult - resultsPerPage;
  const currentResults = allResults.slice(indexOfFirstResult, indexOfLastResult);
  const totalPages = Math.ceil(allResults.length / resultsPerPage);

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
              <input
                type="text"
                defaultValue={query}
                className="w-full py-2 pl-4 pr-10 border border-gray-200 rounded-full shadow-sm hover:shadow-md focus:shadow-md focus:outline-none"
              />
              <button className="absolute right-3 text-blue-500">
                <Search size={18} />
              </button>
            </div>
          </div>
        </div>
      </div>
      
      {/* Search results */}
      <main className="flex-1">
        <div className="container mx-auto px-4 py-4">
          <div className={`max-w-2xl  ${isMobile ? "ml-0" : "ml-24"}`}>
            <h1 className="text-2xl font-bold mb-4">Kết quả tìm kiếm cho: {query}</h1>
            <p className="text-sm text-gray-500 mb-5">About {allResults.length.toLocaleString()} results (0.35 seconds)</p>
            
            <div className="space-y-6">
              {currentResults.map((result, index) => (
                <div key={index} className="max-w-2xl">
                  <div className="text-xs text-gray-600 mb-1">{result.url}</div>
                  <a 
                    href={result.url} 
                    className="text-xl text-blue-800 hover:underline font-medium block mb-1"
                  >
                    {result.title}
                  </a>
                  <p className="text-sm text-gray-700 mb-2">{result.description}</p>
                  
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

            {/* Pagination */}
            <div className="flex justify-center mt-8">
              <nav className="flex items-center gap-1">
                <button
                  onClick={() => setCurrentPage(prev => Math.max(prev - 1, 1))}
                  disabled={currentPage === 1}
                  className="px-3 py-1 rounded hover:bg-gray-100 disabled:opacity-50"
                >
                  Previous
                </button>
                
                {Array.from({ length: Math.min(5, totalPages) }, (_, i) => {
                  const pageNum = currentPage <= 3 
                    ? i + 1 
                    : currentPage >= totalPages - 2 
                      ? totalPages - 4 + i 
                      : currentPage - 2 + i;
                  
                  if (pageNum < 1 || pageNum > totalPages) return null;

                  return (
                    <button
                      key={pageNum}
                      onClick={() => setCurrentPage(pageNum)}
                      className={`px-3 py-1 rounded ${currentPage === pageNum ? 'bg-blue-100 text-blue-800' : 'hover:bg-gray-100'}`}
                    >
                      {pageNum}
                    </button>
                  );
                })}
                
                <button
                  onClick={() => setCurrentPage(prev => Math.min(prev + 1, totalPages))}
                  disabled={currentPage === totalPages}
                  className="px-3 py-1 rounded hover:bg-gray-100 disabled:opacity-50"
                >
                  Next
                </button>
              </nav>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
};

export default SearchResults;