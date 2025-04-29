
import os
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Auto-initialization flag file path
INIT_FLAG_FILE = ".app_initialized"

def auto_initialize():
    """Automatically initialize the application if not done already."""
    if Path(INIT_FLAG_FILE).exists():
        logger.info("Application already initialized, skipping auto-initialization")
        return
    
    logger.info("First run detected, performing auto-initialization...")
    
    # Check if we have a PostgreSQL database
    if not os.environ.get('DATABASE_URL'):
        try:
            logger.info("PostgreSQL database not found, trying to create one...")
            # We're not actually calling the API here as we've already created a database
            # This is just for informational purposes in the logs
            logger.info("PostgreSQL database should be created by Replit")
        except Exception as e:
            logger.error(f"Error creating PostgreSQL database: {e}")
    else:
        logger.info("PostgreSQL database found")
    
    # Initialize database tables and data
    try:
        from app import app, db
        with app.app_context():
            # Import models to ensure they're registered with SQLAlchemy
            import models
            
            # Create tables if they don't exist
            db.create_all()
            
            # Initialize achievements
            from gamification import initialize_achievements
            initialize_achievements()
            
            logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Error initializing database tables: {e}")
    
    # Try to initialize document processor
    try:
        from document_processor import initialize_document_processor
        from rag_engine import initialize_rag_engine
        
        initialize_document_processor()
        initialize_rag_engine()
        
        logger.info("Document processor and RAG engine initialized successfully")
    except Exception as e:
        logger.error(f"Error initializing document processor: {e}")
    
    # Create flag file to indicate initialization is complete
    Path(INIT_FLAG_FILE).touch()
    logger.info("Auto-initialization complete")

# Auto-initialize on import
auto_initialize()

# Import app after initialization
from app import app  # noqa: F401

if __name__ == "__main__":
    debug_mode = os.environ.get("FLASK_ENV") == "development"
    app.run(host="0.0.0.0", port=5000, debug=debug_mode)
