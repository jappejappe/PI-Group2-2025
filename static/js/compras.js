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



