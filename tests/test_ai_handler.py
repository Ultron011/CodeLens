import pytest
from unittest.mock import MagicMock, patch
from codelens.core.ai_handler import AIHandler

@patch("codelens.core.ai_handler.ChatOpenAI")
def test_ai_handler_formats_context_correctly(mock_llm_class):
    mock_llm_instance = MagicMock()
    mock_llm_class.return_value = mock_llm_instance
    
    mock_response = MagicMock()
    mock_response.content = "The database is initialized in db.py"
    mock_llm_instance.invoke.return_value = mock_response
    
    handler = AIHandler()
    context = ["def init_db(): pass", "class User: pass"]
    question = "Where is the DB?"
    
    answer = handler.ask_question(question, context)
    
    assert answer == "The database is initialized in db.py"
    
    args, _ = mock_llm_instance.invoke.call_args
    messages = args[0]
    
    human_msg_content = messages[1].content
    assert "def init_db(): pass" in human_msg_content
    assert "Where is the DB?" in human_msg_content