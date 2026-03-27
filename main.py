from typing import Annotated

from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from typing import Annotated
from pydantic import Field, BaseModel



class Product(BaseModel):
    name: Annotated[str, Field(min_length=3, max_length=30)]
    price: Annotated[float, Field(gt=0)]
    location: Annotated[str, Field(min_length=3)]

product= Product.model_validate(
    {"name":"minigun", "price":17500, "location":"Los Antos"}
)
print(product)



app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates= Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    """Renders the home page."""
    text={"title":"Home",
          "content":"Welcome to my home page.",
          }

    context = {"request": request,"text": text, "sequence": ["a", "b", "c"]}
    return templates.TemplateResponse(
        request=request,
        name= "home.html",
        context= context
    )
products_list = [
    {"name":"Pistola", "price": 100, "location": "Mexico"},
    {"name":"Carabina", "price": 200, "location": "USA"},
    {"name":"Ipad", "price": 150, "location": "Spain"}
]
@app.get("/products", response_class=HTMLResponse)
def products(request: Request):
    return templates.TemplateResponse(
        request=request,
        name= "products.html",
        context={"request": request, "product_list": products_list}
    )


@app.get("/product_form", response_class=HTMLResponse)
def add_product(request: Request,
                name:str | None = None,
                price:float | None = None,
                location:str | None = None
):
    if name and price and location:
        product={"name":name, "price":price, "location":location}
        products_list.append(product)
    return templates.TemplateResponse(
        request=request,
        name= "product_form.html",
        context={"request": request})



@app.post("/insert_product")
def insert_product(product: Annotated[Product, Form()]):

    products_list.append(product.model_dump())
    return "Product added successfully"




@app.post("/insert_product_json")
def insert_product_json(product: Product):
    print(product)
    return {"message": "Product received correctly via JSON", "product": product.model_dump()}