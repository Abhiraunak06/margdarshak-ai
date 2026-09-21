import React from 'react';
import { Sparkles, Mic } from 'lucide-react';

export default function GlassOrb({ size = 200, onClick, active = false }) {
  return (
    <div 
      onClick={onClick}
      className="relative flex flex-col items-center justify-center cursor-pointer group select-none"
      title="Margdarshak AI Orb — Click to talk with AI"
    >
      {/* Ambient background glow aura */}
      <div 
        className="absolute rounded-full filter blur-2xl opacity-60 transition-all duration-700 group-hover:opacity-85 group-hover:scale-110 pointer-events-none"
        style={{
          width: `${size * 1.2}px`,
          height: `${size * 1.2}px`,
          background: 'radial-gradient(circle, rgba(244, 114, 182, 0.45) 0%, rgba(168, 85, 247, 0.35) 40%, rgba(56, 189, 248, 0.25) 70%, transparent 85%)',
        }}
      />

      {/* Floating 3D Iridescent Glass Orb */}
      <div 
        className="relative rounded-full shadow-orb animate-float-slow transition-transform duration-500 group-hover:scale-105"
        style={{
          width: `${size}px`,
          height: `${size}px`,
          background: `
            radial-gradient(circle at 35% 25%, rgba(255, 255, 255, 0.95) 0%, rgba(255, 255, 255, 0.3) 18%, transparent 42%),
            radial-gradient(circle at 75% 70%, rgba(56, 189, 248, 0.85) 0%, rgba(147, 51, 234, 0.7) 45%, rgba(236, 72, 153, 0.85) 85%),
            linear-gradient(135deg, rgba(251, 113, 133, 0.85) 0%, rgba(168, 85, 247, 0.75) 50%, rgba(14, 165, 233, 0.85) 100%)
          `,
          boxShadow: `
            inset 0 10px 25px rgba(255, 255, 255, 0.9),
            inset 0 -12px 25px rgba(14, 165, 233, 0.5),
            inset 0 0 40px rgba(236, 72, 153, 0.6),
            0 20px 45px -10px rgba(168, 85, 247, 0.45),
            0 0 25px rgba(56, 189, 248, 0.3)
          `,
          border: '1.5px solid rgba(255, 255, 255, 0.65)'
        }}
      >
        {/* Specular curved reflection rim on top edge */}
        <div 
          className="absolute inset-1 rounded-full pointer-events-none opacity-80"
          style={{
            background: 'radial-gradient(ellipse at 40% 15%, rgba(255, 255, 255, 0.9) 0%, rgba(255, 255, 255, 0) 55%)'
          }}
        />

        {/* Internal refractive liquid highlight */}
        <div 
          className="absolute bottom-3 left-1/2 -translate-x-1/2 w-3/4 h-1/3 rounded-full pointer-events-none opacity-70 blur-xs"
          style={{
            background: 'radial-gradient(ellipse, rgba(56, 189, 248, 0.95) 0%, rgba(147, 51, 234, 0.5) 60%, transparent 100%)'
          }}
        />

        {/* Center Minimalist Icon Glyph */}
        <div className="absolute inset-0 flex items-center justify-center pointer-events-none">
          <div className="w-10 h-10 rounded-full bg-white/20 backdrop-blur-md flex items-center justify-center border border-white/40 shadow-inner group-hover:scale-110 transition-transform">
            <Sparkles className="w-5 h-5 text-white/90 drop-shadow-sm animate-pulse" />
          </div>
        </div>
      </div>

      {/* Realistic Floor Reflection */}
      <div 
        className="mt-3 rounded-full blur-md opacity-35 transition-all duration-500 group-hover:opacity-50 pointer-events-none"
        style={{
          width: `${size * 0.75}px`,
          height: `${size * 0.18}px`,
          background: 'radial-gradient(ellipse, rgba(168, 85, 247, 0.7) 0%, rgba(56, 189, 248, 0.5) 50%, transparent 80%)'
        }}
      />
    </div>
  );
}
