from codelens.core.ai_handler import AIHandler
import argparse
import time
from codelens.core.scanner import CodeScanner
from codelens.ui.formatter import print_header, display_scan_results, display_query_results, print_answer, console
from codelens.core.parser import CodeParser
from codelens.core.vector_store import VectorMemory
from codelens.core.ai_handler import AIHandler
from codelens.core.memory_manager import ChatMemory

def handle_scan(args):
    with console.status("[bold green]Scanning project structure...") as status:
        scanner = CodeScanner(args.path)
        files = scanner.get_all_files()
        time.sleep(0.1)
        
        status.update("[bold green]Parsing and embedding code chunks...")
        parser = CodeParser()
        memory = VectorMemory()
        
        total_chunks = 0
        for file_path in files:
            if file_path.suffix == ".py":
                content = file_path.read_text(encoding="utf-8-sig", errors="ignore")
                chunks = parser.parse_text(content)
                
                if chunks:
                    metadatas = [{"file": str(file_path)} for _ in chunks]
                    chunk_ids = [f"{file_path}-{i}" for i in range(len(chunks))]
                    memory.add_chunks(contents=chunks, metadatas=metadatas, ids=chunk_ids)
                    total_chunks += len(chunks)
            
    display_scan_results(args.path, files, total_chunks)

def handle_query(args):
    memory = VectorMemory()
    results = memory.search(args.query)
    display_query_results(args.query, results)
    
def handle_ask(args):
    memory = VectorMemory()
    chat_mem = ChatMemory()
    ai = AIHandler()
    
    history = chat_mem.load()
    
    with console.status("[bold yellow]Searching codebase..."):
        results = memory.search(args.query, n_results=5)
        relevant_chunks = results.get('documents', [[]])[0]
        
    with console.status("[bold green]Analyzing with AI..."):
        answer = ai.ask_question(args.query, relevant_chunks, chat_history=history)
    
    chat_mem.save(args.query, answer)
        
    print_answer(answer)
    
def handle_reset(args):
    """Clears local storage to start fresh."""
    chat_mem = ChatMemory()
    
    if args.mode in ["chat", "all"]:
        chat_mem.clear()
        console.print("[bold green]✔ Chat history cleared.[/bold green]")
        
    if args.mode in ["db", "all"]:
        memory_db = VectorMemory()
        memory_db.clear_all() 
        console.print("[bold green]✔ Vector database cleared.[/bold green]")

def run_cli():
    parser = argparse.ArgumentParser(prog="codelens")
    subparsers = parser.add_subparsers(dest="command")

    scan_parser = subparsers.add_parser("scan")
    scan_parser.add_argument("path", type=str)
    
    query_parser = subparsers.add_parser("query")
    query_parser.add_argument("query", type=str)
    
    ask_parser = subparsers.add_parser("ask")
    ask_parser.add_argument("query", type=str, help="What do you want to know about your code?")
    
    reset_parser = subparsers.add_parser("reset", help="Clear local memory or database")
    reset_parser.add_argument(
        "mode", 
        choices=["chat", "db", "all"], 
        help="What to reset: 'chat' for history, 'db' for code index, or 'all' for both"
    )    
    args = parser.parse_args()
    print_header("v0.1.0")

    if args.command == "scan":
        handle_scan(args)
    elif args.command == "query":
        handle_query(args)
    elif args.command == "ask":
        handle_ask(args)
    elif args.command == "reset":
        handle_reset(args)
    else:
        parser.print_help()
