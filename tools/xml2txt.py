"""Convert JATS full-text XML (Europe PMC) to readable text, keeping sections, figure captions, tables and formulas.
Usage: python -I xml2txt.py <in.xml> <out.txt>"""
import re, sys
import xml.etree.ElementTree as ET

src, dst = sys.argv[1], sys.argv[2]
root = ET.parse(src).getroot()
out = []


def text(el):
    return " ".join("".join(el.itertext()).split())


def walk(el, depth=0):
    tag = el.tag.split("}")[-1]
    if tag == "title" and depth:
        out.append("\n" + "#" * min(depth, 4) + " " + text(el))
        return
    if tag == "p":
        out.append(text(el))
        return
    if tag == "fig":
        lab = el.find("label")
        cap = el.find("caption")
        g = el.find("graphic")
        href = g.get("{http://www.w3.org/1999/xlink}href") if g is not None else ""
        out.append(f"\n[FIGURE {text(lab) if lab is not None else ''} | {href}] {text(cap) if cap is not None else ''}\n")
        return
    if tag == "table-wrap":
        out.append("\n[TABLE] " + text(el) + "\n")
        return
    if tag == "disp-formula":
        tex = el.find(".//{*}tex-math")
        out.append("\n$$ " + ("".join(tex.itertext()) if tex is not None else text(el)) + " $$\n")
        return
    if tag in ("ref-list", "back"):
        return
    for c in el:
        walk(c, depth + (1 if tag == "sec" else 0))


front = root.find(".//abstract")
if front is not None:
    out.append("ABSTRACT: " + text(front))
body = root.find(".//body")
walk(body, 0)
s = "\n".join(out)
s = re.sub(r"\n{3,}", "\n\n", s)
open(dst, "w", encoding="utf8").write(s)
print(dst, len(s))
