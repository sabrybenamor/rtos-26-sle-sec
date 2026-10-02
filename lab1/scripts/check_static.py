#!/usr/bin/env python3
"""Static hint for Lab 1: is every variable written by the SIGALRM handler
declared `volatile sig_atomic_t`?

Reads C code on stdin, with comments already stripped (run_and_check.sh does
it with gcc). Prints a WARNING per problem; never fails (exit status 0).

  1. find the handler: signal(SIGALRM, X), or sa.sa_handler / sa.sa_sigaction = X;
  2. collect the variables its body writes: v++, ++v, v--, --v, v = ..., v += ...;
  3. for each one declared at file scope, check that its declaration contains
     both `volatile` and `sig_atomic_t`.
Variables with no file-scope declaration (locals, errno, ...) are skipped.
"""
import re
import sys

text = sys.stdin.read()
text = re.sub(r'"(?:\\.|[^"\\\n])*"', '""', text)          # string literals
text = re.sub(r"'(?:\\.|[^'\\\n])*'", "''", text)          # char literals
text = re.sub(r"^\s*#.*$", "", text, flags=re.M)           # preprocessor lines

CAST = r"(?:\(\s*void\s*\(\s*\*\s*\)\s*\([^()]*\)\s*\)\s*)?"
SKIP = {"SIG_IGN", "SIG_DFL", "NULL"}

found = set(re.findall(r"\bsignal\s*\(\s*SIGALRM\s*,\s*" + CAST + r"&?\s*(\w+)", text))
found |= set(re.findall(r"\.\s*sa_(?:handler|sigaction)\s*=\s*" + CAST + r"&?\s*(\w+)", text))
handlers = found - SKIP
installs = re.search(r"\b(signal|sigaction)\s*\(", text)


def coarse_check():
    """Used when the handler's code cannot be found."""
    if "volatile" not in text:
        print("WARNING: you install a signal handler but nothing is declared volatile.")
        print("         A variable shared with a handler must be 'volatile sig_atomic_t'.")
    sys.exit(0)


if installs and not found:
    coarse_check()

# Brace depth at every position, to tell file scope (depth 0) from bodies.
depth = []
d = 0
for c in text:
    if c == "}":
        d -= 1
    depth.append(d)
    if c == "{":
        d += 1


def body_of(name):
    """Text of the definition of function `name`, or None."""
    for m in re.finditer(r"\b" + name + r"\s*\([^;{}]*\)\s*\{", text):
        if depth[m.start()] != 0:
            continue
        start = i = m.end()
        level = 1
        while i < len(text) and level:
            level += {"{": 1, "}": -1}.get(text[i], 0)
            i += 1
        return text[start:i - 1]
    return None


def written(body):
    """Names of the variables a function body writes (not members)."""
    names = set()
    names |= set(re.findall(r"(?<![\w.>])(\w+)\s*(?:\+\+|--)", body))
    names |= set(re.findall(r"(?:\+\+|--)\s*(\w+)", body))
    names |= set(re.findall(r"(?<![\w.>])(\w+)\s*(?:\[[^\]]*\])?\s*"
                            r"(?:[-+*/%&|^]|<<|>>)?=(?!=)", body))
    return names


# File-scope statements (the text between `;`, `{`, `}` at depth 0). A piece
# that starts inside braces is a function or struct body: skipped.
statements = []
start = 0
for i, c in enumerate(text):
    if c in ";{}" and depth[i] == 0:
        if start >= len(depth) or depth[start] == 0:
            statements.append(text[start:i].strip())
        start = i + 1


def declarations(name):
    """File-scope declarations of variable `name` (the words before it)."""
    decl = re.compile(r"^([\w\s*]*?)\b" + name + r"\s*(?:\[[^\]]*\])?\s*(?:=.*)?$", re.S)
    return [m.group(1) for s in statements if (m := decl.match(s)) and m.group(1).strip()]


bodies = {h: b for h in sorted(handlers) if (b := body_of(h)) is not None}
if handlers and not bodies:
    coarse_check()

warned = set()
for h, body in bodies.items():
    for v in sorted(written(body)):
        for words in declarations(v):
            words = words.split()
            if "volatile" in words and "sig_atomic_t" in words or v in warned:
                continue
            warned.add(v)
            missing = [w for w in ("volatile", "sig_atomic_t") if w not in words]
            print(f"WARNING: '{v}' is written by the handler {h}() but is not "
                  f"declared 'volatile sig_atomic_t' (missing: {', '.join(missing)}).")
            print("         See README, 'The volatile lesson'.")
