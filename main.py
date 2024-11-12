import sqlite3
import atexit
import model
import database
# from loguru import logger

from jinja2 import Template
from jinja2_fragments.fastapi import Jinja2Blocks

from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, FileResponse

# from fastapi.templating import Jinja2Templates


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
    context = {"users": db.get_all_users()}
    return templates.TemplateResponse(
        "index.html", {"request": request, "context": context}
    )


@app.post("/user")
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
        context["users"] = db.get_all_users()
        context["success_message"] = "Added user successfully"
    except Exception as e:
        context["error_message"] = str(e)
        context["users"] = db.get_all_users()

    return templates.TemplateResponse(
        "index.html",
        {"request": request, "context": context},
        block_name="table",
    )


# if __name__ == "__main__":
#     main()
