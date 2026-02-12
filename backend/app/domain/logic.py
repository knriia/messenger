import hashlib


def generate_private_chat_hash(user_ids: list[int]) -> str:
    if not user_ids:
        raise ValueError("User IDs list cannot be empty for hash generation")

    sorted_ids = sorted(user_ids)
    hash_str = ':'.join(map(str, sorted_ids))
    return hashlib.md5(hash_str.encode()).hexdigest()