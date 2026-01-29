import React, { useState } from 'react';
import './LoginForm.css'; // Импортируем стили

const API_URL_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000';

// Оставьте ТОЛЬКО этот блок
const LoginForm = ({ onLoginSuccess, onSwitchToRegister }) => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');

    const handleLogin = async (e) => {
        e.preventDefault();
        setError('');
        try {
            const response = await fetch(`${API_URL_BASE}/auth/login`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: new URLSearchParams({
                    username: username,
                    password: password,
                }),
            });

            if (!response.ok) {
                throw new Error('Login failed');
            }

            const data = await response.json();
            onLoginSuccess(data.access_token);
        } catch (err) {
            setError('Login failed. Check credentials.');
            console.error(err);
        }
    };

    return (
        <div className="login-container">
            <form onSubmit={handleLogin} className="login-form">
                <h1>Войти в мессенджер</h1>
                <input type="text" placeholder="Имя пользователя" value={username} onChange={(e) => setUsername(e.target.value)} required />
                <input type="password" placeholder="Пароль" value={password} onChange={(e) => setPassword(e.target.value)} required />
                <button type="submit">Вход</button>

                {error && <p className="login-error">{error}</p>}

                {/* Эта ссылка использует onSwitchToRegister */}
                <p style={{ marginTop: '1rem' }}>
                    Нет аккаунта?{' '}
                    <a href="#" onClick={(e) => { e.preventDefault(); onSwitchToRegister(); }}>Регистрация</a>
                </p>
            </form>
        </div>
    );
};

export default LoginForm;
