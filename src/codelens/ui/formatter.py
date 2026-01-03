from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from collections import Counter

console = Console()

def print_header(version: str):
    console.print(Panel.fit(f"[bold blue]CodeLens[/bold blue] {version}", border_style="blue"))

def display_scan_results(path: str, files: list, total_chunks: int):
    table = Table(title=f"Scan Summary: {path}", show_header=True, header_style="bold magenta")
    table.add_column("Extension", style="dim")
    table.add_column("Count", justify="right")

    extensions = Counter(f.suffix if f.suffix else "No Extension" for f in files)
    for ext, count in extensions.items():
        table.add_row(ext, str(count))

    console.print(table)
    console.print(f"\n[bold green]✔ Scan Complete![/bold green] Found {len(files)} files.")
    console.print(f"Total Logical Chunks: [bold cyan]{total_chunks}[/bold cyan]\n")