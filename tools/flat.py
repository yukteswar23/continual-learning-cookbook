import os, sys, re

src_root, out = sys.argv[1], sys.argv[2]
os.makedirs(out, exist_ok=True)
MAIN = {"2601.19897": "arxiv.tex", "2505.00661": "neurips_2025.tex", "2605.12484": "neurips_2026.tex"}
COMMENT = re.compile(r"(?<!\\)%.*")
INPUT = re.compile(r"\\(input|include)\{([^}]+)\}")


def expand(p, base, d=0):
    try:
        t = COMMENT.sub("", open(p, encoding="utf8", errors="ignore").read())
    except FileNotFoundError:
        return ""

    def rep(m):
        c = os.path.join(base, m.group(2).strip())
        c = c if c.endswith(".tex") else c + ".tex"
        return expand(c, base, d + 1) if d < 6 else ""
    return INPUT.sub(rep, t)


for pid in sorted(os.listdir(src_root)):
    base = os.path.join(src_root, pid, "x")
    if not os.path.isdir(base):
        continue
    t = expand(os.path.join(base, MAIN.get(pid, "main.tex")), base)
    i = t.find("\\begin{document}")
    t = t[i:] if i >= 0 else t
    t = re.sub(r"\n\s*\n+", "\n\n", t)
    open(os.path.join(out, pid + ".tex"), "w", encoding="utf8").write(t)
    print(pid, len(t), t.count("\n"))
