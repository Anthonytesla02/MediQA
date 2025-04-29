import os
import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from werkzeug.middleware.proxy_fix import ProxyFix

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class Base(DeclarativeBase):
    pass

# Initialize SQLAlchemy
db = SQLAlchemy(model_class=Base)

# Create the app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev_secret_key")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Configure the database
# Handle potential "postgres://" to "postgresql://" conversion for Heroku-style DATABASE_URLs
database_url = os.environ.get("DATABASE_URL", "sqlite:///mediqa.db")
if database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)

app.config["SQLALCHEMY_DATABASE_URI"] = database_url
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
    "pool_size": 10,
    "max_overflow": 20,
}
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize the database
db.init_app(app)

# Import modules
with app.app_context():
    from document_processor import initialize_document_processor
    from rag_engine import initialize_rag_engine
    import models  # noqa: F401
    import routes  # noqa: F401
    
    # Create database tables
    db.create_all()
    
    # Initialize the document processor and RAG engine
    try:
        doc_init_success = initialize_document_processor()
        if doc_init_success:
            rag_init_success = initialize_rag_engine()
            if rag_init_success:
                logger.info("Document processor and RAG engine initialized successfully")
            else:
                logger.warning("RAG engine initialization failed, some features may be limited")
        else:
            logger.warning("Document processor initialization failed, proceeding with limited functionality")
    except Exception as e:
        logger.error(f"Error during initialization: {e}")
        logger.info("Application will continue with limited functionality")
