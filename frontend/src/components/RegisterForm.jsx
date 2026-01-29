import React, { useState } from 'react';
import './LoginForm.css';

const API_URL_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const RegisterForm = ({ onRegistrationSuccess, onBackToLogin }) => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [confirmPassword, setConfirmPassword] = useState('');
    const [error, setError] = useState('');
    const [message, setMessage] = useState(''); // Используем это состояние для условного рендера

    const handleRegister = async (e) => {
        e.preventDefault();
        setError('');
        setMessage('');

        if (password !== confirmPassword) {
            setError('Пароли не совпадают.');
            return;
        }

        try {
            const response = await fetch(`${API_URL_BASE}/auth/register`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    username: username,
                    password: password,
                }),
            });

            if (!response.ok) {
                throw new Error('Регистрация не удалась. Пользователь может уже существовать.');
            }

            // Устанавливаем сообщение об успехе, что изменит отображаемый UI
            setMessage('Вы успешно зарегистрировались!');
            // Удален setTimeout для автоматического перехода

        } catch (err) {
            setError(err.message || 'Регистрация не удалась.');
            console.error(err);
        }
    };

    // --- УСЛОВНЫЙ РЕНДЕРИНГ ---

    // Если сообщение об успехе установлено, показываем этот блок
    if (message) {
        return (
            <div className="login-container">
                <div className="login-form">
                    <h1>Успех!</h1>
                    <p style={{ color: 'green', marginBottom: '1rem' }}>
                        {message}
                    </p>
                    {/* Явная ссылка/кнопка для перехода к логину */}
                    <button onClick={onBackToLogin}>
                        Войти
                    </button>
                </div>
            </div>
        );
    }

    // Иначе показываем форму регистрации
    return (
        <div className="login-container">
            <form onSubmit={handleRegister} className="login-form">
                <h1>Регистрация нового аккаунта</h1>
                <input
                    type="text"
                    placeholder="Имя пользователя"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                    required
                />
                <input
                    type="password"
                    placeholder="Пароль"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    required
                />
                <input
                    type="password"
                    placeholder="Подтвердите пароль"
                    value={confirmPassword}
                    onChange={(e) => setConfirmPassword(e.target.value)}
                    required
                />

                <button type="submit">Зарегистрироваться</button>
                {error && <p className="login-error">{error}</p>}

                <p style={{ marginTop: '1rem' }}>
                    Уже есть аккаунт?{' '}
                    <a href="#" onClick={(e) => { e.preventDefault(); onBackToLogin(); }}>Войти</a>
                </p>
            </form>
        </div>
    );
};

export default RegisterForm;
