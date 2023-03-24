import fastapi
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer


app = fastapi.FastAPI()


@app.post('/login')
def login():
    """Processes user's authentication and returns a token
    on successful authentication.

    request body:

    - username: Unique identifier for a user e.g email, 
                phone number, name

    - password:
    """
    return "ThisTokenIsFake"


outh2_schema = OAuth2PasswordBearer(tokenUrl='token')

@app.post("/token", description="Checking the user is authorize or not if authorize then the token.")
async def token(form_data: OAuth2PasswordRequestForm = fastapi.Depends()):
    return {"access_token": form_data.username + "token"}


@app.get("/")
async def index(token: str = fastapi.Depends(outh2_schema)):
    return {"token": token}



