from codelens.core.memory_manager import ChatMemory
import os

def test_memory_saves_and_loads(tmp_path):
    # Use a temp file for testing
    test_file = tmp_path / "history.json"
    mem = ChatMemory(file_path=str(test_file))
    
    # Save a fake interaction
    mem.save("What is this code?", "It is a scanner.")
    
    # Load it back
    history = mem.load()
    assert len(history) == 2
    assert history[0]['role'] == 'user'
    assert history[1]['content'] == "It is a scanner."