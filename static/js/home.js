// static/js/home.js
document.addEventListener("DOMContentLoaded", () => {
    // 1. Efeito de aparição suave (Fade-in on Scroll)
    const secoes = document.querySelectorAll(".hero, .vantagens, .destaques-home, .chamada-final");

    secoes.forEach((secao) => {
        secao.classList.add("fade-in-section");
    });

    const observador = new IntersectionObserver(
        (entries, observer) => {
            entries.forEach((entry) => {
                if (entry.isIntersecting) {
                    entry.target.classList.add("is-visible");
                    observer.unobserve(entry.target);
                }
            });
        },
        { threshold: 0.15 }
    );

    secoes.forEach((secao) => observador.observe(secao));

    // 2. Tornar o card inteiro de categoria clicável
    const cards = document.querySelectorAll(".categoria-card");
    cards.forEach((card) => {
        card.addEventListener("click", (e) => {
            const link = card.querySelector("a");
            if (link && e.target !== link) {
                link.click();
            }
        });
    });
});