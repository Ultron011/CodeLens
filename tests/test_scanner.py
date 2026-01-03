import os
import pytest
import sys
from codelens.core.scanner import CodeScanner

def test_list_files_ignore_hidden_dirs(tmp_path):
    d = tmp_path / "project"
    d.mkdir()
    (d / "main.py").write_text("print('hello')")

    hidden = d / ".git"
    hidden.mkdir()
    (hidden / "config").write_text("secret")

    scanner = CodeScanner(root_dir=str(d))
    files = scanner.get_all_files()

    assert len(files) == 1
    assert "main.py" in str(files[0])
    assert ".git" not in str(files[0])

