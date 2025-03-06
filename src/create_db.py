from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

URL_MAIN = 'postgresql+psycopg2://admin:admin@localhost/diploma'

engine = create_engine(URL_MAIN, echo=False)
Session = sessionmaker(engine)
session = Session()

Base = declarative_base()
