const chatContainer = document.getElementById('chatContainer');
const input = document.getElementById('input');
const sendBtn = document.getElementById('sendBtn');

let mode = 'menu';
let sessionId = null;

const menuText = `Bem-vindo ao Chat de Suporte! 

Por favor, escolha uma das opções abaixo digitando o número correspondente:

1. Horário de funcionamento
2. Como resetar a senha
3. Chat livre com IA (Gemini)
4. Sair`;

function generateSessionId() {
    return 'session_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
}

function addMessage(text, isUser = false) {
    const msgDiv = document.createElement('div');
    msgDiv.className = `flex ${isUser ? 'justify-end' : 'justify-start'}`;
    msgDiv.text = 'Digitando...'

    const bubble = document.createElement('div');
    bubble.className = isUser
        ? 'bg-gray-500 text-white px-4 py-3 rounded-lg max-w-xs md:max-w-md lg:max-w-lg shadow-lg whitespace-pre-wrap'
        : 'bg-gray-100 text-gray-800 px-4 py-3 rounded-lg max-w-xs md:max-w-md lg:max-w-lg shadow-lg whitespace-pre-wrap border';
    bubble.textContent = text;

    msgDiv.appendChild(bubble);
    chatContainer.appendChild(msgDiv);
    chatContainer.scrollTo({
        top: chatContainer.scrollHeight,
        behavior: 'smooth'
    });

    return bubble;
}

function addUserMessage(text) {
    return addMessage(text, true);
}

function addBotMessage(text) {
    return addMessage(text, false);
}

function handleSend(msg) {
    if (mode === 'ended') return;

    if (mode === 'menu') {
        const num = parseInt(msg);
        if (num === 1) {
            addBotMessage('📅 **Horário de funcionamento:**\nSegunda a sexta-feira, das 9h às 18h.\nSábados, das 9h às 13h.');
            addBotMessage(menuText);
        } else if (num === 2) {
            addBotMessage('🔑 **Como resetar a senha:**\n1. Acesse a página de login.\n2. Clique em \"Esqueci minha senha\".\n3. Insira seu e-mail cadastrado.\n4. Siga as instruções enviadas para seu e-mail.');
            addBotMessage(menuText);
        } else if (num === 3) {
            addBotMessage('🚀 Perfeito! Iniciando o chat livre com nossa IA Gemini. Pode fazer qualquer pergunta agora!');
            sessionId = generateSessionId();
            mode = 'chat';
            input.placeholder = 'Digite sua mensagem... (Enter para enviar)';
        } else if (num === 4) {
            addBotMessage('👋 Obrigado por usar nosso chat de suporte! Tenha um ótimo dia!');
            input.disabled = true;
            sendBtn.disabled = true;
            sendBtn.textContent = 'Chat Encerrado';
            sendBtn.classList.remove('bg-gray-500', 'hover:bg-gray-600');
            sendBtn.classList.add('bg-gray-400');
            mode = 'ended';
        } else {
            addBotMessage('❌ Opção inválida. Por favor, digite 1, 2, 3 ou 4.');
            addBotMessage(menuText);
        }
    } else if (mode === 'chat') {
        addUserMessage(msg);
        const responseBot = addBotMessage('Digitando...')

        input.disabled = true;
        sendBtn.disabled = true;
        sendBtn.textContent = 'Enviando...';

        fetch('http://localhost:5000/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                message: msg,
                session_id: sessionId
            })
        })
        .then(response => response.json())
        .then(data => {
            responseBot.textContent = data.response || data.message || 'Não houve resposta.';
            responseBot.scrollIntoView({
                behavior: 'smooth',
                block: "start"
            });

            input.disabled = false;
            sendBtn.disabled = false;
            sendBtn.textContent = 'Enviar';
            input.focus();
        })
        .catch(error => {
            responseBot.textContent = '❌ Desculpe, ocorreu um erro ao conectar com a IA. Verifique sua conexão e tente novamente.';
            responseBot.scrollIntoView({
                behavior: 'smooth',
                block: "start"
            });
            
            input.disabled = false;
            sendBtn.disabled = false;
            sendBtn.textContent = 'Enviar';
            input.focus();
        });
    }
}

// Event listeners
input.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        const msg = input.value.trim();
        if (msg) {
            input.value = '';
            handleSend(msg);
        }
    }
});

sendBtn.addEventListener('click', () => {
    const msg = input.value.trim();
    if (msg) {
        input.value = '';
        handleSend(msg);
    }
});

// Inicialização
document.addEventListener('DOMContentLoaded', () => {
    addBotMessage(menuText);
    input.focus();
});