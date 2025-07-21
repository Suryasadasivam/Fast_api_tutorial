from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

#url 
sql_alchmey_url='sqlite:///./todos.db'

#create a engine 
engine=create_engine(sql_alchmey_url,connect_args={'check_same_thread':False})

SessionLocal= sessionmaker(autocommit=False,autoflush=False,bind=engine)

Base=declarative_base()




