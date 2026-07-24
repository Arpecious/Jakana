# Jakana Ecosystem: API, SDK, and Systems

## 1. REST API Development

### FastAPI

**Jakana**
```jakana
use fastapi as fa
use pydantic as pyd

app = fa.FastAPI()

class Item(pyd.BaseModel) {
    name: str
    price: float
}

@app.get("/items/{item_id}")
fn read_item(item_id: int) {
    return {"item_id": item_id}
}

@app.post("/items/")
fn create_item(item: Item) {
    return item
}
```

**Python**
```python
import fastapi as fa
import pydantic as pyd

app = fa.FastAPI()

class Item(pyd.BaseModel):
    name: str
    price: float

@app.get("/items/{item_id}")
def read_item(item_id: int):
    return {"item_id": item_id}

@app.post("/items/")
def create_item(item: Item):
    return item
```

### Flask

**Jakana**
```jakana
use flask as fl

app = fl.Flask(__name__)

@app.route("/")
fn hello() {
    return "Hello, World!"
}
```

**Python**
```python
import flask as fl

app = fl.Flask(__name__)

@app.route("/")
def hello():
    return "Hello, World!"
```

## 2. HTTP Clients

### Requests

**Jakana**
```jakana
use requests as req

response = req.get("https://api.example.com/data")
response.json() |> echo
```

**Python**
```python
import requests as req

response = req.get("https://api.example.com/data")
print(response.json())
```

### Httpx (Async)

**Jakana**
```jakana
use httpx

async fn fetch() {
    async with httpx.AsyncClient() as client {
        r = await client.get("https://example.com")
        r.status_code |> echo
    }
}
```

**Python**
```python
import httpx

async def fetch():
    async with httpx.AsyncClient() as client:
        r = await client.get("https://example.com")
        print(r.status_code)
```

## 3. Database Systems

### SQLAlchemy

**Jakana**
```jakana
use sqlalchemy as sa
use sqlalchemy.orm as orm

engine = sa.create_engine("sqlite:///memory:")
Base = orm.declarative_base()

class User(Base) {
    __tablename__ = "users"
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String)
}
```

**Python**
```python
import sqlalchemy as sa
import sqlalchemy.orm as orm

engine = sa.create_engine("sqlite:///memory:")
Base = orm.declarative_base()

class User(Base):
    __tablename__ = "users"
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String)
```

### MongoDB

**Jakana**
```jakana
use pymongo as pm

client = pm.MongoClient("mongodb://localhost:27017/")
db = client["mydb"]
collection = db["users"]
collection.insert_one({"name": "Alice"})
```

**Python**
```python
import pymongo as pm

client = pm.MongoClient("mongodb://localhost:27017/")
db = client["mydb"]
collection = db["users"]
collection.insert_one({"name": "Alice"})
```

## 4. Message Queues & Streaming

### Celery

**Jakana**
```jakana
use celery as cel

app = cel.Celery("tasks", broker="redis://localhost:6379/0")

@app.task
fn add(x, y) {
    return x + y
}
```

**Python**
```python
import celery as cel

app = cel.Celery("tasks", broker="redis://localhost:6379/0")

@app.task
def add(x, y):
    return x + y
```

## 5. Authentication & Security

### PyJWT

**Jakana**
```jakana
use jwt

secret = "secret"
token = jwt.encode({"user": "admin"}, secret, algorithm="HS256")
decoded = jwt.decode(token, secret, algorithms=["HS256"])
```

**Python**
```python
import jwt

secret = "secret"
token = jwt.encode({"user": "admin"}, secret, algorithm="HS256")
decoded = jwt.decode(token, secret, algorithms=["HS256"])
```

## 6. SDK Creation Patterns

### Base Client

**Jakana**
```jakana
use requests as req

class APIClient {
    fn __init__(self, api_key) {
        self.api_key = api_key
        self.base_url = "https://api.service.com/v1"
    }

    fn get_user(self, user_id) {
        headers = {"Authorization": f"Bearer {self.api_key}"}
        r = req.get(f"{self.base_url}/users/{user_id}", headers=headers)
        return r.json()
    }
}
```

**Python**
```python
import requests as req

class APIClient:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.service.com/v1"

    def get_user(self, user_id):
        headers = {"Authorization": f"Bearer {self.api_key}"}
        r = req.get(f"{self.base_url}/users/{user_id}", headers=headers)
        return r.json()
```

## 7. ADK (Agent Development Kit) Patterns

### Simple Tool Agent

**Jakana**
```jakana
class Agent {
    fn __init__(self, tools) {
        self.tools = tools
        self.memory = []
    }

    fn act(self, instruction) {
        # Decide action based on tools
        action = "search"
        if action in self.tools {
            result = self.tools[action](instruction)
            self.memory.append(result)
            return result
        } else {
            return "No tool found."
        }
    }
}
```

**Python**
```python
class Agent:
    def __init__(self, tools):
        self.tools = tools
        self.memory = []

    def act(self, instruction):
        # Decide action based on tools
        action = "search"
        if action in self.tools:
            result = self.tools[action](instruction)
            self.memory.append(result)
            return result
        else:
            return "No tool found."
```

## 8. Cloud & Infrastructure

### Boto3 (AWS S3)

**Jakana**
```jakana
use boto3

s3 = boto3.client("s3")
s3.upload_file("local.txt", "my-bucket", "remote.txt")
```

**Python**
```python
import boto3

s3 = boto3.client("s3")
s3.upload_file("local.txt", "my-bucket", "remote.txt")
```

## 9. DevOps & CI/CD

### Subprocess

**Jakana**
```jakana
use subprocess as sp

result = sp.run(["git", "status"], capture_output=True, text=True)
result.stdout |> echo
```

**Python**
```python
import subprocess as sp

result = sp.run(["git", "status"], capture_output=True, text=True)
print(result.stdout)
```

## 10. GraphQL

### Strawberry

**Jakana**
```jakana
use strawberry

@strawberry.type
class Query {
    @strawberry.field
    fn hello(self) -> str {
        return "Hello world"
    }
}

schema = strawberry.Schema(query=Query)
```

**Python**
```python
import strawberry

@strawberry.type
class Query:
    @strawberry.field
    def hello(self) -> str:
        return "Hello world"

schema = strawberry.Schema(query=Query)
```

## 11. WebSocket & Real-Time

### WebSockets

**Jakana**
```jakana
use websockets
use asyncio

async fn handler(websocket, path) {
    data = await websocket.recv()
    await websocket.send(f"Echo: {data}")
}
```

**Python**
```python
import websockets
import asyncio

async def handler(websocket, path):
    data = await websocket.recv()
    await websocket.send(f"Echo: {data}")
```

## 12. Testing & Quality

### Pytest

**Jakana**
```jakana
use pytest

@pytest.fixture
fn sample_data() {
    return {"id": 1, "value": "test"}
}

fn test_example(sample_data) {
    assert sample_data["id"] == 1
}
```

**Python**
```python
import pytest

@pytest.fixture
def sample_data():
    return {"id": 1, "value": "test"}

def test_example(sample_data):
    assert sample_data["id"] == 1
```
