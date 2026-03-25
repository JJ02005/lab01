from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
app = FastAPI()
templates= Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    """Renders the home page."""
    text={"title":"Home",
          "content":"Welcome to my home page.",
          }
    context = {
        "text": text, "sequence": ["a", "b", "c"]}
    return templates.TemplateResponse(
        request=request,
        name= "home.html",
        context= context
    )
