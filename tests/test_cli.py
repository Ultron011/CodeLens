import pytest
from codelens.core.scanner import run_cli
import sys

def test_cli_scan_command_parsing(monkeypatch):
    """Tests if the 'scan' command is recognized properly."""
    # monkeypatch allows us to fake the command line arguments
    monkeypatch.setattr(sys, "argv", ["codelens", "scan", "."])
    
    try:
        run_cli()
    except SystemExit:
        pytest.fail("CLI exited unexpectedly")