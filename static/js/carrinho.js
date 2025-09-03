document.addEventListener("DOMContentLoaded", async () => {
    const compradorId = localStorage.getItem("compradorId");
    if (!compradorId) {
        document.querySelector(".produtos-lista").innerHTML =
            "<p>Você precisa estar logado para ver o carrinho. <a href='/login'>Fazer login</a></p>";
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
        document.querySelector(".produtos-lista").innerHTML =
            "<p>Erro ao carregar o carrinho. Tente novamente.</p>";
    }
});

function diminuirQuantidade(produtoId) {
    const input = document.getElementById(`qtd${produtoId}`);
    if (input.value > 1) {
        input.value--;
        atualizarPreco(produtoId);
    }
}

function aumentarQuantidade(produtoId) {
    const input = document.getElementById(`qtd${produtoId}`);
    input.value++;
    atualizarPreco(produtoId);
}

function atualizarPreco(produtoId) {
    const quantidade = parseInt(document.getElementById(`qtd${produtoId}`).value);
    const precoUnitario = parseFloat(
        document.getElementById(`preco${produtoId}`).getAttribute("data-preco-unitario")
    );
    const precoTotal = quantidade * precoUnitario;

    document.getElementById(`preco${produtoId}`).textContent = `R$ ${precoTotal
        .toFixed(2)
        .replace(".", ",")}`;
    atualizarTotalCarrinho();
}

async function removerProduto(produtoId) {
    try {
        const compradorId = localStorage.getItem("compradorId");
        if (!compradorId) {
            alert("Você precisa estar logado para remover itens do carrinho.");
            return;
        }

        const resp = await fetch("/removerDoCarrinho", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ id_comprador: compradorId, id_produto: produtoId })
        });

        const json = await resp.json();
        if (!resp.ok || (json && json.status !== "ok")) {
            console.error("Erro ao remover:", json);
            alert("Não foi possível remover o item.");
            return;
        }

        const produto = document.getElementById(`produto${produtoId}`);
        if (produto) produto.remove();
        atualizarTotalCarrinho();

    } catch (e) {
        console.error(e);
        alert("Erro ao comunicar com o servidor.");
    }
}

function atualizarTotalCarrinho() {
    const produtos = document.querySelectorAll(".produto-item");
    let total = 0;
    let totalItens = 0;

    produtos.forEach(produto => {
        const checkbox = produto.querySelector("input[type='checkbox']");
        if (checkbox && checkbox.checked) {
            const quantidade = parseInt(produto.querySelector(".quantidade-input").value);
            const precoUnitario = parseFloat(
                produto.querySelector(".preco-valor").getAttribute("data-preco-unitario")
            );
            total += quantidade * precoUnitario;
            totalItens += quantidade;
        }
    });

    document.getElementById("totalItens").textContent = `Total de itens: ${totalItens}`;
    document.getElementById("subtotal").textContent = `Subtotal: R$ ${total
        .toFixed(2)
        .replace(".", ",")}`;
}

document.addEventListener("change", function (e) {
    if (e.target.type === "checkbox" && e.target.closest(".produto-item")) {
        atualizarTotalCarrinho();
    }
});
