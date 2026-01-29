import { useState } from 'react';
import './App.css';
import LoginForm from './components/LoginForm.jsx';
import RegisterForm from './components/RegisterForm.jsx'; // Импортируем новую форму
import ChatRoom from './components/ChatRoom.jsx';

function App() {
  const [token, setToken] = useState(null);
  // Добавляем состояние для отслеживания текущего вида: 'login', 'register', или 'chat'
  const [view, setView] = useState('login');

  const handleLoginSuccess = (receivedToken) => {
    setToken(receivedToken);
    setView('chat'); // Переключаемся на чат после успешного входа
  };

  // Функция для возврата на логин после регистрации
  const handleBackToLogin = () => {
    setView('login');
  };

  // Функция для перехода на форму регистрации из логина
  const handleSwitchToRegister = () => {
    setView('register');
  };

  // Логика условного рендеринга
  if (token && view === 'chat') {
    return <ChatRoom token={token} />;
  } else if (view === 'register') {
    return <RegisterForm onRegistrationSuccess={handleLoginSuccess} onBackToLogin={handleBackToLogin} />;
  } else {
    // Показываем форму логина по умолчанию
    return <LoginForm onLoginSuccess={handleLoginSuccess} onSwitchToRegister={handleSwitchToRegister} />;
  }
}

export default App;
