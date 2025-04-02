document.addEventListener("DOMContentLoaded", async () => {
    const ctx = document.getElementById("grafico-usuarios")?.getContext("2d");
    if (!ctx) return;

    try {
        const res = await fetch("/api/admin/usuarios-por-mes");
        const dados = await res.json();

        const labels = dados.map(item => `${item.mes}/${item.ano}`);
        const totais = dados.map(item => item.total);

        new Chart(ctx, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [{
                    label: "Usuários por Mês",
                    data: totais,
                    backgroundColor: "#0077cc"
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    title: {
                        display: true,
                        text: "Crescimento de Usuários por Mês"
                    },
                    legend: {
                        display: false
                    }
                },
                scales: {
                    x: { title: { display: true, text: "Mês/Ano" } },
                    y: { title: { display: true, text: "Total de Usuários" } }
                }
            }
        });

    } catch (err) {
        console.error("Erro ao carregar gráfico de usuários:", err);
    }
});
