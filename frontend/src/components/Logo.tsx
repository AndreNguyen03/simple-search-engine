import React from "react";

interface LogoProps {
  small?: boolean;
}

const Logo = ({ small = false }: LogoProps) => {
  const logoUrl = "/logo.png" 
  
  const sizeClass = small ? "w-32 h-10" : "w-80 h-24"; // Có thể điều chỉnh

  return (
    <div className="flex justify-center my-3">
      <img 
        src={logoUrl} 
        alt="Company Logo"
        className={`${sizeClass} object-contain`}
      />
    </div>
  );
};

export default Logo;