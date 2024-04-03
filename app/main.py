from fastapi import FastAPI
from .routes.user import userRoute
from .routes.auth import authRouter
from .core.config import dbSettings

app = FastAPI()
@app.get("/")
def read_root():

    return {"Hello": "World"}
#include routers
app.include_router(authRouter)
app.include_router(userRoute)

