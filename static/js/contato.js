// static/js/contato.js
document.addEventListener("DOMContentLoaded", () => {
    // 1. Efeito Fade-in on Scroll
    const secoes = document.querySelectorAll(".contato-hero, .contato-info, .contato-form-container");
    secoes.forEach((secao) => secao.classList.add("fade-in-section"));

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

    // 2. Contador dinâmico de caracteres da mensagem
    const campoMensagem = document.getElementById("mensagem");
    const contadorTexto = document.getElementById("contador-caracteres");
    const maxChars = 500;

    if (campoMensagem && contadorTexto) {
        campoMensagem.addEventListener("input", () => {
            const restante = maxChars - campoMensagem.value.length;
            contadorTexto.textContent = `${restante} caracteres restantes`;
        });
    }

    // 3. Máscara interactiva de telefone / telemóvel
    const campoTelefone = document.getElementById("telefone");
    if (campoTelefone) {
        campoTelefone.addEventListener("input", (e) => {
            let v = e.target.value.replace(/\D/g, "");
            if (v.length > 11) v = v.slice(0, 11);

            if (v.length > 10) {
                // Formato telemóvel: (XX) XXXXX-XXXX
                e.target.value = v.replace(/^(\d{2})(\d{5})(\d{4})/, "($1) $2-$3");
            } else if (v.length > 5) {
                // Formato fixo: (XX) XXXX-XXXX
                e.target.value = v.replace(/^(\d{2})(\d{4})(\d{0,4})/, "($1) $2-$3");
            } else if (v.length > 2) {
                e.target.value = v.replace(/^(\d{2})(\d{0,5})/, "($1) $2");
            } else {
                e.target.value = v;
            }
        });
    }

    // 4. Feedback no envio do formulário
    const formContato = document.getElementById("form-contato");
    const btnEnviar = document.getElementById("btn-enviar");
    const feedbackBox = document.getElementById("feedback-envio");

    if (formContato && btnEnviar && feedbackBox) {
        formContato.addEventListener("submit", (e) => {
            btnEnviar.disabled = true;
            btnEnviar.textContent = "A enviar mensagem...";

            // Se o formulário não submeter via Django nativo (POST com reload), simula confirmação:
            if (!formContato.getAttribute("action")) {
                e.preventDefault();
                setTimeout(() => {
                    feedbackBox.className = "mensagem-feedback sucesso";
                    feedbackBox.textContent = "Mensagem enviada com sucesso! Entraremos em contacto brevemente.";
                    formContato.reset();
                    if (contadorTexto) contadorTexto.textContent = `${maxChars} caracteres restantes`;
                    btnEnviar.disabled = false;
                    btnEnviar.textContent = "Enviar Mensagem";
                }, 1000);
            }
        });
    }
});