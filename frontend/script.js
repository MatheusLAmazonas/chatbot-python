const chatContainer = document.getElementById('chatContainer');
const input = document.getElementById('input');
const sendBtn = document.getElementById('sendBtn');

let mode = 'menu';
let sessionId = null;
let currentPromptType = 'estruturado';
let currentMode = 'suporte';

const menuText = `Bem-vindo ao Chat de Suporte! 

Por favor, escolha uma das opções abaixo digitando o número correspondente:

1. Chat livre com IA (Gemini)
2. Problemas com o Login
3. Problemas com o Cadastro
4. Redefinir minha Senha
5. Dúvidas sobre D&D (Classes, Raças, Regras)
6. Sair`;

function generateSessionId() {
    return 'session_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
}

function enviarParaIA(pergunta, mostrarMenu = false, promptType = null, modeParam = null) {
    const responseBot = addBotMessage('Digitando...');

    const payload = {
        message: pergunta,
        session_id: sessionId
    };

    if (promptType) payload.prompt_type = promptType;
    if (modeParam) payload.mode = modeParam;

    fetch('http://localhost:5000/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload)
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            responseBot.textContent = '❌ ' + data.error;
        } else {
            responseBot.textContent = data.response || data.message || 'Não houve resposta.';
            
            if (data.type === 'dnd') {
                const msgDiv = responseBot.parentElement;
                const indicator = document.createElement('span');
                indicator.className = 'text-xs bg-purple-200 text-purple-800 px-2 py-1 rounded ml-2 inline-block';
                indicator.textContent = '🎲 D&D 5e';
                msgDiv.querySelector('.bg-gray-100').appendChild(indicator);
            }
        }
        
        responseBot.scrollIntoView({
            behavior: 'smooth',
            block: "start"
        });

        if (mostrarMenu) {
            setTimeout(() => {
                addBotMessage(menuText);
            }, 600);
        }

        input.disabled = false;
        sendBtn.disabled = false;
        sendBtn.textContent = 'Enviar';
        input.focus();
    })
    .catch(error => {
        console.log(error);
        responseBot.textContent = '❌ Desculpe, ocorreu um erro ao conectar com a IA. Verifique se o servidor está rodando em http://localhost:5000';
        responseBot.scrollIntoView({
            behavior: 'smooth',
            block: "start"
        });

        if (mostrarMenu) {
            addBotMessage(menuText);
        }
        
        input.disabled = false;
        sendBtn.disabled = false;
        sendBtn.textContent = 'Enviar';
        input.focus();
    });
}

function addMessage(text, isUser = false) {
    const msgDiv = document.createElement('div');
    msgDiv.className = `flex ${isUser ? 'justify-end' : 'justify-start'}`;

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
            addUserMessage("Quero tirar dúvidas com a IA!");
            addBotMessage('🚀 Perfeito! Iniciando o chat livre com nossa IA Gemini. Pode fazer qualquer pergunta agora!\n\nDica: Você pode perguntar sobre D&D também!');
            sessionId = generateSessionId();
            mode = 'chat';
            currentMode = 'suporte';
            currentPromptType = 'estruturado';
            input.placeholder = 'Digite sua mensagem... (Enter para enviar)';
        } else if (num === 2) {
            addUserMessage("Estou tendo problemas com o Login...");
            enviarParaIA("Estou tendo problemas com o Login no Dice Tales (faça o tutorial para o login, e fale de forma sucinta o que pode estar causando o problema.)", true);
        } else if (num === 3) {
            addUserMessage("Estou tendo problemas com o Cadastro...");
            enviarParaIA("Estou tendo problemas com o Cadastro no Dice Tales (faça o tutorial sobre o cadastro, e fale de forma sucinta o que pode estar causando o problema.)", true);
        } else if (num === 4) {
            addUserMessage("Como posso resetar minha senha?");
            enviarParaIA("Como posso resetar minha senha no Dice Tales? (faça o tutorial de redefinir senha e fale sucintamente o que o usuário precisa saber.)", true);
        } else if (num === 5) {
            addUserMessage("Tenho dúvidas sobre D&D!");
            addBotMessage('🎲 **Modo D&D Ativado!**\n\nVocê pode perguntar sobre:\n• Classes (Bárbaro, Mago, Guerreiro, etc.)\n• Raças (Elfo, Anão, Halfling, etc.)\n• Regras e mecânicas\n• Magias e habilidades\n\nDigite sua pergunta sobre D&D e usarei a API oficial da D&D 5e para responder!\n\n(Para voltar ao menu principal, digite "/menu")');
            sessionId = generateSessionId();
            mode = 'chat';
            currentMode = 'professor';
            currentPromptType = 'estruturado';
            input.placeholder = 'Digite sua pergunta sobre D&D...';
        } else if (num === 6) {
            addUserMessage("Sair!");
            addBotMessage('👋 Obrigado por usar nosso chat de suporte! Tenha um ótimo dia!');

            input.disabled = true;
            sendBtn.disabled = true;
            sendBtn.textContent = 'Chat Encerrado';
            sendBtn.classList.remove('bg-gray-500', 'hover:bg-gray-600');
            sendBtn.classList.add('bg-gray-400');
            mode = 'ended';
        } else {
            addBotMessage('❌ Opção inválida. Por favor, digite 1, 2, 3, 4, 5 ou 6.');
            addBotMessage(menuText);
        }
    } else if (mode === 'chat') {
        if (msg.toLowerCase() === '/menu') {
            addUserMessage("/menu");
            addBotMessage('🔙 Retornando ao menu principal...');
            addBotMessage(menuText);
            mode = 'menu';
            input.placeholder = 'Digite 1, 2, 3, 4, 5 ou 6...';
            return;
        }
        
        addUserMessage(msg);

        input.disabled = true;
        sendBtn.disabled = true;
        sendBtn.textContent = 'Enviando...';

        enviarParaIA(msg, false, currentPromptType, currentMode);
    }
}

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

document.addEventListener('DOMContentLoaded', () => {
    addBotMessage(menuText);
    input.focus();
});