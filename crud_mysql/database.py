# here i am not useing mysql but just for setup i add mysql here.


from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


# Create sqlite engine instance
engine = create_engine("mysql://root:root@localhost/fastapi_crud")
# Create declaritive base meta instance
Base = declarative_base()
# Create session local class for session maker
SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)

# # This will create our database if it doesn't already exists.
# Base.metadata.create_all(engine)


# def get_session():
#     session = SessionLocal()
#     try:
#         yield session
#     finally:
#         session.close()
