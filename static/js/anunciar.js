document.addEventListener("DOMContentLoaded", function () {

    let selectedFiles = [];

    // Função para mostrar o preview das imagens selecionadas
    document.getElementById("files").addEventListener("change", function() {
        const preview = document.getElementById("preview"); // div para mostrar os previews
        preview.innerHTML = ""; // limpa os previews anteriores
        selectedFiles = Array.from(this.files); // armazena os arquivos selecionados

        for (const file of selectedFiles) {
            if (!file.type.startsWith("image/")) continue; // ignora se não for imagem

            const reader = new FileReader(); // Lê os arquivos locais inseridos (fotos)
            reader.onload = function(e) { // dispara o onload quando a leitura é concluída
                const img = document.createElement("img"); // cria um elemento de imagem na tela
                img.src = e.target.result; // define o src da imagem como o resultado do FileReader
                img.style.maxWidth = "120px";
                img.style.maxHeight = "120px";
                img.style.margin = "5px";
                img.style.objectFit = "cover";
                img.style.border = "1px solid #000000";
                img.style.borderRadius = "8px";
                preview.appendChild(img);
            }
            reader.readAsDataURL(file);
        }
    });

    
    document.getElementById("sendBtn").addEventListener("click", async function() {

        if (selectedFiles.length === 0) {
            alert("Selecione pelo menos uma imagem!");
            return;
        }

        titulo = document.getElementById('titulo').value;
        condicao = document.getElementById('condicao').value;
        tipo_material = document.getElementById('tipo_material').value;
        descricao = document.getElementById('descricao').value;
        quantidade = document.getElementById('quantidade').value;
        preco = document.getElementById('preco').value;



        const base64Images = await Promise.all(
            selectedFiles.map(file => {
                return new Promise(resolve => {
                    const reader = new FileReader();
                    reader.onload = e => resolve(e.target.result); // Base64
                    reader.readAsDataURL(file);
                });
            })
        );


        axios.post("http://127.0.0.1:5000/salvarImagens", {
            titulo: document.getElementById('titulo').value,
            condicao: document.getElementById('condicao').value,
            tipo_material: document.getElementById('tipo_material').value,
            descricao: document.getElementById('descricao').value,
            quantidade: document.getElementById('quantidade').value,
            preco: document.getElementById('preco').value,
            imagens: base64Images,
        })
        
        .then(response => {
            console.log("Aviso: ", response.data);
            if (response.data.status === "Sucesso") {
                alert("Anúncio salvo com sucesso!");
                window.location.href = "/"; // Redireciona para a página inicial
            }
            else {
                alert("Falha ao anunciar: " + response.data.message);
            }
        })
    })

});