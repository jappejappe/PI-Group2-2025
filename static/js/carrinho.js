document.addEventListener("DOMContentLoaded", async() => {
    const compradorId = localStorage.getItem("compradorId");
    if (!compradorId) {
        document.querySelector(".produtos-lista").innerHTML = "<p>Você precisa estar logado para ver o carrinho. <a href='/login'>Fazer login</a></p>";
        return;
    }

    try {
        const response = await fetch("/getCarrinho", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ id_comprador: compradorId })
        });

        const itens = await response.json();

        const lista = document.querySelector(".produtos-lista");
        lista.innerHTML = "";

        if (itens.length === 0) {
            lista.innerHTML = "<p>Seu carrinho está vazio.</p>";
            return;
        }

        itens.forEach(item => {
            const produto = document.createElement("div");
            produto.classList.add("produto-item");
            produto.id = `produto${item.id}`;

            produto.innerHTML = `
        <div class="produto-checkbox"><input type="checkbox" checked></div>
        <div class="produto-imagem"><div class="imagem-placeholder"></div></div>
        <div class="produto-info"><p class="produto-descricao">${item.titulo}</p></div>
        <div class="produto-quantidade">
          <div class="quantidade-controles">
            <button class="btn-quantidade" onclick="diminuirQuantidade(${item.id})">-</button>
            <input type="number" value="${item.quantidade}" min="1" class="quantidade-input" id="qtd${item.id}" onchange="atualizarPreco(${item.id})">
            <button class="btn-quantidade" onclick="aumentarQuantidade(${item.id})">+</button>
          </div>
        </div>
        <div class="produto-preco"><span class="preco-valor" id="preco${item.id}" data-preco-unitario="${item.preco}">R$ ${(item.preco * item.quantidade).toFixed(2).replace('.', ',')}</span></div>
        <div class="produto-acoes"><button class="btn-remover" onclick="removerProduto(${item.id})">×</button></div>
      `;

            lista.appendChild(produto);
        });

        atualizarTotalCarrinho();

    } catch (err) {
        console.error("Erro ao carregar carrinho:", err);
        document.querySelector(".produtos-lista").innerHTML = "<p>Erro ao carregar o carrinho. Tente novamente.</p>";
    }
});