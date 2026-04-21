def check_user_profile(user) -> int:
    score = 0
    # Check for RTL characters (often used to hide links)
    if any('\u202e' in s for s in [user.first_name, user.username or ""]):
        score += 5
    # Check for scam keywords in name
    if any(k in user.first_name.lower() for k in ["crypto", "admin", "support"]):
        score += 2
    return score
