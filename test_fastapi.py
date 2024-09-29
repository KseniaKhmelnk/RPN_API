from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_create_stack():
    response = client.post("/rpn/create_stack/test_stack")
    assert response.json() == {"message": "Stack test_stack created.",
        "all_stacks": ["test_stack"]}

def test_clear_stack():
    client.post("/rpn/create_stack/test_stack")
    client.post("/rpn/push/test_stack?item=15")
    response = client.delete("/rpn/clear/test_stack")
    assert response.json() == {"message": "Stack 'test_stack' cleared.", "stack": []}

def test_push_item():
    client.delete("/rpn/clear/test_stack")
    client.post("/rpn/create_stack/test_stack")
    response = client.post("/rpn/push/test_stack?item=5")
    assert response.json() == {"message": "Item added to test_stack", "stack": [5]}
    
def test_get_stack():
    client.delete("/rpn/clear/test_stack")
    client.post("/rpn/create_stack/test_stack")
    client.post("/rpn/push/test_stack?item=10")
    response = client.get("/rpn/stack/test_stack")
    assert response.json() == {"stack": [10]}

def test_operate_stack_division():
    client.delete("/rpn/clear/test_stack")
    client.post("/rpn/create_stack/test_stack")
    client.post("/rpn/push/test_stack?item=8")
    client.post("/rpn/push/test_stack?item=4")
    response = client.post("/rpn/operate/test_stack?operation=%2F") #/ division
    assert response.json() == {"stack": [2]}

def test_operate_stack_minus():
    client.delete("/rpn/clear/test_stack")
    client.post("/rpn/create_stack/test_stack")
    client.post("/rpn/push/test_stack?item=8")
    client.post("/rpn/push/test_stack?item=4")
    response = client.post("/rpn/operate/test_stack?operation=-") #- 
    assert response.json() == {"stack": [4]}

def test_operate_stack_multiplication():
    client.delete("/rpn/clear/test_stack")
    client.post("/rpn/create_stack/test_stack")
    client.post("/rpn/push/test_stack?item=8")
    client.post("/rpn/push/test_stack?item=4")
    response = client.post("/rpn/operate/test_stack?operation=%2A") #*
    assert response.json() == {"stack": [32]}

def test_operate_stack_plus():
    client.delete("/rpn/clear/test_stack")
    client.post("/rpn/create_stack/test_stack")
    client.post("/rpn/push/test_stack?item=8")
    client.post("/rpn/push/test_stack?item=4")
    response = client.post("/rpn/operate/test_stack?operation=%2B") #+
    assert response.json() == {"stack": [12]}

def test_stack_not_found():
    response = client.get("/rpn/stack/stack_null")
    assert response.json() == {"detail": "Stack not found"}

def test_invalid_operation():
    client.delete("/rpn/clear/test_stack")
    client.post("/rpn/create_stack/test_stack")
    client.post("/rpn/push/test_stack?item=100")
    response = client.post("/rpn/operate/test_stack?operation=%2B")
    assert response.json() == {"detail": "Not enough items in the stack"}

def test_divide_by_zero():
    client.delete("/rpn/clear/test_stack")
    client.post("/rpn/create_stack/test_stack")
    client.post("/rpn/push/test_stack?item=100")
    client.post("/rpn/push/test_stack?item=0") 
    response = client.post("/rpn/operate/test_stack?operation=%2F") #/ => division
    assert response.json() == {"detail": "Cannot divide by zero"}
