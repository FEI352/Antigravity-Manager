#!/usr/bin/env python3
"""
strip-apikey-fun.py — Deterministic patch to strip apikey-fun (promotional/affiliate page)
from Antigravity Manager source code.
"""

import os, re, sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def patch_navbar():
    path = os.path.join(REPO_ROOT, "src", "components", "navbar", "Navbar.tsx")
    if not os.path.exists(path): return
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()
    text = re.sub(r",\s*KeyRound", "", text)
    text = re.sub(r"KeyRound,\s*", "", text)
    text = re.sub(r"\s*\{\s*path:\s*'/apikey-fun'[^}]+\},?", "", text)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    print("Patched Navbar.tsx")

def patch_settings():
    path = os.path.join(REPO_ROOT, "src", "pages", "Settings.tsx")
    if not os.path.exists(path): return
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()
    text = re.sub(r",\s*KeyRound", "", text)
    text = re.sub(r"KeyRound,\s*", "", text)
    text = re.sub(r"\s*\{\s*path:\s*'/apikey-fun'[^}]+\},?", "", text)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    print("Patched Settings.tsx")

def patch_nav_menu():
    path = os.path.join(REPO_ROOT, "src", "components", "navbar", "NavMenu.tsx")
    if not os.path.exists(path): return
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()
    text = text.replace("isDouble11Active, ", "").replace(", isDouble11Active", "")
    # Remove any apikey-fun / double11 event badge logic
    text = re.sub(r"const isApiKeyFun = item\.path === '/apikey-fun';\s*", "", text)
    text = re.sub(r"const showEventBadge = isApiKeyFun && isDouble11Active\(\);\s*", "", text)
    text = re.sub(r"\$\{showEventBadge \? '[^']+' : '([^']+)'\}", r"\1", text)
    text = re.sub(r"\{/\* \[TEMPORARY_EVENT: DOUBLE11_2026\].*?\{showEventBadge && \(.*?</span>\s*\)\}\s*", "", text, flags=re.DOTALL)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    print("Patched NavMenu.tsx")

def patch_nav_dropdowns():
    path = os.path.join(REPO_ROOT, "src", "components", "navbar", "NavDropdowns.tsx")
    if not os.path.exists(path): return
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()
    text = text.replace("isDouble11Active, ", "").replace(", isDouble11Active", "")
    text = re.sub(r"const isApiKeyFun = item\.path === '/apikey-fun';\s*", "", text)
    text = re.sub(r"const showEventBadge = isApiKeyFun && isDouble11Active\(\);\s*", "", text)
    text = re.sub(r"\{/\* \[TEMPORARY_EVENT: DOUBLE11_2026\].*?\{showEventBadge && \(.*?</span>\s*\)\}\s*", "", text, flags=re.DOTALL)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    print("Patched NavDropdowns.tsx")

def patch_app():
    path = os.path.join(REPO_ROOT, "src", "App.tsx")
    if not os.path.exists(path): return
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()
    text = re.sub(r"import\s*\{\s*ApiKeyFun\s*\}\s*from\s*'./pages/ApiKeyFun';\n?", "", text)
    text = re.sub(
        r"\{\s*path:\s*'apikey-fun',\s*element:\s*<ApiKeyFun\s*/>,?\s*\},?",
        "{\n        path: 'apikey-fun',\n        element: <Navigate to=\"/\" replace />,\n      },",
        text
    )
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    print("Patched App.tsx")

def remove_files():
    for rel in ["src/pages/ApiKeyFun.tsx", "docs/images/APIKEYFUN.png"]:
        p = os.path.join(REPO_ROOT, rel)
        if os.path.exists(p):
            os.remove(p)
            print(f"Removed {rel}")

def main():
    patch_navbar()
    patch_settings()
    patch_nav_menu()
    patch_nav_dropdowns()
    patch_app()
    remove_files()
    print("All apikey-fun components stripped successfully.")

if __name__ == "__main__":
    main()
