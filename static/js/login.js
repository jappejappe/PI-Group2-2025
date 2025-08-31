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
            const compradorId = response.data.compradorId;
            if (response.data.status === "Sucesso") {
                localStorage.setItem("compradorId", compradorId);
                window.location.href = `/perfil/${compradorId}`;
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