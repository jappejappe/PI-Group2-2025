document.addEventListener("DOMContentLoaded", () => {
  const principal = document.getElementById("imagemPrincipal");
  const miniaturas = document.querySelectorAll(".miniaturas img");

  miniaturas.forEach((thumb, index) => {
    thumb.addEventListener("click", () => {
      principal.src = thumb.src;
      miniaturas.forEach((t, i) => t.classList.toggle("ativa", i === index));
    });
  });
});