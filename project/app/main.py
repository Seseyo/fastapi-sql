import os
import sys

sys.path.append(os.path.join(os.getcwd(),'project/app'))
sys.path.append(os.path.join(os.getcwd(),'app'))

import uvicorn
from fastapi import FastAPI

from db.config import engine, Base, session
from routers import menu_router

app = FastAPI()
app.include_router(menu_router.router)


@app.on_event("startup")
def startup():
    # create db tables
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


#if __name__ == '__main__':
#    uvicorn.run("app:app", port=1111, host='127.0.0.1', reload=True)
