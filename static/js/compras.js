// mostra/esconde seção de novo endereço
    document.querySelectorAll('input[name="endereco"]').forEach(radio => {
      radio.addEventListener('change', function() {
        const novoEnderecoDiv = document.getElementById('novoEndereco');
        if (this.value === 'novo') {
          novoEnderecoDiv.style.display = 'block';
        } else {
          novoEnderecoDiv.style.display = 'none';
        }
      });
    });

// coloca barra no cep
    document.getElementById('cep').addEventListener('input', function(e) {
      let value = e.target.value.replace(/\D/g, '');
      if (value.length > 5) {
        value = value.substring(0, 5) + '-' + value.substring(5, 8);
      }
      e.target.value = value;
    });


// FORMATA NUMERO DO CARTAO PARA TER OS ESPAÇOS
    document.getElementById('numeroCartao').addEventListener('input', function(e) {
      let value = e.target.value.replace(/\D/g, '');
      value = value.replace(/(\d{4})(?=\d)/g, '$1 ');
      e.target.value = value;
    });

// FORMATA VALIDADE PRA TER A BARRA
    document.getElementById('validadeCartao').addEventListener('input', function(e) {
      let value = e.target.value.replace(/\D/g, '');
      if (value.length >= 2) {
        value = value.substring(0, 2) + '/' + value.substring(2, 4);
      }
      e.target.value = value;
    });

// Finalizar compra
    document.getElementById("botao-finalizar").addEventListener("click", finalizarCompra);

    function finalizarCompra() {
    const btnFinalizar = document.getElementById("botao-finalizar");
    btnFinalizar.disabled = true;
    

    setTimeout(() => {
        document.getElementById('modalConfirmacao').style.display = 'flex';
    }, 100);
    }


// poder fechar o modal
    document.getElementById('modalConfirmacao').addEventListener('click', function(e) {
      if (e.target === this) {
        this.style.display = 'none';
      }
    });


// atualizar preço das parcelas
    function atualizarParcelas() {
      // total da compra
      const totalElement = document.querySelector('.valor-total span:last-child');
      const totalText = totalElement.textContent;
      const total = parseFloat(totalText.replace('R$ ', '').replace(',', '.'));
      
      const parcelasSelect = document.getElementById('parcelas');
      parcelasSelect.innerHTML = '';
      
      for (let i = 1; i <= 12; i++) {
        const valorParcela = (total / i).toFixed(2);
        const option = document.createElement('option');
        option.value = i;
        option.textContent = `${i}x de R$ ${valorParcela.replace('.', ',')}`;
        parcelasSelect.appendChild(option);
      }
    }

    document.addEventListener('DOMContentLoaded', function() {
      atualizarParcelas();
    });

// parte de inserir dados cartão
    document.addEventListener("DOMContentLoaded", () => {
  const botaoFinalizar = document.getElementById("botao-finalizar");
  const modalConfirmacao = document.getElementById("modalConfirmacao");

  const camposPagamento = {
    numeroCartao: document.getElementById("numeroCartao"),
    nomeCartao: document.getElementById("nomeCartao"),
    validadeCartao: document.getElementById("validadeCartao"),
    cvv: document.getElementById("cvv"),
  };

  function validarCampos() {
    let valido = true;
    let mensagens = [];

    for (const [campo, input] of Object.entries(camposPagamento)) {
      if (input.value.trim() === "") {
        valido = false;
        mensagens.push(`Preencha o campo: ${campo}`);
        input.classList.add("erro");
      } else {
        input.classList.remove("erro");
      }
    }

    if (!valido) {
      alert("Por favor, corrija os erros:\n\n" + mensagens.join("\n"));
      return false;
    }

    return valido
  }
});