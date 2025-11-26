import React from 'react';
import './Logo.css';

export default function Logo() {
  return (
    <div className="logo-container">
      <div className="logo-icon">
        <svg width="32" height="32" viewBox="0 0 32 32" fill="none">
          {/* AI智议院Logo设计 */}
          {/* 外圆代表议事厅 */}
          <circle cx="16" cy="16" r="15" fill="#4a90e2" stroke="#2c5aa0" strokeWidth="1"/>

          {/* 内部三个人形代表多个AI */}
          <circle cx="10" cy="12" r="2.5" fill="white"/>
          <path d="M10 15 Q10 18 8 20 Q10 19 12 20 Q10 18 10 15" fill="white"/>

          <circle cx="16" cy="12" r="2.5" fill="white"/>
          <path d="M16 15 Q16 18 14 20 Q16 19 18 20 Q16 18 16 15" fill="white"/>

          <circle cx="22" cy="12" r="2.5" fill="white"/>
          <path d="M22 15 Q22 18 20 20 Q22 19 24 20 Q22 18 22 15" fill="white"/>

          {/* 底部对话气泡代表审议 */}
          <ellipse cx="16" cy="26" rx="6" ry="3" fill="white" opacity="0.9"/>
          <path d="M14 26 L13 28 L15 27" fill="white" opacity="0.9"/>
        </svg>
      </div>
      <div className="logo-text">
        <h1>AI智议院</h1>
        <span className="logo-subtitle">多模型协作审议系统</span>
      </div>
    </div>
  );
}