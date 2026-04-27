import React from 'react';

interface MagazineCardProps {
  title: string;
  image: string;
  score: number;
  category: string;
}

export const MagazineCard: React.FC<MagazineCardProps> = ({ title, image, score, category }) => {
  const matchPercentage = Math.round(score * 100);
  
  return (
    <div className="relative group overflow-hidden rounded-xl bg-surface ghost-border transition-all duration-300 hover:scale-[1.02] hover:shadow-2xl hover:shadow-primary/20 flex flex-col h-full">
      
      {/* Portada */}
      <div className="relative aspect-[3/4] w-full overflow-hidden bg-[#2a2a2b]">
        <img 
          src={image} 
          alt={title} 
          className="w-full h-full object-cover transition-transform duration-500 group-hover:scale-105"
          onError={(e) => { e.currentTarget.src = "https://via.placeholder.com/300x400?text=No+Cover" }}
        />
        
        {/* Gradiente oscuro sobre la imagen para que resalte el Match Score */}
        <div className="absolute inset-0 bg-gradient-to-t from-black/80 via-black/20 to-transparent opacity-80" />
        
        {/* Match Score Badge (Glassmorphism) */}
        <div className="absolute top-3 right-3 flex items-center justify-center w-12 h-12 rounded-full bg-[#353436]/60 backdrop-blur-md ghost-border shadow-lg">
          <div className="relative flex items-center justify-center w-full h-full">
            <svg className="absolute w-full h-full -rotate-90">
              <circle cx="24" cy="24" r="20" stroke="rgba(255,255,255,0.1)" strokeWidth="3" fill="none" />
              <circle 
                cx="24" cy="24" r="20" 
                stroke="#00d16a" 
                strokeWidth="3" 
                fill="none" 
                strokeDasharray={`${matchPercentage * 1.25} 125`} 
                strokeLinecap="round"
              />
            </svg>
            <span className="text-xs font-bold font-sans text-textPrimary z-10">{matchPercentage}%</span>
          </div>
        </div>
      </div>

      {/* Contenido Editorial */}
      <div className="p-5 flex flex-col flex-grow">
        <span className="text-[10px] font-bold tracking-widest uppercase text-secondary mb-2 block font-sans">
          {category}
        </span>
        <h3 className="font-display text-lg leading-tight text-textPrimary mb-3 line-clamp-2">
          {title}
        </h3>
        
        <div className="mt-auto">
          <button className="w-full py-2 px-4 rounded-full bg-primary/10 text-primary text-sm font-semibold hover:bg-primary hover:text-white transition-colors duration-200">
            View Details
          </button>
        </div>
      </div>
    </div>
  );
};
