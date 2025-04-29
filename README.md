# MediQA - AI-Powered Medical Diagnostic Training App

MediQA is an AI-powered medical diagnostic mobile app with RAG capabilities using the Ghana National Drugs Programme's "Standard Treatment Guidelines" document as its knowledge base. The app includes gamification features and interactive learning tools.

## Features

- **AI-powered Chat**: Get medical information from the embedded knowledge base
- **Case Simulations**: Practice diagnosing virtual patient cases
- **Flashcards**: Study medical concepts with spaced repetition
- **Daily Challenges**: Test your diagnostic skills with daily challenges
- **Performance Dashboard**: Track your progress and see your stats
- **Leaderboard**: Compare your progress with others

## Technical Components

- **Flask Backend**: Serves the web application and API endpoints
- **Retrieval Augmented Generation (RAG)**: Enhances AI responses with domain-specific content
- **Gamification System**: Points, streaks, achievements, and leaderboard
- **Spaced Repetition**: Advanced algorithm for flashcard learning
- **Modern Mobile UI**: Responsive design with animations, cards, and more

## Migrating to a New Replit Account

The app is designed to be easily migrated to another Replit account with minimal setup:

1. **Fork the Repl** to your new Replit account
2. **Run the application** - the automatic initialization will:
   - Create a PostgreSQL database if needed
   - Set up all required database tables
   - Initialize the document processor and RAG engine
   - Configure any necessary environment

The Mistral API key is hardcoded in `config.py`, so no API key configuration is required.

## Auto-Setup Features

This app includes several auto-setup features:

1. **Automatic Database Initialization**: The database tables are created automatically on first run
2. **Hardcoded API Key**: The Mistral API key is hardcoded in `config.py`
3. **Document Processing**: The medical document is processed automatically on first run
4. **PostgreSQL Support**: The app works with the Replit PostgreSQL database service

## Manual Setup (If Needed)

If you prefer to manually set things up:

1. Run the setup script for a complete initialization:
   ```
   python setup.py
   ```
   This will install all packages, initialize the database, and set up the document processor.

2. Or install packages manually:
   ```
   pip install -r package_requirements.txt
   ```

## File Structure

- `main.py` - Application entry point with auto-initialization logic
- `app.py` - Flask application setup
- `document_processor.py` - Processes the knowledge base document
- `rag_engine.py` - Handles retrieval augmented generation
- `ai_service.py` - Interface to the Mistral AI API with hardcoded key
- `models.py` - Database models
- `routes.py` - API and web routes
- `gamification.py` - Gamification system
- `setup.py` - Complete setup script for manual initialization
- `templates/` - HTML templates
- `static/` - Static files (CSS, JS, images)
- `attached_assets/` - Knowledge base document

## Customization

You can customize the app by:

1. Replacing the document in `attached_assets/` with your own
2. Adjusting the points and reward system in `config.py`
3. Modifying the UI theme in `static/css/style.css`

## Troubleshooting

If you encounter any issues after migration:

1. **Database Issues**: 
   - Try running `python setup.py` to reset the database and create fresh tables
   - Ensure the Replit PostgreSQL service is enabled in your account

2. **Document Processing Issues**:
   - Check that the document file exists in `attached_assets/`
   - Try restarting the application

3. **API Key Issues**:
   - The Mistral API key is hardcoded in `config.py`
   - If you need to update it, edit the `MISTRAL_API_KEY` variable in that file

4. **Application Not Starting**:
   - Check the logs for specific error messages
   - Ensure all packages are installed correctly
   - Try running `pip install -r package_requirements.txt`