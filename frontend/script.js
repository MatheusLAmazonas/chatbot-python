const chatContainer = document.getElementById('chatContainer');
const input = document.getElementById('input');
const sendBtn = document.getElementById('sendBtn');

let mode = 'menu';
let sessionId = null;

const menuText = `Bem-vindo ao Chat de Suporte! 

Por favor, escolha uma das opções abaixo digitando o número correspondente:

1. Chat livre com IA
2. Problemas com o Login
3. Problemas com o Cadastro
4. Redefinir minha Senha 
5. Sair`;

function generateSessionId() {
    return 'session_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
}

function enviarParaIA(pergunta, mostrarMenu = false) {
  const responseBot = addBotMessage('Digitando...');

  fetch('http://localhost:5000/chat', {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json',
      },
      body: JSON.stringify({
          message: pergunta,
          session_id: sessionId
      })
  })
  .then(response => response.json())
  .then(data => {
      responseBot.textContent = data.response || data.message || 'Não houve resposta.';
      responseBot.scrollIntoView({
          behavior: 'smooth',
          block: "start"
      })

      if (mostrarMenu) {
        setTimeout(() => {
            addBotMessage(menuText)
        }, 600);
      }

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
      })

      if (mostrarMenu) {
        addBotMessage(menuText)
      }
      
      input.disabled = false;
      sendBtn.disabled = false;
      sendBtn.textContent = 'Enviar';
      input.focus();
  })
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
            addUserMessage("Quero tirar dúvidas com a IA!")
            addBotMessage('🚀 Perfeito! Iniciando o chat livre com nossa IA. Pode fazer qualquer pergunta agora!');
            sessionId = generateSessionId();
            mode = 'chat';
            input.placeholder = 'Digite sua mensagem... (Enter para enviar)';
        } else if (num === 2) {
            addUserMessage("Estou tendo problemas com o Login...")
            enviarParaIA("Estou tendo problemas com o Login no Dice Tales (faça o tutorial para o login, e fale de forma sucinta o que pode estar causando o problema.)", true)
        } else if (num === 3) {
            addUserMessage("Estou tendo problemas com o Cadastro...")
            enviarParaIA("Estou tendo problemas com o Cadastro no Dice Tales (faça o tutorial sobre o cadastro, e fale de forma sucinta o que pode estar causando o problema.)", true)
        } else if (num === 4) {
            addUserMessage("Como posso resetar minha senha?")
            enviarParaIA("Como posso resetar minha senha no Dice Tales? (faça o tutorial de redefinir senha e fale sucintamente o que o usuário precisa saber.)", true)
        }else if (num === 5) {
            addUserMessage("Sair!")
            addBotMessage('👋 Obrigado por usar nosso chat de suporte! Tenha um ótimo dia!');

            input.disabled = true;
            sendBtn.disabled = true;
            sendBtn.textContent = 'Chat Encerrado';
            sendBtn.classList.remove('bg-gray-500', 'hover:bg-gray-600');
            sendBtn.classList.add('bg-gray-400');
            mode = 'ended';
        } else {
            addBotMessage('❌ Opção inválida. Por favor, digite 1, 2, 3, 4 ou 5.');
            addBotMessage(menuText);
        }
    } else if (mode === 'chat') {
        addUserMessage(msg);

        input.disabled = true;
        sendBtn.disabled = true;
        sendBtn.textContent = 'Enviando...';

        enviarParaIA(msg)
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