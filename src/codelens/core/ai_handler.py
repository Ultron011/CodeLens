import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.messages import SystemMessage, HumanMessage, AIMessage

load_dotenv('.env')

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

class AIHandler:
    def __init__(self, model_provider="openai", model_name="gpt-5-mini"):
        self.llm = ChatOpenAI(model=model_name, api_key=OPENAI_API_KEY)
        
    def ask_question(self, question: str, code_context: list[str], chat_history: list=None):        
        if not code_context:
            return "I couldn't find any relevant code to answer that question. Please try scanning the project first."  
        chat_history = chat_history or []

        system_prompt = SystemMessage(content="""
                    You are a Senior Software Architect. Use the provided code snippets to answer the user's question.
                    
                    Formatting Rules:
                    1. Use Markdown for your response.
                    2. Use `backticks` for variable names, function names, and class names.
                    3. Use **bold** for emphasis on key concepts.
                    4. Use code blocks (```python) for any code examples.
                    5. Use bullet points for lists.
                    
                    Content Rules:
                    1. If the answer is not in the code, say "I don't have enough context to answer that."
                    2. Be concise and technical.
                    3. Reference specific function or class names found in the context.
                    4. Do not make up code that doesn't exist in the context.
                """)
        
        messages = [system_prompt]
        
        context_text = "\n---\n".join(code_context)
        user_prompt = HumanMessage(content=f"Contextual Code:\n{context_text}\n\nQuestion: {question}")
        
        
        for msg in chat_history:
            if msg["role"] == "user":
                messages.append(HumanMessage(content=msg["content"]))
            else:
                messages.append(AIMessage(content=msg["content"]))
                
        messages.append(user_prompt)

        response = self.llm.invoke(messages)     
        return response.content