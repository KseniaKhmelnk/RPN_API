from collections import deque
from fastapi import FastAPI, HTTPException
from typing import Dict

app = FastAPI()

class RPN:
    """Class of Reverse Polish Notation operations"""
    def __init__(self):
        self.items = deque()

    def push(self, value: int):
        self.items.append(value)
    
    def operate(self, operation: str):
        if len(self.items) < 2:
            raise ValueError("Not enough items in the stack")
        b, a = self.items.pop(), self.items.pop()
        try:
            expr = f"{a} {operation} {b}"
            result = eval(expr)
            self.items.append(result)
        except ZeroDivisionError:
            raise ValueError("Cannot divide by zero")
        except Exception:
            raise ValueError("Invalid operation")

    def clear(self):
        self.items.clear()
    
    def get_stack(self):
        return list(self.items)

class Parser:
    """Class to hande the parsing of the input commands"""
    def __init__(self, rpn: RPN):
        self.rpn = rpn

    def parse_and_execute(self, command: str):
        tokens = command.split()
        if not tokens:
            raise ValueError("Empty command")
        
        for token in tokens:
            if token.isdigit():
                self.rpn.push(int(token))
            else:
                self.rpn.operate(token)

stacks: Dict[str, RPN] = {}

@app.post("/rpn/create_stack/{stack_name}", tags=["rpn"])
def create_stack(stack_name: str):
    if stack_name in stacks:
        raise HTTPException(status_code=400, detail="Stack already exists")
    stacks[stack_name] = RPN()
    return {"message": f"Stack {stack_name} created", "all_stacks": list(stacks.keys())}

@app.post("/rpn/push/{stack_name}", tags=["rpn"])
def push(stack_name: str, item: float):
    if stack_name not in stacks:
        raise HTTPException(status_code=404, detail="Stack not found")
    stacks[stack_name].push(item)
    return {"message": f"Item added to {stack_name}", "stack": stacks[stack_name].get_stack()}

@app.get("/rpn/stack/{stack_name}", tags=["rpn"])
def get_stack(stack_name: str):
    if stack_name not in stacks:
        raise HTTPException(status_code=404, detail="Stack not found")
    return {"stack": stacks[stack_name].get_stack()}

@app.delete("/rpn/clear/{stack_name}", tags=["rpn"])
def clear_stack(stack_name: str):
    if stack_name not in stacks:
        raise HTTPException(status_code=404, detail="Stack not found")
    stacks[stack_name].clear()
    return {"message": f"Stack '{stack_name}' cleared.", "stack": stacks[stack_name].get_stack()}

@app.post("/rpn/operate/{stack_name}", tags=["rpn"])
def operate(stack_name: str, operation: str):
    if stack_name not in stacks:
        raise HTTPException(status_code=404, detail="Stack not found")
    stack = stacks[stack_name]
    try:
        stack.operate(operation)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return {"stack": stack.get_stack()}

#Possibility of writing PRN in one line
rpn = RPN()
parser = Parser(rpn)

@app.post("/rpn/execute_one_line", tags=["rpn_command"])
def execute_rpn_command(command: str):
    try:
        parser.parse_and_execute(command)
        return {"stack": rpn.get_stack()}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))