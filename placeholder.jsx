import { createRoot } from 'react-dom/client';
import Button from './components/button';
// nao tem ainda ^

const ButtonDiv = document.getElementById('botao-continuar');
if (ButtonDiv) {
  createRoot(ButtonDiv).render(<Button/>);
}
// coloca o componente do botao na div ^