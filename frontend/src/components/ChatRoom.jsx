import React, { useState, useEffect, useRef } from 'react';
import './ChatRoom.css'; // Импортируем стили

const API_URL_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const ChatRoom = ({ token }) => {
    const [messages, setMessages] = useState([]);
    const [inputMessage, setInputMessage] = useState('');
    const ws = useRef(null);
    const messagesEndRef = useRef(null); // Для автопрокрутки
    const messageIdCounter = useRef(0); // Счетчик для ID

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    };

    useEffect(scrollToBottom, [messages]);

    useEffect(() => {
        if (!token) return;

        const wsUrl = `${API_URL_BASE.replace('http', 'ws')}/ws?token=${token}`;
        ws.current = new WebSocket(wsUrl);

        ws.current.onopen = () => {
            setMessages(prev => [...prev, {
                id: messageIdCounter.current++,
                type: 'status',
                text: 'Connected to chat room'
            }]);
        };

        ws.current.onmessage = (event) => {
            const data = JSON.parse(event.data);
            setMessages(prev => [...prev, {
                id: messageIdCounter.current++,
                type: 'message',
                text: data.message
            }]);
        };

        ws.current.onclose = () => {
            console.log('WebSocket Disconnected');
            setMessages(prev => [...prev, {
                id: messageIdCounter.current++,
                type: 'status',
                text: 'Disconnected from chat room'
            }]);
        };

        return () => {
            if (ws.current && ws.current.readyState === WebSocket.OPEN) {
                ws.current.close();
            }
        };
    }, [token]);

    const sendMessage = (e) => {
        e.preventDefault();
        if (ws.current && inputMessage.trim() !== '' && ws.current.readyState === WebSocket.OPEN) {
            // Отправляем JSON-строку в FastAPI
            ws.current.send(JSON.stringify({ message: inputMessage }));
            setInputMessage('');
        }
    };

    return (
        <div className="chat-container">
            <header className="chat-header">
                WebSocket Chat Room
            </header>
            <div className="chat-messages">
                {messages.map((msg) => (
                    <div key={msg.id} className={msg.type === 'status' ? 'message-status' : 'message-text'}>
                        {msg.text}
                    </div>
                ))}
                 <div ref={messagesEndRef} /> {/* Пустой div для прокрутки */}
            </div>
            <form onSubmit={sendMessage} className="chat-form">
                <input
                    type="text"
                    value={inputMessage}
                    onChange={(e) => setInputMessage(e.target.value)}
                    placeholder="Type a message..."
                />
                <button type="submit">Send</button>
            </form>
        </div>
    );
};

export default ChatRoom;