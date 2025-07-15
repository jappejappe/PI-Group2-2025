import React from 'react';

export default function Botao({ texto, onClick }) {
  return (
    <button 
      onClick={onClick} 
      style={{ padding: '10px 20px', backgroundColor: '#3498db', color: 'white', border: 'none', borderRadius: '5px' }}
    >
      {texto}
    </button>
  );
}
