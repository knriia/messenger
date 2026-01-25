const clientId = Math.floor(Math.random() * 10000);
const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
const ws = new WebSocket(`${protocol}//${window.location.host}/ws/${clientId}`);

const messagesContainer = document.getElementById('messages');
const chatForm = document.getElementById('chat-form');
const messageInput = document.getElementById('messageText');

ws.onmessage = (event) => {
    const div = document.createElement('div');
    div.className = 'msg-item';
    div.textContent = event.data;

    // Простая проверка: если сообщение начинается с нашего ID, можно стилизовать иначе
    if (event.data.includes(`ID ${clientId}:`)) {
        div.classList.add('my-message');
    }

    messagesContainer.appendChild(div);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
};

chatForm.onsubmit = (e) => {
    e.preventDefault();
    const text = messageInput.value.trim();
    if (text) {
        ws.send(text);
        messageInput.value = '';
    }
};