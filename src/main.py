from fastapi import FastAPI, Response
import pathlib

app = FastAPI()

@app.get('/')
async def get():
    return {'message': 'Hello world'}

@app.get('/data')
def get_data():
    root = pathlib.Path(__file__).parent.parent

    with open(f'{root}\\data\\data.json', 'r', encoding='utf-8') as f:
        data = f.read()

    return Response(content=data, media_type="application/json")
