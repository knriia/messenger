from app.database.repositories.chat import ChatRepository
from app.database.repositories.chat_member import ChatMemberRepository


class ChatManagementService:
    def __init__(self, chat_repo: ChatRepository, member_repo: ChatMemberRepository):
        self.chat_repo = chat_repo
        self.member_repo = member_repo

    async def get_or_create_private_chat(self, creator_id: int, target_id: int):
        user_ids = sorted({creator_id, target_id})
        chat = await self.chat_repo.get_private_chat_by_hash(user_ids=user_ids)
        if chat:
            return chat

        try:
            chat = await self.chat_repo.create_chat(
                creator_id=creator_id,
                chat_type="private",
                user_ids=user_ids
            )

            for u_id in user_ids:
                await self.member_repo.add_chat_member(chat_id=chat.id, user_id=u_id)

            await self.chat_repo.session.commit()
            await self.chat_repo.session.refresh(chat)
            return chat

        except Exception as e:
            await self.chat_repo.session.rollback()
            raise e
