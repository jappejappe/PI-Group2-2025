document.getElementById("outrosCheckbox").addEventListener("change", function () {
    const outrosInput = document.getElementById("outrosInput");
    if (this.checked) {
        outrosInput.style.display = "block";
    } else {
        outrosInput.style.display = "none";
        outrosInput.value = "";
    }
});


document.getElementById("meuFormulario").addEventListener("submit", function (e) {
    e.preventDefault();


    const textInputs = this.querySelectorAll('input[type="text"]');
    const checkboxes = this.querySelectorAll('input[type="checkbox"]');
    const outrosCheckbox = document.getElementById("outrosCheckbox");
    const outrosInput = document.getElementById("outrosInput");


    for (let input of textInputs) {
        if (input !== outrosInput && input.value.trim() === "") {
        alert("É obrigatório preencher todos os campos.");
        input.focus();
        return;
        }
    }


    let algumMarcado = false;
    for (let checkbox of checkboxes) {
        if (checkbox.checked) {
        algumMarcado = true;
        break;
        }
    }
    if (!algumMarcado) {
        alert("Selecione pelo menos uma opção.");
        return;
    }


    if (outrosCheckbox.checked && outrosInput.value.trim() === "") {
        alert("Você marcou 'Outros'. Especifique o conteúdo.");
        outrosInput.focus();
        return;
    }


    alert("Formulário válido! Pode ser enviado.");
});

