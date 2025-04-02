document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("form-login");
    const erroMsg = document.getElementById("erro-login");

    form.addEventListener("submit", async (e) => {
        e.preventDefault();

        const email = document.getElementById("email").value;
        const senha = document.getElementById("senha").value;

        try {
            const res = await fetch("/api/usuarios/login", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ email, senha }),
            });

            if (res.ok) {
                // Aguarda um pouco para garantir que o cookie seja salvo
                setTimeout(() => {
                    window.location.href = "/";
                }, 300);
            } else {
                const data = await res.json();
                erroMsg.textContent = data.detail || "Erro ao fazer login.";
            }
        } catch (err) {
            console.error(err);
            erroMsg.textContent = "Erro de conexão com o servidor.";
        }
    });
});
