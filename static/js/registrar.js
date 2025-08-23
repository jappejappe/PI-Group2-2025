document.addEventListener("DOMContentLoaded", () => {


    const button = document.getElementById("registrarButton");

    function getRegistrar() {

        const nome = document.getElementById('nome').value;
        const apelido = document.getElementById('username').value;
        const email = document.getElementById('email').value;
        const nascimento = document.getElementById('nascimento').value;
        const cep = document.getElementById('cep').value;
        const cpf = document.getElementById('cpf').value;
        const password = document.getElementById('password').value;

        axios.post("http://127.0.0.1:5000/registrarDB", {
            nome: nome,
            apelido: apelido,
            email: email,
            nascimento: nascimento,
            cep: cep,
            cpf: cpf,
            password: password
        })

        .then(response => {
            console.log("Sucesso:", response.data);
            window.location.href = "http://127.0.0.1:5000/perfil";
        })

    }

    button.addEventListener("click", () => {
        console.log("Clicou no botão");
        getRegistrar();
    });

});