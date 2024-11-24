import sqlite3
import atexit
import model
import database
from jinja2_fragments.fastapi import Jinja2Blocks
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, FileResponse

app = FastAPI()
templates = Jinja2Blocks(directory="templates")
conn = sqlite3.connect("app.db")
atexit.register(lambda: conn.close())
db = database.Database(conn)


@app.get("/favicon.ico")
async def get_favicon():
    return FileResponse("static/favicon.ico")


@app.get("/")
async def root(request: Request):
    context = {}
    context["users"] = db.get_all_users()
    return templates.TemplateResponse(
        "index.html", {"request": request, "context": context}
    )


@app.post("/create_user")
async def create_user(
    request: Request,
    name: str = Form(...),
    age: int = Form(...),
    email: str = Form(...),
):
    context = {}
    try:
        user = model.User(name=name, age=age, email=email)
        db.insert_user(user)
        context["success"] = True
        context["message"] = "Added user successfully"
        context["users"] = db.get_all_users()
    except Exception as e:
        context["message"] = str(e)
        context["success"] = False
        context["users"] = db.get_all_users()

    # Return both message and table blocks
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "context": context},
        block_names=["message", "table"],
    )
