from datetime import datetime
from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from tinydb import TinyDB
from tinydb.middlewares import CachingMiddleware
from tinydb.storages import MemoryStorage
from pydantic import BaseModel
from deta import Deta
import asyncio

import convert_time as ct

deta = Deta()
async_uses = deta.AsyncBase("uses")
async_machines = deta.AsyncBase("machines")

app = FastAPI(
  title="QueueToken",
  license_info={
    "name": "Apache 2.0",
    "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
  }
)
templates = Jinja2Templates(directory="templates/")

memory_db = TinyDB(storage=CachingMiddleware(MemoryStorage))
table = memory_db.table('tokens')


@app.get("/", status_code=200)
def form_get(request: Request):
    return templates.TemplateResponse('form.html', context={'request': request, 'result': "Digite seu token"})


@app.post("/", status_code=201)
async def form_post(request: Request, token: str = Form(...)):
    # trim the token
    token = token.strip()
    ret = await async_machines.get(token)
    print(ret)
    if ret:
        table.insert({'token': token})
        now = datetime.now()
        await async_uses.put({
            "timestamp": now.strftime("%d/%m/%Y %H:%M:%S"),
            "user": ret["user"]
        })
        return templates.TemplateResponse('wait.html', context={'request': request, 'result': '{}'.format(token)})
    return templates.TemplateResponse('form.html', context={'request': request, 'result': "Digite seu token"})


@app.get("/tokens", status_code=200)
def tokens_get(request: Request):
    resp = table.all()
    table.truncate()
    return resp


@app.get("/machine", status_code=200)
async def machine_get(request: Request, token: str):
    ret = await async_machines.get(token)
    return '{}'.format(ret["machine"])


@app.get("/timesheet", status_code=200)
async def timesheet_get(request: Request, key: str):
    res = await async_uses.fetch()
    result = res.items

    for r in result:
        r["timestamp"] = ct.convert_timestamp(r["timestamp"])

    result.sort(reverse=True, key=ct.sort_function)

    return templates.TemplateResponse('timesheet.html', context={'request': request, 'result': result})


@app.get("/favicon.ico", status_code=200)
async def favicon(request: Request):
    return ""


@app.get("/*", status_code=404)
def catch_all(request: Request):
    return ""