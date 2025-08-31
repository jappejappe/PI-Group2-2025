const container = document.getElementById("anunciosContainer");
const template = document.getElementById("cardTemplate");

axios.get("http://127.0.0.1:5000/mostrarAnuncios")
    .then(response => {
        const anuncios = response.data;

        anuncios.forEach(anuncio => {
            // clona o template
            const card = template.cloneNode(true);
            card.style.display = "flex"; // mostra o card

            // preenche os dados
            card.querySelector(".card-img").alt = anuncio.titulo || "Produto";
            card.querySelector(".card_titulo").textContent = anuncio.titulo || "Produto sem título";
            card.querySelector(".card_preco").textContent = anuncio.preco ? `R$ ${anuncio.preco}` : "R$ 0,00";
            
            const verBotao = card.querySelector("#verBotaoCard");
                verBotao.addEventListener("click", () => {
                window.location.href = `/anuncio?id=${anuncio.id}`;
            });

            // pega o botão de carrinho
            const carrinhoBotao = card.querySelector("#carrinhoBotao");

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

            // adiciona ao container
            container.appendChild(card);
        });
    })
    .catch(err => console.error("Erro ao carregar anúncios:", err));
