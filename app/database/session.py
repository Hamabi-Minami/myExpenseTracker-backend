from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

engine = create_engine(settings.db_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)



def init_db():
    from app.models import user, comment, article, role
    from app.database.base import Base
    Base.metadata.create_all(bind=engine)