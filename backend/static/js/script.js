document.addEventListener("DOMContentLoaded", () => {
    // Só roda o restante se estiver na home
    if (window.location.pathname !== "/") return;

    const form = document.getElementById("form-transacao");
    const filtroForm = document.getElementById("filtro-form");
    const lista = document.getElementById("lista-transacoes");
    const mesInput = document.getElementById("mes");
    const anoInput = document.getElementById("ano");
    const botaoAtualizar = document.getElementById("btn-atualizar-resumo");

    let graficoReceitas = null;
    let graficoDespesas = null;

    async function verificarLogin() {
        try {
            const res = await fetch("/api/usuarios/login-status");
            if (!res.ok) {
                window.location.href = "/login";
            } else {
                // Só carrega os dados se o login estiver OK
                carregarTransacoes();
                carregarResumo();
                carregarGraficoLinha();
            }
        } catch {
            window.location.href = "/login";
        }
    }

    if (form) {
        form.addEventListener("submit", async (e) => {
            e.preventDefault();
            const formData = new FormData(form);
            const dados = Object.fromEntries(formData.entries());

            try {
                const response = await fetch("/api/transacoes/", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify(dados)
                });
                if (response.ok) {
                    form.reset();
                    carregarTransacoes();
                    carregarResumo();
                } else {
                    alert("Erro ao adicionar transação.");
                }
            } catch (err) {
                console.error(err);
                alert("Erro de conexão.");
            }
        });
    }

    if (filtroForm) {
        filtroForm.addEventListener("submit", (e) => {
            e.preventDefault();
            carregarTransacoes();
        });
    }

    if (botaoAtualizar) {
        botaoAtualizar.addEventListener("click", () => {
            carregarResumo();
        });
    }

    async function carregarTransacoes() {
        if (!lista) return;

        try {
            const mes = mesInput?.value;
            const ano = anoInput?.value;
            let url = "/api/transacoes/";

            const params = new URLSearchParams();
            if (mes) params.append("mes", mes);
            if (ano) params.append("ano", ano);
            if (params.toString()) url += "?" + params.toString();

            const res = await fetch(url);
            const transacoes = await res.json();

            lista.innerHTML = "";
            const receitasPorCategoria = {};
            const despesasPorCategoria = {};

            transacoes.forEach((t) => {
                const item = document.createElement("li");
                item.innerHTML = `
                    <span class="info-transacao">
                    ${t.tipo.toUpperCase()} - R$${parseFloat(t.valor).toFixed(2)} - ${t.categoria} - ${t.descricao || "-"} - ${t.data}
                    </span>
                    <button class="editar-btn" data-id="${t.id}">Editar</button>
                    <button class="excluir-btn" data-id="${t.id}">Excluir</button>
                    <form class="editar-form" style="display: none; margin-top: 10px;">
                        <input type="text" name="tipo" value="${t.tipo}" required>
                        <input type="number" name="valor" value="${t.valor}" step="0.01" required>
                        <input type="text" name="categoria" value="${t.categoria}" required>
                        <input type="text" name="descricao" value="${t.descricao || ''}">
                        <input type="date" name="data" value="${t.data}" required>
                        <button type="submit">Salvar</button>
                        <button type="button" class="cancelar-edicao">Cancelar</button>
                    </form>
                `;

                item.querySelector(".editar-btn").addEventListener("click", () => {
                    item.querySelector(".info-transacao").style.display = "none";
                    item.querySelector(".editar-form").style.display = "block";
                });

                item.querySelector(".cancelar-edicao").addEventListener("click", () => {
                    item.querySelector(".info-transacao").style.display = "block";
                    item.querySelector(".editar-form").style.display = "none";
                });

                item.querySelector(".editar-form").addEventListener("submit", async (e) => {
                    e.preventDefault();
                    const formEdit = e.target;
                    const dadosAtualizados = Object.fromEntries(new FormData(formEdit));

                    try {
                        const res = await fetch(`/api/transacoes/${t.id}`, {
                            method: "PUT",
                            headers: { "Content-Type": "application/json" },
                            body: JSON.stringify(dadosAtualizados)
                        });

                        if (res.ok) {
                            carregarTransacoes();
                            carregarResumo();
                        } else {
                            alert("Erro ao atualizar transação.");
                        }
                    } catch (err) {
                        console.error("Erro ao atualizar:", err);
                    }
                });

                item.querySelector(".excluir-btn").addEventListener("click", async () => {
                    if (confirm("Deseja realmente excluir esta transação?")) {
                        try {
                            const res = await fetch(`/api/transacoes/${t.id}`, {
                                method: "DELETE"
                            });
                            if (res.ok) {
                                carregarTransacoes();
                                carregarResumo();
                            } else {
                                alert("Erro ao excluir transação.");
                            }
                        } catch (err) {
                            console.error("Erro ao excluir:", err);
                        }
                    }
                });

                lista.appendChild(item);

                const categoria = t.categoria;
                const valor = parseFloat(t.valor);

                if (t.tipo === "receita") {
                    receitasPorCategoria[categoria] = (receitasPorCategoria[categoria] || 0) + valor;
                } else {
                    despesasPorCategoria[categoria] = (despesasPorCategoria[categoria] || 0) + valor;
                }
            });

            desenharGrafico("grafico-receitas", "Receitas por Categoria", receitasPorCategoria, graficoReceitas, g => graficoReceitas = g);
            desenharGrafico("grafico-despesas", "Despesas por Categoria", despesasPorCategoria, graficoDespesas, g => graficoDespesas = g);
        } catch (err) {
            console.error("Erro ao carregar transações:", err);
        }
    }

    async function carregarResumo() {
        try {
            const mes = mesInput?.value;
            const ano = anoInput?.value;
            let url = "/api/transacoes/resumo";

            const params = new URLSearchParams();
            if (mes) params.append("mes", mes);
            if (ano) params.append("ano", ano);
            if (params.toString()) url += "?" + params.toString();

            const res = await fetch(url);
            const data = await res.json();

            document.getElementById("resumo-receitas").textContent = `R$ ${data.receitas.toFixed(2)}`;
            document.getElementById("resumo-despesas").textContent = `R$ ${data.despesas.toFixed(2)}`;
            document.getElementById("resumo-saldo").textContent = `R$ ${data.saldo.toFixed(2)}`;
        } catch (err) {
            console.error("Erro ao carregar resumo:", err);
        }
    }

    function desenharGrafico(idCanvas, titulo, dados, graficoExistente, setGrafico) {
        const ctx = document.getElementById(idCanvas)?.getContext("2d");
        if (!ctx) return;

        if (graficoExistente) {
            graficoExistente.destroy();
        }

        const categorias = Object.keys(dados);
        const valores = Object.values(dados);
        const cores = categorias.map(() =>
            `hsl(${Math.floor(Math.random() * 360)}, 70%, 65%)`
        );

        const novoGrafico = new Chart(ctx, {
            type: 'pie',
            data: {
                labels: categorias,
                datasets: [{
                    label: titulo,
                    data: valores,
                    backgroundColor: cores,
                    borderColor: "#ffffff",
                    borderWidth: 2,
                    hoverOffset: 15
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'right',
                        labels: {
                            usePointStyle: true,
                            padding: 20
                        }
                    },
                    title: {
                        display: true,
                        text: titulo,
                        font: { size: 18 }
                    }
                }
            }
        });

        setGrafico(novoGrafico);
    }

    async function carregarGraficoLinha() {
        try {
            const mes = mesInput?.value;
            const ano = anoInput?.value;
            let url = "/api/transacoes/saldo-por-dia";

            const params = new URLSearchParams();
            if (mes) params.append("mes", mes);
            if (ano) params.append("ano", ano);
            if (params.toString()) url += "?" + params.toString();

            const res = await fetch(url);
            const dados = await res.json();

            const labels = dados.map(item => item.data);
            const saldos = dados.map(item => item.saldo);

            const ctx = document.getElementById("grafico-evolucao-saldo")?.getContext("2d");
            if (!ctx) return;

            if (window.graficoLinhaSaldo) {
                window.graficoLinhaSaldo.destroy();
            }

            window.graficoLinhaSaldo = new Chart(ctx, {
                type: "line",
                data: {
                    labels: labels,
                    datasets: [{
                        label: "Saldo acumulado",
                        data: saldos,
                        fill: false,
                        borderColor: "#0077cc",
                        tension: 0.3
                    }]
                },
                options: {
                    responsive: true,
                    plugins: {
                        title: {
                            display: true,
                            text: "Evolução do Saldo (Diária)"
                        },
                        legend: { display: false }
                    },
                    scales: {
                        x: { title: { display: true, text: "Data" } },
                        y: { title: { display: true, text: "Saldo (R$)" } }
                    }
                }
            });
        } catch (err) {
            console.error("Erro ao carregar gráfico de saldo:", err);
        }
    }

    if (window.location.pathname === "/") {
        verificarLogin();          // Só roda aqui
        carregarTransacoes();
        carregarResumo();
        carregarGraficoLinha();
    }
});
