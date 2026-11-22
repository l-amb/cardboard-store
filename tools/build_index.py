#!/usr/bin/env python3
"""Builds index.json, the catalog the CardboardXR store reads, from the folders in apps/.

    python3 tools/build_index.py          # writes index.json
    python3 tools/build_index.py --check  # exits 1 if index.json is out of date (for CI)

Each apps/<id>/ holds app.json and the app's Lua files. Run this, then commit and push; the store
sees the change within a few minutes. The same rules the store applies are checked here first, so
a mistake shows up now rather than as a skipped app on the phone.
"""
import hashlib
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APPS = os.path.join(ROOT, "apps")
MAX_FILES, MAX_FILE, MAX_TOTAL = 64, 512 * 1024, 4 * 1024 * 1024
ALLOWED = {".lua", ".json", ".txt", ".md"}
NAME_CHARS = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-.")


def fail(message):
    print("error: " + message, file=sys.stderr)
    sys.exit(1)


def valid_id(value):
    ok = set("abcdefghijklmnopqrstuvwxyz0123456789")
    return (isinstance(value, str) and 2 <= len(value) <= 40 and value[0] in ok
            and all(c in ok or c == "-" for c in value))


def valid_version(value):
    parts = str(value).split(".")
    return 1 <= len(parts) <= 4 and all(p.isdigit() and len(p) <= 6 for p in parts)


def safe_path(rel):
    if not rel or len(rel) > 100 or rel.startswith("/"):
        return False
    segments = rel.split("/")
    if len(segments) > 4:
        return False
    for s in segments:
        if not s or s.startswith(".") or any(c not in NAME_CHARS for c in s):
            return False
    return os.path.splitext(rel)[1].lower() in ALLOWED


def no_controls(text):
    return all(ord(c) >= 32 for c in text)


def build_app(folder):
    app_dir = os.path.join(APPS, folder)
    manifest_path = os.path.join(app_dir, "app.json")
    if not os.path.isfile(manifest_path):
        fail(f"apps/{folder} has no app.json")
    with open(manifest_path, encoding="utf-8") as handle:
        manifest = json.load(handle)
    where = f"apps/{folder}/app.json"
    if manifest.get("id") != folder or not valid_id(folder):
        fail(f"{where}: id must equal the folder name, lowercase letters, digits and dashes")
    if not str(manifest.get("name", "")).strip() or len(manifest["name"]) > 60:
        fail(f"{where}: name is missing or too long")
    if not valid_version(manifest.get("version")):
        fail(f"{where}: version must be like 1 or 1.2.3")
    entry = manifest.get("entry", "main.lua")
    if not safe_path(entry) or not entry.endswith(".lua"):
        fail(f"{where}: entry must be a .lua file in the folder")
    if len(manifest.get("description", "")) > 400 or len(manifest.get("author", "")) > 60:
        fail(f"{where}: description (400) or author (60) is too long")
    for key in ("name", "author", "description", "icon"):
        if not no_controls(str(manifest.get(key, ""))):
            fail(f"{where}: {key} has a control character")

    files = []
    total = 0
    for current, _dirs, names in os.walk(app_dir):
        for name in sorted(names):
            full = os.path.join(current, name)
            rel = os.path.relpath(full, app_dir).replace(os.sep, "/")
            if not safe_path(rel):
                fail(f"apps/{folder}/{rel}: not an allowed file (names use letters, digits, _ - . ; kinds are .lua .json .txt .md)")
            data = open(full, "rb").read()
            if len(data) > MAX_FILE:
                fail(f"apps/{folder}/{rel} is over {MAX_FILE // 1024} KB")
            total += len(data)
            files.append({"path": rel, "sha256": hashlib.sha256(data).hexdigest(), "size": len(data)})
    files.sort(key=lambda f: f["path"])
    if len(files) > MAX_FILES or total > MAX_TOTAL:
        fail(f"apps/{folder} is over the limits ({MAX_FILES} files, {MAX_TOTAL // 1024 // 1024} MB)")
    if not any(f["path"] == entry for f in files):
        fail(f"apps/{folder}: entry {entry} isn't in the folder")
    return {
        "id": folder,
        "name": manifest["name"],
        "version": str(manifest["version"]),
        "author": manifest.get("author", ""),
        "description": manifest.get("description", ""),
        "icon": manifest.get("icon", "apps"),
        "entry": entry,
        "api": int(manifest.get("api", 1)),
        "files": files,
    }


def main():
    folders = sorted(f for f in os.listdir(APPS) if os.path.isdir(os.path.join(APPS, f)))
    index = {"format": 1, "apps": [build_app(f) for f in folders]}
    text = json.dumps(index, indent=1, ensure_ascii=False) + "\n"
    target = os.path.join(ROOT, "index.json")
    if "--check" in sys.argv:
        current = open(target, encoding="utf-8").read() if os.path.isfile(target) else ""
        if current != text:
            fail("index.json is out of date: run python3 tools/build_index.py")
        print("index.json is up to date")
        return
    with open(target, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(text)
    print(f"Wrote index.json with {len(index['apps'])} apps")


if __name__ == "__main__":
    main()
