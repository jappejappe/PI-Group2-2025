document.addEventListener("DOMContentLoaded", () => {


    const button = document.getElementById("registrarButton");

    function getRegistrar() {

        const nome = document.getElementById('nome').value;
        const apelido = document.getElementById('username').value;
        const email = document.getElementById('email').value;
        const nascimento = document.getElementById('nascimento').value;
        const cep = document.getElementById('cep').value.replace(/\D/g, '');;
        const cpf = document.getElementById('cpf').value.replace(/\D/g, '');;
        const password = document.getElementById('password').value;
        const fotoInput = document.getElementById('foto');
        const file = fotoInput.files[0];

        if (!file) {
            alert("Adicione uma foto de perfil.");
            return
        }

        const reader = new FileReader();
        reader.onloadend = function () {
            const fotoBase64 = reader.result.split(",")[1];

            axios.post("http://127.0.0.1:5000/registrarDB",{
            nome: nome,
            apelido: apelido,
            email: email,
            nascimento: nascimento,
            cep: cep,
            cpf: cpf,
            password: password,
            foto: fotoBase64
        },
        { timeout: 0 }
        )

        .then(response => {
            console.log(response.data)
            console.log("Sucesso:", response.data);
            const compradorId = response.data.compradorId;
            const usuarioId = response.data.usuarioId;
            if (response.data.status === "Sucesso") {
                localStorage.setItem("compradorId", compradorId);
                localStorage.setItem("usuarioId", usuarioId);
                window.location.href = `/perfil/${compradorId}`;
            }
            else {
                alert("Falha no registro: " + response.data.message);
            }
        })
        .catch(error => {
            console.error("Erro na requisição:", error);
            alert("Erro ao registrar: " + (error.response?.data?.message || error.message));
        });
        };

        reader.readAsDataURL(file);
    }

    button.addEventListener("click", () => {
        console.log("Clicou no botão");
        getRegistrar();
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

    function formatDate(raw) {
        const d = raw.replace(/\D/g, '').slice(0,8);
        const dd = d.slice(0,2), mm = d.slice(2,4), yy = d.slice(4,8);
        let out = '';
        if (dd) out += dd;
        if (mm) out += '/' + mm;
        if (yy) out += '/' + yy;
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
    attachMask('#nascimento', formatDate);
    // attachMask('#telefone', formatPhone); // se existir, implemente formatPhone similar

    // limpeza antes de enviar
    const form = document.getElementById('registrarForm');
    if (form) {
        form.addEventListener('submit', function (e) {
        e.preventDefault();
        const onlyDigits = v => v ? v.replace(/\D/g, '') : '';
        ['cep','cpf','telefone'].forEach(id => {
            const el = document.getElementById(id);
            if (el) el.value = onlyDigits(el.value);
        });
        const nasc = document.getElementById('nascimento');
        if (nasc) {
            const m = nasc.value.match(/^(\d{2})\/(\d{2})\/(\d{4})$/);
            if (m) nasc.value = `${m[3]}-${m[2]}-${m[1]}`;
        }
        });
    }
});