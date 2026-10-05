// static/js/catalogo.js
document.addEventListener("DOMContentLoaded", () => {
    // 1. Função auxiliar para obter o CSRF Token
    function getCsrfToken() {
        const inputCsrf = document.querySelector("input[name='csrfmiddlewaretoken']");
        if (inputCsrf) return inputCsrf.value;

        let cookieValue = null;
        if (document.cookie && document.cookie !== "") {
            const cookies = document.cookie.split(";");
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, 10) === "csrftoken=") {
                    cookieValue = decodeURIComponent(cookie.substring(10));
                    break;
                }
            }
        }
        return cookieValue;
    }

    // 2. Controlos de incremento e decremento (+ / -)
    const botoesStep = document.querySelectorAll(".btn-qty-step");
    botoesStep.forEach((botao) => {
        botao.addEventListener("click", () => {
            const acao = botao.getAttribute("data-action");
            const wrapper = botao.closest(".quantidade-wrapper");
            const inputQtd = wrapper.querySelector(".quantidade-input");
            let valorAtual = parseInt(inputQtd.value, 10) || 1;

            if (acao === "mais") {
                inputQtd.value = valorAtual + 1;
            } else if (acao === "menos" && valorAtual > 1) {
                inputQtd.value = valorAtual - 1;
            }
        });
    });

    // 3. Controle do Modal Toast (Canto Inferior Direito)
    const modal = document.getElementById("modal-carrinho");
    const btnFecharModal = document.getElementById("btn-fechar-modal");
    const btnContinuar = document.getElementById("btn-continuar-comprando");
    const modalNome = document.getElementById("modal-produto-nome");
    const modalInfo = document.getElementById("modal-produto-info");
    let timerModal = null;

    function fecharModal() {
        if (modal) modal.classList.remove("aberto");
        if (timerModal) clearTimeout(timerModal);
    }

    if (btnFecharModal) btnFecharModal.addEventListener("click", fecharModal);
    if (btnContinuar) btnContinuar.addEventListener("click", fecharModal);

    // 4. Adicionar ao Carrinho via JavaScript Puro (Sem Recarregar)
    const botoesAdicionar = document.querySelectorAll(".btn-adicionar");

    botoesAdicionar.forEach((botao) => {
        botao.addEventListener("click", async (e) => {
            e.preventDefault();

            const card = botao.closest(".produto-card");
            const inputQtd = card.querySelector(".quantidade-input");
            const quantidade = inputQtd ? inputQtd.value : "1";

            const idProduto = card.getAttribute("data-id");
            const nomeProduto = card.getAttribute("data-nome");
            const precoProduto = card.getAttribute("data-preco");
            const url = card.getAttribute("data-url");

            // Estado de carregamento no botão
            const textoOriginal = botao.innerHTML;
            botao.disabled = true;
            botao.innerHTML = "Adicionando...";

            const formData = new FormData();
            formData.append("produto_id", idProduto);
            formData.append("nome_produto", nomeProduto);
            formData.append("preco_produto", precoProduto);
            formData.append("quantidade", quantidade);

            try {
                const response = await fetch(url, {
                    method: "POST",
                    body: formData,
                    headers: {
                        "X-CSRFToken": getCsrfToken(),
                        "X-Requested-With": "XMLHttpRequest",
                    },
                });

                const data = await response.json();

                if (data.sucesso) {
                    botao.disabled = false;
                    botao.innerHTML = textoOriginal;

                    // Atualiza o contador vermelho com a regra de 99+
                    const badge = document.getElementById("carrinho-contador");
                    if (badge) {
                        const total = parseInt(data.total_itens, 10);
                        badge.textContent = total > 99 ? "99+" : total;
                        badge.classList.remove("oculto");

                        // Efeito de pulso suave
                        badge.classList.add("pulso");
                        setTimeout(() => badge.classList.remove("pulso"), 300);
                    }

                    // Exibe o Toast no canto inferior direito
                    if (modal && modalNome && modalInfo) {
                        modalNome.textContent = nomeProduto;
                        modalInfo.textContent = `${quantidade}x unidade(s) adicionada(s).`;
                        modal.classList.add("aberto");

                        // Fecha sozinho após 4 segundos se não houver interação
                        if (timerModal) clearTimeout(timerModal);
                        timerModal = setTimeout(() => {
                            fecharModal();
                        }, 4000);
                    }
                } else {
                    alert("Erro ao adicionar produto.");
                    botao.disabled = false;
                    botao.innerHTML = textoOriginal;
                }
            } catch (err) {
                console.error("Falha ao adicionar item:", err);
                botao.disabled = false;
                botao.innerHTML = textoOriginal;
            }
        });
    });

    // 5. Filtro de Busca Instantânea
    const campoBusca = document.getElementById("busca-produtos");
    const cardsProdutos = document.querySelectorAll(".produto-card");

    if (campoBusca) {
        campoBusca.addEventListener("input", (e) => {
            const termo = e.target.value.toLowerCase().trim();
            cardsProdutos.forEach((card) => {
                const titulo = card.querySelector("h2").textContent.toLowerCase();
                const descricao = card.querySelector(".produto-descricao").textContent.toLowerCase();
                card.style.display = (titulo.includes(termo) || descricao.includes(termo)) ? "flex" : "none";
            });
        });
    }
});