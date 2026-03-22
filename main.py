from fastapi import FastAPI

app = FastAPI()

@app.get("/home")
def homepage():
    return "This is the homepage"


@app.get("/{username}")
def username_webpage(username: str):
    return f"This is the webpage of user {username}"


@app.get("/{username}/orders/{order_id}")
def orders_webpage(
        username: str,
        order_id: int,
        sort: bool = False
):
    return f"Order {order_id} for user {username}, sorted {sort}"


@app.get("/{username}/orders/{order_id}")
def repository_webpage(
        username: str,
        order_id: int
):
    return f"Order {order_id} for user {username}"

