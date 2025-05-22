
import React from "react";

const Footer = () => {
  return (
    <footer className="absolute bottom-0 left-0 right-0 bg-gray-100 text-sm text-gray-600">
      <div className="py-3 px-8 border-b border-gray-300">
        <span>United States</span>
      </div>
      <div className="flex flex-col md:flex-row md:justify-between py-3 px-8 space-y-4 md:space-y-0">
        <div className="flex flex-wrap gap-x-6 gap-y-2">
          <a href="#" className="hover:underline">About</a>
          <a href="#" className="hover:underline">Advertising</a>
          <a href="#" className="hover:underline">Business</a>
          <a href="#" className="hover:underline">How Search works</a>
        </div>
        <div className="flex flex-wrap gap-x-6 gap-y-2">
          <a href="#" className="hover:underline">Privacy</a>
          <a href="#" className="hover:underline">Terms</a>
          <a href="#" className="hover:underline">Settings</a>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
