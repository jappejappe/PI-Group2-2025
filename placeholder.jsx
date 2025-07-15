import React from 'react';

import { createRoot } from 'react-dom/client';
import Botao from './components/button';
// nao tem ainda ^

const BotaoContinuarDiv = document.getElementById('botao-continuar');
if (BotaoContinuarDiv) {
  createRoot(BotaoContinuarDiv).render(<Botao texto="Continuar" backgroundColor="#000000" color="#ffffff"/>);
}

const BotaoLoginDiv = document.getElementById('botao-fazerlogin');
if (BotaoLoginDiv) {
  createRoot(BotaoLoginDiv).render(<Botao texto="Fazer Login" backgroundColor="#ffffff" color="#000000"/>);
}

const BotaoCriarContaDiv = document.getElementById('botao-criarconta');
if (BotaoCriarContaDiv) {
  createRoot(BotaoCriarContaDiv).render(<Botao texto="Criar Conta" backgroundColor="#ffffff" color="#000000"/>);
}
// coloca o componente do botao na div ^