from app.domain.consts import ChatType
from app.database.uow import UnitOfWork


class ChatManagementService:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    async def get_or_create_private_chat(self, creator_id: int, target_id: int):
        user_ids = sorted({creator_id, target_id})
        chat = await self.uow.chats.get_private_chat_by_hash(user_ids=user_ids)
        if chat:
            return chat

        try:
            chat = await self.uow.chats.create_chat(
                creator_id=creator_id,
                chat_type=ChatType.PRIVATE,
                user_ids=user_ids
            )

            for u_id in user_ids:
                await self.uow.members.add_chat_member(chat_id=chat.id, user_id=u_id)

            await self.uow.commit()
            await self.uow.refresh(chat)
            return chat

        except Exception as e:
            await self.uow.rollback()
            raise e
