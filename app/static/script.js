let ws = null;
let isLoginMode = true; // Отслеживает текущий режим: true = Логин, false = Регистрация

// Функция для переключения между логином и регистрацией (визуально меняет текст)
function toggleAuthMode() {
    isLoginMode = !isLoginMode;
    const title = document.getElementById('auth-title');
    const subtitle = document.getElementById('auth-subtitle');
    const btn = document.getElementById('main-auth-btn');
    const toggleBtn = document.getElementById('toggle-btn');
    const toggleText = document.getElementById('toggle-text');

    if (isLoginMode) {
        title.textContent = "С возвращением";
        subtitle.textContent = "Войдите в свой аккаунт";
        btn.textContent = "Войти";
        toggleText.textContent = "Нет аккаунта?";
        toggleBtn.textContent = "Создать профиль";
    } else {
        title.textContent = "Регистрация";
        subtitle.textContent = "Присоединяйтесь к нам сегодня";
        btn.textContent = "Зарегистрироваться";
        toggleText.textContent = "Уже есть аккаунт?";
        toggleBtn.textContent = "Войти";
    }
}

// Функция-обертка, вызываемая по нажатию главной кнопки "Войти/Зарегистрироваться"
async function handleAuth() {
    const type = isLoginMode ? 'login' : 'register';
    await auth(type);
}

// Основная функция аутентификации, отправляет запросы на бэкенд
async function auth(type) {
    const usernameInput = document.getElementById('username');
    const passwordInput = document.getElementById('password');
    const username = usernameInput.value;
    const password = passwordInput.value;

    if (!username || !password) return alert("Заполните поля");

    try {
        if (type === 'register') {
            const resp = await fetch('/auth/register', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({ username, password })
            });

            if (resp.ok) {
                alert("Регистрация успешна! Теперь войдите.");
                // Автоматически переключаемся на форму входа и очищаем поля
                toggleAuthMode();
                usernameInput.value = '';
                passwordInput.value = '';
            } else {
                alert("Ошибка регистрации");
            }
            return;
        }

        // Логин: FastAPI ожидает данные формы (FormData), а не JSON для OAuth2
        const formData = new FormData();
        formData.append('username', username);
        formData.append('password', password);

        const resp = await fetch('/auth/login', {
            method: 'POST',
            body: formData
        });

        if (resp.ok) {
            const data = await resp.json();
            // Запускаем чат после успешного входа
            startChat(data.access_token, username);
        } else {
            alert("Неверный логин или пароль");
        }
    } catch (e) {
        console.error("Ошибка сети или сервера при аутентификации:", e);
        alert("Произошла ошибка при попытке подключения к серверу.");
    }
}

// Функция инициализации WebSocket и интерфейса чата
function startChat(token, username) {
    // Скрываем блок авторизации и показываем блок чата
    document.getElementById('auth-container').classList.add('d-none');
    // При условии, что вы вернули классы Bootstrap в index.html или добавили их вручную
    if (document.getElementById('chat-block')) {
        document.getElementById('chat-block').classList.remove('d-none');
    }
    document.getElementById('user-display').textContent = username;

    // Определяем протокол ws/wss в зависимости от текущего URL
    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    // Подключаемся к WebSocket, передавая токен как Query-параметр (как исправлено в FastAPI)
    ws = new WebSocket(`${protocol}//${window.location.host}/ws?token=${token}`);

    ws.onmessage = (event) => {
        const messagesContainer = document.getElementById('messages');
        const div = document.createElement('div');
        div.className = 'msg-item mb-2'; // Используем классы из style.css
        div.textContent = event.data;

        messagesContainer.appendChild(div);
        // Прокрутка вниз к новому сообщению
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    };

    ws.onclose = (event) => {
        console.log("Соединение WebSocket закрыто:", event.code, event.reason);
        alert("Соединение с чатом потеряно. Пожалуйста, войдите снова.");
        // Можно добавить логику для возврата на страницу авторизации
    };

    ws.onerror = (error) => {
        console.error("Ошибка WebSocket:", error);
        alert("Ошибка соединения WebSocket.");
    };
}

// Обработчик отправки сообщения через форму чата
if (document.getElementById('chat-form')) {
    document.getElementById('chat-form').onsubmit = (e) => {
        e.preventDefault();
        const input = document.getElementById('messageText');
        if (input.value && ws && ws.readyState === WebSocket.OPEN) {
            ws.send(input.value);
            input.value = '';
        }
    };
}