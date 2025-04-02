document.getElementById("form-registro").addEventListener("submit", async function (e) {
    e.preventDefault();

    const email = document.getElementById("email").value;
    const senha = document.getElementById("senha").value;

    const resposta = await fetch("/api/usuarios/registrar", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, senha })
    });

    if (resposta.ok) {
        const dados = await resposta.json();

        // Exibe mensagem de sucesso
        const mensagem = document.getElementById("mensagem");
        mensagem.innerText = dados.mensagem;
        mensagem.style.color = "green";

        // Redireciona após alguns segundos
        setTimeout(() => {
            window.location.href = "/login";
        }, 1500);
    } else {
        const erro = await resposta.json();
        const mensagem = document.getElementById("mensagem");
        mensagem.innerText = erro.detail || "Erro ao registrar.";
        mensagem.style.color = "red";
    }
});
