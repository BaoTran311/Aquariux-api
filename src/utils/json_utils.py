import json
import re


def truncate_json(data: dict | str, lines: int = 8) -> str:
    if isinstance(data, str):
        try:
            data = json.loads(data)
        except Exception:
            return data

    formatted = json.dumps(data, indent=3, ensure_ascii=False)
    split_lines = formatted.splitlines()

    if len(split_lines) > lines:
        first_key_indent = re.match(r"(\s*)", split_lines[1]).group(1)
        return "\n".join(split_lines[:lines]) + f"\n{first_key_indent}...\n" + "}"
    return formatted

def extract_json_objects(s: str):
    objs = []
    depth = 0
    start = None
    for i, ch in enumerate(s):
        if ch == '{':
            if depth == 0:
                start = i
            depth += 1
        elif ch == '}':
            depth -= 1
            if depth == 0 and start is not None:
                objs.append(s[start:i+1])
    return objs