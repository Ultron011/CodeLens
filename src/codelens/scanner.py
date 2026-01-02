import os
import argparse
import time
from collections import Counter
from pathlib import Path

from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table
from rich.panel import Panel

console = Console()

class CodeScanner:
    def __init__(self, root_dir: str, ignore_list=None):
        self.root_dir = Path(root_dir)
        self.ignore_list = ignore_list or {'.git', '__pycache__', "node_modules", '.venv', '.pytest_cache'}
        
    def get_all_files(self):
        found_files = []
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True
        ) as progress:
            progress.add_task(description="Scanning project structure...", total=None)
            
            for file_path in self.root_dir.rglob("*"):
                if any(part in self.ignore_list for part in file_path.parts):
                    continue
                
                if file_path.is_file():
                    found_files.append(file_path)
                    time.sleep(0.01)
            
            return found_files

def handle_scan(args):
    scanner = CodeScanner(args.path)
    files = scanner.get_all_files()

    table = Table(title=f"Scan Summary: {args.path}", show_header=True, header_style="bold magenta")
    table.add_column("Extension", style="dim")
    table.add_column("Count", justify="right")

    from collections import Counter
    extensions = Counter(f.suffix if f.suffix else "No Extension" for f in files)
    for ext, count in extensions.items():
        table.add_row(ext, str(count))

    console.print(table)
    console.print(f"\n[bold green]✔ Scan Complete![/bold green] Found {len(files)} files.")

def run_cli():
    parser = argparse.ArgumentParser(prog="codelens", description="CodeLens: AI-Powered Codebase Intelligence")
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    scan_parser = subparsers.add_parser("scan", help="Scan a directory and show a summary")
    scan_parser.add_argument("path", type=str, help="The folder path to scan")
    
    args = parser.parse_args()

    console.print(Panel.fit("[bold blue]CodeLens[/bold blue] v0.1.0", border_style="blue"))

    if args.command == "scan":
        handle_scan(args)
    elif args.command is None:
        parser.print_help()

if __name__ == "__main__":
    run_cli()