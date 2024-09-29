import pytest
from main import RPN

def test_rpn_push():
    rpn = RPN()
    rpn.push(10)
    assert rpn.get_stack() == [10]

def test_rpn_addition():
    rpn = RPN()
    rpn.push(2)
    rpn.push(3)
    rpn.operate("+")
    assert rpn.get_stack() == [5]

def test_rpn_subtraction():
    rpn = RPN()
    rpn.push(5)
    rpn.push(2)
    rpn.operate("-")
    assert rpn.get_stack() == [3]

def test_rpn_multiplication():
    rpn = RPN()
    rpn.push(3)
    rpn.push(4)
    rpn.operate("*")
    assert rpn.get_stack() == [12]

def test_rpn_division():
    rpn = RPN()
    rpn.push(10)
    rpn.push(2)
    rpn.operate("/")
    assert rpn.get_stack() == [5]

def test_rpn_divide_by_zero():
    rpn = RPN()
    rpn.push(10)
    rpn.push(0)
    with pytest.raises(ValueError, match="Cannot divide by zero"):
        rpn.operate("/")

def test_rpn_clear():
    rpn = RPN()
    rpn.push(10)
    rpn.clear()
    assert rpn.get_stack() == []
