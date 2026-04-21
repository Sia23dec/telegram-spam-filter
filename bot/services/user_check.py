from telegram import Update

async def get_profile_spam_score(update: Update) -> int:
    user = update.effective_user
    score = 0
    # Check for profile photo
    photos = await user.get_profile_photos()
    if photos.total_count == 0:
        score += 2
    
    # Check if they have a username
    if not user.username:
        score += 1
        
    return score
