#!/usr/bin/env python3
"""Fail if a skill or command names a tool the MCP server does not have.

tools.txt is the server's tool list (regenerate it from the dashboard repo when tools change). Skills
reference tools by name, so a rename there must be reflected here.
"""
import pathlib
import re
import sys

root = pathlib.Path(__file__).resolve().parents[1]
tools = set((root / "tools.txt").read_text().split())
pattern = re.compile(r"`((?:get|list|query|evaluate|drill)_[a-z0-9_]+)")
bad = []
for path in sorted((root / "plugins").rglob("*.md")):
    for name in sorted(set(pattern.findall(path.read_text()))):
        if name not in tools:
            bad.append(f"{path.relative_to(root)}: unknown tool {name}")
print("\n".join(bad) or f"ok: every tool name matches tools.txt ({len(tools)} tools)")
sys.exit(1 if bad else 0)
