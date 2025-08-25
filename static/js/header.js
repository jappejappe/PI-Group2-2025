document.addEventListener("DOMContentLoaded", () => {
    const userIcon = document.getElementById("user-icon");
    const userMenu = document.getElementById("user-menu");

    // fazer o menu
    function renderMenu() {
        userMenu.innerHTML = "";
        const compradorId = localStorage.getItem("compradorId");

        if (compradorId) {
            // se tiver logado
            const btnPerfil = document.createElement("button");
            btnPerfil.textContent = "Ver perfil";
            btnPerfil.onclick = () => {
                window.location.href = `/perfil/${compradorId}`;
            };

            const btnLogout = document.createElement("button");
            btnLogout.textContent = "Logout";
            btnLogout.classList.add("logout");
            btnLogout.onclick = () => {
                localStorage.removeItem("compradorId");
                renderMenu(); // recarrega menu
            };

            userMenu.appendChild(btnPerfil);
            userMenu.appendChild(btnLogout);
        } else {
            // se nao tiver logado
            const btnLogin = document.createElement("button");
            btnLogin.textContent = "Login";
            btnLogin.onclick = () => {
                window.location.href = "/login";
            };

            const btnRegistrar = document.createElement("button");
            btnRegistrar.textContent = "Registrar";
            btnRegistrar.onclick = () => {
                window.location.href = "/registrar";
            };

            userMenu.appendChild(btnLogin);
            userMenu.appendChild(btnRegistrar);
        }
    }

    // abrir o menu quando clica
    userIcon.addEventListener("click", () => {
        renderMenu();
        userMenu.classList.toggle("hidden");
    });

    // fechar
    document.addEventListener("click", (e) => {
        if (!userMenu.contains(e.target) && e.target !== userIcon) {
            userMenu.classList.add("hidden");
        }
    });
});