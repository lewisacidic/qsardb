from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from ..utils import config

Base = declarative_base()
engine = create_engine(config['alembic']['sqlalchemy.url'])
Session = sessionmaker(bind=engine)

from .models import Source, Species, Target, Compound, Activity
