from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

#SQLALCHEMY_DATABASE_URL = 'sqlite:///./todosapp.db'
#POSTGRESQL_DATABASE_URL = 'postgresql+psycopg2://postgres:test1234!@localhost/TodoApplicationDatabase'
MYSQL_DATABASE_URL = 'mysql+pymysql://root:elDelle6432..@127.0.0.1:3306/TodoApplicationDatabase'

#engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={'check_same_thread': False})
engine = create_engine(MYSQL_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()