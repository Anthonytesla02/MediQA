import os

# Hardcoded Mistral API key
MISTRAL_API_KEY = "j4h3leTe769ILXBLzwsMkrKEzWqZjOTj"

# Document configuration
DOCUMENT_PATH = "attached_assets/pharmacy_guide.docx"

# RAG configuration
VECTOR_DB_PATH = "vector_db"
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

# Gamification settings
DAILY_STREAK_POINTS = 10
CASE_COMPLETION_POINTS = {
    "easy": 10,
    "medium": 20,
    "hard": 30
}
CHALLENGE_COMPLETION_POINTS = 15
CORRECT_DIAGNOSIS_BONUS = 25
FLASHCARD_REVIEW_POINTS = 5

# Spaced repetition settings
MIN_INTERVAL = 1
MAX_INTERVAL = 365
EASY_BONUS = 1.3
INITIAL_EASE = 2.5
