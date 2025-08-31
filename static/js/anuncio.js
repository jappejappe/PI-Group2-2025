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
  const carrinhoBotao = card.querySelector("#botaoCard");

  // adiciona evento de clique
  carrinhoBotao.addEventListener("click", () => {
    const compradorId = localStorage.getItem("compradorId"); // precisa já estar salvo no login
    if (!compradorId) {
      alert("Você precisa estar logado para adicionar itens ao carrinho.");
      return;
    }

    axios.post("http://127.0.0.1:5000/addCarrinho", {
      id_comprador: compradorId,
      id_produto: anuncio.id,
      quantidade: 1
    })
    .then(() => {
      alert("Produto adicionado ao carrinho!");
    })
    .catch(err => {
      console.error("Erro ao adicionar ao carrinho:", err);
      alert("Erro ao adicionar ao carrinho.");
    });
  });

});