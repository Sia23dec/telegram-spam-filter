import httpx

async def check_global_ban(user_id: int) -> bool:
    """Checks if user is a known spammer in the Combot Anti-Spam database."""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"https://api.cas.chat/check?user_id={user_id}")
            return response.json().get("ok", False)
        except:
            return False