ACCESS_ERROR_MESSAGE = "You dont have access to this session"
ALREAD_LOGGED_IN_USER_ERROR = "You are already in this session"
DEFENSE_LABELS = ["10 + 1/2 lvl", "Ability", "Armor", "Class"]
INVALID_INVITATION_KEY_ERROR_MESSAGE = "Invalid invitation key"
NON_EXISTENT_CHARACTER_ERRROR = (
    'Character doesnt exist, not your character, '
    'or you are in a wrong session'
)
POST_REQUEST_ERROR_MESSAGE = "Invalid post"
UNIQUE_KEY_ERROR = "Could not generate a unique key after multiple attempts."
USER_VALUE = {
    'abilities': {
        'strength': 12,
        'constitution': 14,
        'dexterity': 13,
        'intelligence': 15,
        'wisdom': 6,
        'charisma': 17,
    }
}
SKILL_DEPENDENCIES = {
    "acrobatic": "Dexterity",
    "arcana": "Intelligence",
    "athletic": "Strength",
    "bluff": "Charisma",
    "diplomacy": "Charisma",
    "dungeoning": "Wisdom",
    "endurange": "Strength",
    "heal": "Wisdom",
    "history": "Intelligence",
    "insight": "Wisdom",
    "intimidate": "Charisma",
    "nature": "Wisdom",
    "perception": "Wisdom",
    "religion": "Intelligence",
    "stealth": "Dexterity",
    "streetwise": "Charisma",
    "thievery": "Dexterity"
}