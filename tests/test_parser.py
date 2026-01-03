import pytest
from codelens.core.parser import CodeParser

DUMMY_CODE = """
def hello():
    print("world")

class Calculator:
    def add(self, a, b):
        return a + b

class Database:
    def connect(self):
        pass
    def query(self):
        pass
"""

def test_parser_identifies_all_components():
    parser = CodeParser()
    chunks = parser.parse_text(DUMMY_CODE)
    
    # Check total count (1 function + 1 class meta + 1 method + 1 class meta + 2 methods = 6)
    assert len(chunks) == 6
    
    assert any("def connect(self):" in chunk for chunk in chunks)
    assert any("Class: Calculator" in chunk for chunk in chunks)
    assert any("def hello():" in chunk for chunk in chunks)

def test_parser_handles_non_python_or_malformed_code():
    parser = CodeParser()
    malformed_code = "This is not valid python code { [ ]"
    
    chunks = parser.parse_text(malformed_code)
    
    assert len(chunks) == 1
    assert chunks[0] == malformed_code

def test_parser_handles_empty_string():
    parser = CodeParser()
    chunks = parser.parse_text("")
    
    assert chunks == [""]