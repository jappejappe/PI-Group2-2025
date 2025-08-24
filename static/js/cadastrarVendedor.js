document.addEventListener("DOMContentLoaded", function () {

    // document.getElementById("outrosCheckbox").addEventListener("change", function () {
    //     const outrosInput = document.getElementById("outrosInput");
    //     if (this.checked) {
    //         outrosInput.style.display = "block";
    //     } else {
    //         outrosInput.style.display = "none";
    //         outrosInput.value = "";
    //     }
    // });


    // document.getElementById("meuFormulario").addEventListener("submit", function (e) {
    //     e.preventDefault();


    //     const textInputs = this.querySelectorAll('input[type="text"]');
    //     const checkboxes = this.querySelectorAll('input[type="checkbox"]');
    //     const outrosCheckbox = document.getElementById("outrosCheckbox");
    //     const outrosInput = document.getElementById("outrosInput");


    //     for (let input of textInputs) {
    //         if (input !== outrosInput && input.value.trim() === "") {
    //         alert("É obrigatório preencher todos os campos.");
    //         input.focus();
    //         return;
    //         }
    //     }


    //     let algumMarcado = false;
    //     for (let checkbox of checkboxes) {
    //         if (checkbox.checked) {
    //         algumMarcado = true;
    //         break;
    //         }
    //     }
    //     if (!algumMarcado) {
    //         alert("Selecione pelo menos uma opção.");
    //         return;
    //     }


    //     if (outrosCheckbox.checked && outrosInput.value.trim() === "") {
    //         alert("Você marcou 'Outros'. Especifique o conteúdo.");
    //         outrosInput.focus();
    //         return;
    //     }


    //     alert("Formulário válido! Pode ser enviado.");
    // });

////////////////////////////////////////////////////////////////////////////////////////////////////
// Inserir vendedor no banco de dados

    function cadastrarVendedor() {
        const userId = localStorage.getItem("userId");
        const nome = document.getElementById('nome').value;
        const cep = document.getElementById('cep').value;
        const telefone = document.getElementById('telefone').value;
        const email = document.getElementById('email').value;
        const descricao = document.getElementById('descricao').value;


        console.log("ID do usuário salvo:", userId);


        axios.post("http://127.0.0.1:5000/cadastrarVendedor", {
            id_comprador: userId,
            nome: nome,
            email: email,
            cep: cep,
            telefone: telefone,
            descricao: descricao
        }) // NOTA PARA MIM MESMO: você parou aqui, ainda precisa fazer a rota do flask que recebe e add no banco
        // Falta pegar o coiso dos carregamentos, e linkar com o usuário logado
        
        .then(response => {
            console.log("Sucesso:", response.data);
            window.location.href = "http://127.0.0.1:5000/perfil";
        })
    }

    document.getElementById("cadastrarVendedorButton").addEventListener("click", () => {
        console.log("Clicou no botão");
        cadastrarVendedor();
    });

});