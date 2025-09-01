document.addEventListener("DOMContentLoaded", () => {
  const principal = document.getElementById("imagemPrincipal");
  const miniaturas = document.querySelectorAll(".miniaturas img");

  miniaturas.forEach((thumb, index) => {
    thumb.addEventListener("click", () => {
      principal.src = thumb.src;
      miniaturas.forEach((t, i) => t.classList.toggle("ativa", i === index));
    });
  });

  // pega o botão de carrinho
  const carrinhoBotao = document.querySelector("#botaoCarrinhoAnuncio");
  
  console.log("Botão encontrado:", carrinhoBotao);

  // adiciona evento de clique
  carrinhoBotao.addEventListener("click", () => {    
    const compradorId = localStorage.getItem("compradorId"); // precisa já estar salvo no login
    console.log("Comprador ID:", compradorId); // debug
    
    if (!compradorId) {
      alert("Você precisa estar logado para adicionar itens ao carrinho.");
      return;
    }

    // pega id de anuncio do url
    const urlParams = new URLSearchParams(window.location.search);
    const anuncioId = urlParams.get('id');
    console.log("Anúncio ID:", anuncioId); // debug

    if (!anuncioId) {
      alert("ID do anúncio não encontrado.");
      return;
    }

    console.log("Enviando requisição para addCarrinho..."); // debug

    axios.post("http://127.0.0.1:5000/addCarrinho", {
      id_comprador: compradorId,
      id_produto: anuncioId,
      quantidade: 1
    })
    .then(() => {
      console.log("Sucesso! Produto adicionado ao carrinho"); // debug
      alert("Produto adicionado ao carrinho!");
    })
    .catch(err => {
      console.error("Erro ao adicionar ao carrinho:", err);
      alert("Erro ao adicionar ao carrinho.");
    });
  });

});