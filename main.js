$(document).ready(function () {
    var chatLog = document.getElementById('chat-log');
    var form = document.getElementById('composer');
    var input = document.getElementById('pergunta');
    var botaoEnviar = document.getElementById('perguntar');

    function rolarParaFinal() {
        chatLog.scrollTop = chatLog.scrollHeight;
    }

    function adicionarMensagem(texto, autor) {
        var row = document.createElement('div');
        row.className = 'msg-row ' + autor;

        var avatar = document.createElement('div');
        avatar.className = 'msg-avatar';
        avatar.innerHTML = autor === 'bot'
            ? '<i class="ph-fill ph-robot"></i>'
            : '<i class="ph-fill ph-user"></i>';

        var bubble = document.createElement('div');
        bubble.className = 'bubble';
        bubble.textContent = texto;

        row.appendChild(avatar);
        row.appendChild(bubble);
        chatLog.appendChild(row);
        rolarParaFinal();

        return row;
    }

    function mostrarDigitando() {
        var row = document.createElement('div');
        row.className = 'msg-row bot';
        row.id = 'typing-indicator';

        var avatar = document.createElement('div');
        avatar.className = 'msg-avatar';
        avatar.innerHTML = '<i class="ph-fill ph-robot"></i>';

        var bubble = document.createElement('div');
        bubble.className = 'bubble';
        bubble.innerHTML = '<div class="typing-dots"><span></span><span></span><span></span></div>';

        row.appendChild(avatar);
        row.appendChild(bubble);
        chatLog.appendChild(row);
        rolarParaFinal();
    }

    function removerDigitando() {
        var indicador = document.getElementById('typing-indicator');
        if (indicador) indicador.remove();
    }

    // Mensagem inicial de boas-vindas
    adicionarMensagem(
        "Olá! Eu sou o sistema MAAM. Por favor, digite sua pergunta ou 'Tchau' para encerrar a nossa conversa.",
        'bot'
    );

    form.addEventListener('submit', function (event) {
        event.preventDefault();

        var pergunta = input.value.trim();
        if (!pergunta) return;

        adicionarMensagem(pergunta, 'user');
        input.value = '';
        input.focus();
        botaoEnviar.disabled = true;
        mostrarDigitando();

        $.ajax({
            url: 'conectChat.php',
            method: 'post',
            dataType: 'json',
            data: { pergunta: pergunta },
            success: function (data) {
                removerDigitando();
                if (data && data !== 'error') {
                    adicionarMensagem(data, 'bot');
                } else {
                    adicionarMensagem('Desculpe, ocorreu um erro ao processar sua pergunta.', 'bot');
                }
            },
            error: function (xhr, status, error) {
                console.log(xhr.responseText);
                removerDigitando();
                adicionarMensagem('Não consegui me conectar ao servidor. Tente novamente.', 'bot');
            },
            complete: function () {
                botaoEnviar.disabled = false;
            }
        });
    });
});
