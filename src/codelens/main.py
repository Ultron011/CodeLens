import argparse
from codelens.core.scanner import CodeScanner
from codelens.ui.formatter import print_header, display_scan_results
from codelens.core.parser import CodeParser

def handle_scan(args):
    scanner = CodeScanner(args.path)
    files = scanner.get_all_files()
    
    parser = CodeParser()
    total_chunks = 0
    for file_path in files:
        if file_path.suffix == ".py":
            content = file_path.read_text(errors="ignore")
            total_chunks += len(parser.parse_text(content))
            
    display_scan_results(args.path, files, total_chunks)

def run_cli():
    parser = argparse.ArgumentParser(prog="codelens")
    subparsers = parser.add_subparsers(dest="command")

    scan_parser = subparsers.add_parser("scan")
    scan_parser.add_argument("path", type=str)
    
    args = parser.parse_args()
    print_header("v0.1.0")

    if args.command == "scan":
        handle_scan(args)
    else:
        parser.print_help()