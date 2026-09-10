<!DOCTYPE html>
<html lang="pt-br">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <script src="https://code.jquery.com/jquery-1.9.1.js"></script>
    <script src="https://unpkg.com/@phosphor-icons/web"></script>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
    <link rel="icon" href="View/icon.svg" type="image/svg+xml">
    <link rel="stylesheet" href="View/style.css">
    <title>ChatBot Guarani</title>
</head>

<body>

    <div id="chat-card">

        <header id="chat-header">
            <div id="avatar">
                <i class="ph-fill ph-robot"></i>
            </div>
            <div id="header-info">
                <h1>ChatBot Guarani</h1>
                <p><span id="status-dot"></span> Assistente virtual · Online</p>
            </div>
        </header>

        <div id="chat-log" aria-live="polite"></div>

        <form id="composer">
            <input
                type="text"
                id="pergunta"
                placeholder="Digite sua pergunta..."
                autocomplete="off"
            >
            <button type="submit" id="perguntar" title="Enviar">
                <i class="ph-fill ph-paper-plane-right"></i>
            </button>
        </form>

    </div>

</body>

<script src="main.js"></script>

</html>
