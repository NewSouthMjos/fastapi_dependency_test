import uvicorn
from fastapi import FastAPI, Depends


app = FastAPI()


def get_something_sync():
    yield True


async def get_something_async():
    yield True


@app.get('/1')
def router_func(dependency=Depends(get_something_sync)):
    raise ValueError
    return


@app.get('/2')
def router_func(dependency=Depends(get_something_async)):
    raise ValueError
    return


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=5600, workers=1)
