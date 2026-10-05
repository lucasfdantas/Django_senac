// static/js/sobre.js
document.addEventListener("DOMContentLoaded", () => {
    // 1. Efeito Fade-in on Scroll
    const secoes = document.querySelectorAll(".sobre-hero, .sobre-historia, .metricas-grid, .pilares-grid, .faq-secao");

    secoes.forEach((secao) => secao.classList.add("fade-in-section"));

    const observador = new IntersectionObserver(
        (entries, observer) => {
            entries.forEach((entry) => {
                if (entry.isIntersecting) {
                    entry.target.classList.add("is-visible");

                    // 2. Se a seção for a grade de métricas, dispara o contador numérico
                    if (entry.target.classList.contains("metricas-grid")) {
                        iniciarContadores();
                    }

                    observer.unobserve(entry.target);
                }
            });
        },
        { threshold: 0.15 }
    );

    secoes.forEach((secao) => observador.observe(secao));

    // Função para animar os números das métricas
    function iniciarContadores() {
        const contadores = document.querySelectorAll(".metrica-numero");
        contadores.forEach((contador) => {
            const alvo = +contador.getAttribute("data-alvo");
            let contagem = 0;
            const incremento = alvo / 40;

            const atualizar = () => {
                contagem += incremento;
                if (contagem < alvo) {
                    contador.textContent = Math.ceil(contagem).toLocaleString("pt-BR") + "+";
                    requestAnimationFrame(atualizar);
                } else {
                    contador.textContent = alvo.toLocaleString("pt-BR") + "+";
                }
            };
            atualizar();
        });
    }

    // 3. Acordeão interativo de Dúvidas / FAQ
    const faqItens = document.querySelectorAll(".faq-item");

    faqItens.forEach((item) => {
        const botao = item.querySelector(".faq-pergunta");
        botao.addEventListener("click", () => {
            const estaAtivo = item.classList.contains("ativo");

            // Fecha todos antes de abrir o clicado
            faqItens.forEach((i) => i.classList.remove("ativo"));

            if (!estaAtivo) {
                item.classList.add("ativo");
            }
        });
    });
});