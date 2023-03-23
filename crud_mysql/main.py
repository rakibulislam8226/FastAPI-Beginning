from fastapi import FastAPI, Depends
from src.database import Base, engine, SessionLocal
from crud_mysql import models
from crud_mysql import schemas

# the database are from src.database. i am not using here mysql. just for setup i add mysql here. 

Base.metadata.create_all(engine)


def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()

app = FastAPI()


@app.get("/")
def getItems(session=Depends(get_session)):
    items = session.query(models.User).all()
    return items


@app.post("/")
async def addItem(user: schemas.User, session=Depends(get_session)):
    item = models.User(email=user.email, name=user.name, is_active=user.is_active, articles=user.articles)
    session.add(item)
    session.commit()
    session.refresh(item)
    return item


@app.get("/{id}")
async def getItem(id: int, session=Depends(get_session)):
    item = session.query(models.User).get(id)
    return item


@app.put("/")
async def updateItem(id: int, item: schemas.User, session=Depends(get_session)):
    itemObject = session.query(models.User).get(id)
    itemObject.email = item.email
    itemObject.name = item.name
    itemObject.is_active = item.is_active
    itemObject.articles = item.articles
    session.commit()
    return itemObject


@app.delete("/id")
async def deleteItem(id: int, session=Depends(get_session)):
    itemObject = session.query(models.User).get(id)
    session.delete(itemObject)
    session.commit()
    session.close()
    return 'Item was deleted.'
