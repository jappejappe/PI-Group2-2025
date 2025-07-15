import React from 'react';

export default function CardVenda({ titulo, preco, descricao }) {
  return (
    <div style={{ border: '1px solid #ccc', padding: '16px', borderRadius: '10px', width: '250px' }}>
      <h2>{titulo}</h2>
      <p>{descricao}</p>
      <strong>R$ {preco}</strong>
    </div>
  );
}
