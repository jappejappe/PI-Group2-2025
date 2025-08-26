document.addEventListener("DOMContentLoaded", function () {

    function logar() {
        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;


        axios.post("http://127.0.0.1:5000/logar", {
            email: email,
            password: password
        })
        
        .then(response => {
            console.log("Sucesso:", response.data);
            if (response.data.status === "Sucesso") {
                localStorage.setItem("compradorId", response.data.compradorId);
                window.location.href = "http://127.0.0.1:5000/perfil";
            }
            else {
                alert("Falha no login: " + response.data.message);
            }
        })
    }

    document.getElementById("logarButton").addEventListener("click", () => {
        console.log("Clicou no botão");
        logar();
    });

});