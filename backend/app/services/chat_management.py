from app.domain.consts import UserRole
from app.domain.entities.chat_entity import PrivateChatEntity
from app.domain.interfaces.uow import IUnitOfWork


class ChatManagementService:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    async def get_or_create_private_chat(self, creator_id: int, target_id: int) -> PrivateChatEntity:
        user_ids = sorted({creator_id, target_id})
        async with self.uow:
            chat = await self.uow.chats.get_private_chat_by_hash(user_ids=user_ids)
            if chat:
                return chat
            chat = await self.uow.chats.create_private_chat(creator_id=creator_id, user_ids=user_ids)

            for u_id in user_ids:
                role = UserRole.OWNER if u_id == creator_id else UserRole.MEMBER
                await self.uow.members.add_chat_member(chat_id=chat.id, user_id=u_id, role=role)

            await self.uow.commit()

            return chat
