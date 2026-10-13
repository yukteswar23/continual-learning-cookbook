"""Parse arXiv LaTeX sources for figure environments (graphics + caption + label),
in document order following \\input/\\include, and render the graphics to PNG.
Usage: python -I figs.py <src_root> <out_root>
"""
import json, os, re, sys
import fitz  # PyMuPDF
from PIL import Image

src_root, out_root = sys.argv[1], sys.argv[2]
MAIN = {"2601.19897": "arxiv.tex", "2505.00661": "neurips_2025.tex", "2605.12484": "neurips_2026.tex"}


def strip_comments(t):
    return re.sub(r"(?<!\\)%.*", "", t)


def expand(path, base, depth=0):
    try:
        t = strip_comments(open(path, encoding="utf8", errors="ignore").read())
    except FileNotFoundError:
        return ""
    if depth > 6:
        return t

    def rep(m):
        name = m.group(2).strip()
        cand = os.path.join(base, name)
        if not cand.endswith(".tex"):
            cand += ".tex"
        return expand(cand, base, depth + 1)
    return re.sub(r"\\(input|include)\{([^}]+)\}", rep, t)


def balanced(t, i):
    """Return content of the {...} group starting at t[i] == '{'."""
    d, j = 0, i
    while j < len(t):
        if t[j] == "{":
            d += 1
        elif t[j] == "}":
            d -= 1
            if d == 0:
                return t[i + 1:j], j
        j += 1
    return t[i + 1:], len(t)


def find_file(base, name):
    for ext in ["", ".pdf", ".png", ".jpg", ".jpeg"]:
        p = os.path.join(base, name + ext)
        if os.path.isfile(p):
            return p
    return None


def render(src, dst):
    if src.lower().endswith(".pdf"):
        doc = fitz.open(src)
        page = doc[0]
        zoom = min(4.0, max(2.0, 2200 / max(page.rect.width, 1)))
        pix = page.get_pixmap(matrix=fitz.Matrix(zoom, zoom), alpha=False)
        pix.save(dst)
    else:
        im = Image.open(src).convert("RGB")
        im.save(dst)
    im = Image.open(dst)
    if im.width > 2000:
        im = im.resize((2000, int(im.height * 2000 / im.width)), Image.LANCZOS)
        im.save(dst)
    return Image.open(dst).size


report = {}
for pid in sorted(os.listdir(src_root)):
    base = os.path.join(src_root, pid, "x")
    if not os.path.isdir(base):
        continue
    main = MAIN.get(pid, "main.tex")
    text = expand(os.path.join(base, main), base)
    figs = []
    for m in re.finditer(r"\\begin\{(figure\*?|wrapfigure)\}(.*?)\\end\{\1\}", text, re.S):
        body = m.group(2)
        graphics = re.findall(r"\\includegraphics(?:\[[^\]]*\])?\{([^}]+)\}", body)
        cap = ""
        ci = body.find("\\caption")
        if ci >= 0:
            bi = body.find("{", ci)
            cap, _ = balanced(body, bi)
        label = re.findall(r"\\label\{([^}]+)\}", body)
        figs.append({"graphics": graphics, "caption": " ".join(cap.split()), "label": label[0] if label else ""})
    out_dir = os.path.join(out_root, pid)
    os.makedirs(out_dir, exist_ok=True)
    n = 0
    for fi, f in enumerate(figs, 1):
        f["n"] = fi
        f["png"] = []
        for gi, g in enumerate(f["graphics"]):
            p = find_file(base, g.strip())
            if not p:
                f["png"].append(None)
                continue
            dst = os.path.join(out_dir, f"fig{fi:02d}{('_' + str(gi + 1)) if len(f['graphics']) > 1 else ''}.png")
            try:
                size = render(p, dst)
                f["png"].append({"file": os.path.basename(dst), "w": size[0], "h": size[1]})
                n += 1
            except Exception as e:  # noqa
                f["png"].append({"error": str(e)})
    report[pid] = figs
    print(f"{pid}: {len(figs)} figure envs, {n} images rendered")

json.dump(report, open(os.path.join(out_root, "figures.json"), "w", encoding="utf8"), indent=1, ensure_ascii=False)
