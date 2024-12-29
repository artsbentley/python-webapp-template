import sqlite3
import atexit
import model
import database
import auth
from jinja2_fragments.fastapi import Jinja2Blocks
from fastapi import FastAPI, Request, Form, HTTPException, Response
from fastapi.responses import HTMLResponse, FileResponse, RedirectResponse


# NOTE:
# - idea; each page receives it's own context model in pydantic which get's
# passed to jinja templates

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
        name="index.html", context={"request": request, "context": context}
    )


@app.get("/login")
async def login(request: Request):
    return templates.TemplateResponse(
        name="login.html",
        context={
            "request": request,
        },
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
        raise Exception
    except Exception as e:
        raise HTTPException(status_code=500, detail=e)
        # context["message"] = str(e)
        # context["success"] = False
        # context["users"] = db.get_all_users()

    # Return both message and table blocks
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "context": context},
        block_names=["message", "table"],
    )


# TODO: setup right login page and such
@app.exception_handler(auth.RequiresLoginException)
async def exception_handler(
    request: Request, exc: auth.RequiresLoginException
) -> Response:
    return RedirectResponse("/login")


# TODO: change to returning a template
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    html_content = f"""
    <html>
        <head><title>error {exc.status_code}</title></head>
        <body>
            <h1>error {exc.status_code}</h1>
            <p>{exc.detail}</p>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=exc.status_code)


# @app.exception_handler(Exception)
# async def global_exception_handler(request: Request, exc: Exception):
#     html_content = f"""
#     <html>
#         <head><title>Server Error</title></head>
#         <body>
#             <h1>5000000 Internal Server Error</h1>
#             <p>{str(exc)}</p>
#         </body>
#     </html>
#     """
#     return HTMLResponse(content=html_content, status_code=500)
