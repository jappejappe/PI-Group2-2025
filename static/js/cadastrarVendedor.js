document.addEventListener("DOMContentLoaded", function () {
// Inserir vendedor no banco de dados

    function cadastrarVendedor() {
        const compradorId = localStorage.getItem("compradorId");
        const nome = document.getElementById('nome').value;
        const cep = document.getElementById('cep').value;
        const telefone = document.getElementById('telefone').value;
        const email = document.getElementById('email').value;
        const descricao = document.getElementById('descricao').value;
        const checkboxes = document.querySelectorAll('input[name="infraestrutura"]:checked');
        const selecionados = Array.from(checkboxes).map(cb => cb.value); // array de infraestruturasselecionadas


        console.log("ID do usuário salvo:", compradorId);


        axios.post("http://127.0.0.1:5000/cadastrarVendedor", {
            id_comprador: compradorId,
            nome: nome,
            email: email,
            cep: cep,
            telefone: telefone,
            descricao: descricao,
            carregamentos: selecionados // envia array de infraestruturas
        })
        
        .then(response => {
            console.log("Sucesso:", response.data);
            window.location.href = `/perfil/${compradorId}`;
        })
    }

    document.getElementById("cadastrarVendedorButton").addEventListener("click", (e) => {
        e.preventDefault();
        console.log("Clicou no botão");
        cadastrarVendedor();
    });

    // utilitários para preservar posição do cursor por índice de dígitos
    function digitIndexFromPos(val, pos) {
        let count = 0;
        for (let i = 0; i < pos; i++) if (/\d/.test(val[i])) count++;
        return count;
    }
    function setCursorByDigitIndex(input, digitIndex) {
        const val = input.value;
        let digitsSeen = 0;
        for (let i = 0; i < val.length; i++) {
        if (/\d/.test(val[i])) digitsSeen++;
        if (digitsSeen === digitIndex) { input.setSelectionRange(i + 1, i + 1); return; }
        }
        input.setSelectionRange(val.length, val.length);
    }

    // formatadores
    function formatCEP(raw) {
        const d = raw.replace(/\D/g, '').slice(0,8);
        if (d.length <= 5) return d;
        return d.slice(0,5) + '-' + d.slice(5);
    }

    function formatCPF(raw) {
        const d = raw.replace(/\D/g, '').slice(0,11);
        const p1 = d.slice(0,3), p2 = d.slice(3,6), p3 = d.slice(6,9), p4 = d.slice(9,11);
        let out = p1;
        if (p2) out += '.' + p2;
        if (p3) out += '.' + p3;
        if (p4) out += '-' + p4;
        return out;
    }

    function formatPhone(raw) {
        const d = raw.replace(/\D/g, '').slice(0,11);
        const ddd = d.slice(0,2), pt1 = d.slice(2,7), pt2 = d.slice(7,11);
        let out = '';
        if (ddd) out += '(' + ddd + ')';
        if (pt1) out += ' ' + pt1;
        if (pt2) out += '-' + pt2;
        return out;
    }

    // anexa máscara a um input pelo seletor
    function attachMask(selector, formatter) {
        const input = document.querySelector(selector);
        if (!input) return;
        input.addEventListener('input', function (e) {
        const oldVal = input.value;
        const oldPos = input.selectionStart;
        const digitIndex = digitIndexFromPos(oldVal, oldPos);
        const newVal = formatter(oldVal);
        input.value = newVal;
        setCursorByDigitIndex(input, digitIndex);
        });

        // também no paste (para formatar o conteúdo colado)
        input.addEventListener('paste', function () {
        setTimeout(() => { // wait for paste to populate
            input.value = formatter(input.value);
        }, 0);
        });
    }

    attachMask('#cep', formatCEP);
    attachMask('#cpf', formatCPF);
    attachMask('#telefone', formatPhone);
    // attachMask('#telefone', formatPhone); // se existir, implemente formatPhone similar

    // limpeza antes de enviar
    const form = document.getElementById('meuFormulario');
    if (form) {
        form.addEventListener('submit', function () {
        const onlyDigits = v => v ? v.replace(/\D/g, '') : '';
        ['cep','cpf','telefone'].forEach(id => {
            const el = document.getElementById(id);
            if (el) el.value = onlyDigits(el.value);
        });
        });
    }

});