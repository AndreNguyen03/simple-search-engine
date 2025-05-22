
import React, { useEffect } from "react";
import GoogleLogo from "../components/Logo";
import SearchBar from "../components/SearchBar";

const Index = () => {
  useEffect(() => {
    document.title = "Vietnamnet"; // title mặc định khi ở trang chủ
  }, []);
  return (
    <div className="flex flex-col min-h-screen">
      <main className="flex-1 flex flex-col justify-center items-center px-4 pb-20">
        <GoogleLogo />
        <SearchBar />
      </main>
      <footer className="py-4 text-center text-sm text-gray-600">
        © {new Date().getFullYear()} Copyright by AndreNguyen03&FhuAnn
      </footer>
    </div>
  );
};

export default Index;
