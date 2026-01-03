import pytest
from codelens.core.vector_store import VectorMemory

def test_store_and_retrieve_code(tmp_path):
    # Use a temporary directory for the database instead of ":memory"
    memory = VectorMemory(db_path=str(tmp_path))
    
    code_chunk = "def calculate_tax(amount): return amount * 0.1"
    memory.add_chunk(
        content=code_chunk, 
        metadata={"file": "finance.py"},
        chunk_id="chunk_1"
    )
    
    results = memory.search("How do i compute taxes?")
    
    assert len(results['documents'][0]) > 0
    assert "calculate_tax" in results['documents'][0][0]
