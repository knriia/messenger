messenger/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   ├── endpoints/
│   │   │   │   └── v1/
│   │   │   │       ├── auth.py
│   │   │   │       ├── chat.py
│   │   │   │       ├── messages.py
│   │   │   │       ├── users.py
│   │   │   │       └── websocket.py
│   │   │   ├── dependencies.py
│   │   │   └── lifespan.py
│   │   ├── core/
│   │   │   └── config.py
│   │   ├── di/
│   │   │   ├── providers/
│   │   │   │   ├── chat_provider.py
│   │   │   │   ├── config_provider.py
│   │   │   │   ├── db_provider.py
│   │   │   │   ├── kafka_provider.py
│   │   │   │   ├── message_provider.py
│   │   │   │   ├── redis_provider.py
│   │   │   │   └── user_provider.py
│   │   │   └── container.py
│   │   ├── domain/
│   │   │   ├── entities/
│   │   │   │   ├── chat_entity.py
│   │   │   │   ├── message_entity.py
│   │   │   │   ├── token.py
│   │   │   │   └── user_entity.py
│   │   │   ├── exceptions/
│   │   │   │   ├── auth.py
│   │   │   │   ├── base.py
│   │   │   │   └── security.py
│   │   │   ├── interfaces/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── broker.py
│   │   │   │   ├── chat_member_repo.py
│   │   │   │   ├── chat_repo.py
│   │   │   │   ├── message_repo.py
│   │   │   │   ├── processor.py
│   │   │   │   ├── security.py
│   │   │   │   ├── uow.py
│   │   │   │   └── user_repo.py
│   │   │   ├── __init__.py
│   │   │   ├── consts.py
│   │   │   └── logic.py
│   │   ├── infrastructure/
│   │   │   ├── kafka/
│   │   │   │   ├── consumer/
│   │   │   │   │   └── message.py
│   │   │   │   └── producer/
│   │   │   │       └── message.py
│   │   │   ├── postgres/
│   │   │   │   ├── mappers/
│   │   │   │   │   ├── chat_mapper.py
│   │   │   │   │   ├── message_mapper.py
│   │   │   │   │   └── user_mapper.py
│   │   │   │   ├── migrations/
│   │   │   │   │   ├── versions/
│   │   │   │   │   │   ├── 6bcc8602dab8_init.py
│   │   │   │   │   │   └── __init__.py
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   ├── alembic.ini
│   │   │   │   │   ├── env.py
│   │   │   │   │   ├── README
│   │   │   │   │   └── script.py.mako
│   │   │   │   ├── models/
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   ├── base.py
│   │   │   │   │   ├── chat.py
│   │   │   │   │   ├── chat_member.py
│   │   │   │   │   ├── message.py
│   │   │   │   │   └── user.py
│   │   │   │   ├── repositories/
│   │   │   │   │   ├── chat_member_repo.py
│   │   │   │   │   ├── chat_repo.py
│   │   │   │   │   ├── message_repo.py
│   │   │   │   │   └── user_repo.py
│   │   │   │   ├── session.py
│   │   │   │   └── uow.py
│   │   │   └── redis/
│   │   │       └── listener.py
│   │   ├── schemas/
│   │   │   ├── chat.py
│   │   │   ├── message.py
│   │   │   ├── notification.py
│   │   │   ├── token.py
│   │   │   └── user.py
│   │   ├── services/
│   │   │   ├── auth.py
│   │   │   ├── chat_management.py
│   │   │   ├── connection_manager.py
│   │   │   ├── message.py
│   │   │   ├── message_handler.py
│   │   │   ├── security.py
│   │   │   └── user.py
│   │   ├── __init__.py
│   │   ├── main.py
│   │   └── worker.py
│   ├── Dockerfile
│   └── requirements.txt
├── deploy/
│   ├── docker-compose.apps.yml
│   ├── docker-compose.db.yml
│   └── docker-compose.infra.yml
├── frontend/
│   ├── public/
│   │   └── vite.svg
│   ├── src/
│   │   ├── assets/
│   │   │   └── react.svg
│   │   ├── components/
│   │   │   ├── ChatRoom.css
│   │   │   ├── ChatRoom.jsx
│   │   │   ├── LoginForm.css
│   │   │   ├── LoginForm.jsx
│   │   │   └── RegisterForm.jsx
│   │   ├── App.css
│   │   ├── App.jsx
│   │   ├── index.css
│   │   └── main.jsx
│   ├── Dockerfile
│   ├── eslint.config.js
│   ├── index.html
│   ├── package-lock.json
│   ├── package.json
│   ├── README.md
│   └── vite.config.js
├── docker-compose.yml
├── generate_tree.py
├── Makefile
├── pyproject.toml
└── structure.md
