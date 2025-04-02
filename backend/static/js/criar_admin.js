document.addEventListener("DOMContentLoaded", () => {
    const form = document.querySelector("form");
    if (!form) return;

    form.addEventListener("submit", (e) => {
        const email = form.email.value.trim();
        const senha = form.senha.value.trim();
        const confirmar = form.confirmar_senha?.value.trim();  // opcional, caso não tenha

        // Remove mensagens antigas
        document.querySelectorAll(".erro-validacao").forEach(el => el.remove());

        let mensagemErro = "";

        // Validação de email
        if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
            mensagemErro = "Email inválido.";
        }

        // Validação de tamanho
        else if (senha.length < 6) {
            mensagemErro = "A senha deve ter pelo menos 6 caracteres.";
        }

        // Força mínima: letras + números + caractere especial
        else if (!/[a-zA-Z]/.test(senha) || !/\d/.test(senha) || !/[!@#$%^&*()_+{}\[\]:;<>,.?~\\/-]/.test(senha)) {
            mensagemErro = "A senha deve conter letras, números e um caractere especial.";
        }

        // Confirmação de senha (se o campo existir)
        else if (confirmar && senha !== confirmar) {
            mensagemErro = "As senhas não coincidem.";
        }

        if (mensagemErro) {
            e.preventDefault();

            const aviso = document.createElement("p");
            aviso.textContent = mensagemErro;
            aviso.classList.add("erro-validacao");
            aviso.style.color = "red";
            form.appendChild(aviso);
        }
    });
});
