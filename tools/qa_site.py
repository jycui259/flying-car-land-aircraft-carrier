# -*- coding: utf-8 -*-
"""Structural QA for the static site: tag balance, ids, links, images, citations."""
import os, re, sys, html
from html.parser import HTMLParser

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FILES = ["index.html", "assignment-1.html", "assignment-2.html", "references.html"]
VOID = {"area","base","br","col","embed","hr","img","input","link","meta","param",
        "source","track","wbr"}

class Checker(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack = []
        self.errors = []
        self.ids = {}
        self.hrefs = []
        self.imgs = []
        self.line = 1

    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        if "id" in d:
            self.ids.setdefault(d["id"], 0)
            self.ids[d["id"]] += 1
        if tag == "a" and "href" in d:
            self.hrefs.append(d["href"])
        if tag in ("img", "script", "link"):
            if tag == "img" and "src" in d:
                self.imgs.append(d["src"])
            if tag in ("script", "link") and ("src" in d or "href" in d):
                self.imgs.append(d.get("src") or d.get("href"))
        if tag not in VOID:
            self.stack.append((tag, self.getpos()[0]))

    def handle_endtag(self, tag):
        if tag in VOID:
            return
        if not self.stack:
            self.errors.append(f"line {self.getpos()[0]}: stray </{tag}>")
            return
        if self.stack[-1][0] == tag:
            self.stack.pop()
        else:
            # find in stack
            idx = None
            for i in range(len(self.stack) - 1, -1, -1):
                if self.stack[i][0] == tag:
                    idx = i
                    break
            if idx is None:
                self.errors.append(f"line {self.getpos()[0]}: unexpected </{tag}> (open: {self.stack[-3:]})")
            else:
                for t, ln in self.stack[idx + 1:]:
                    self.errors.append(f"line {ln}: <{t}> not closed before </{tag}> at {self.getpos()[0]}")
                del self.stack[idx:]

def main():
    ok = True
    parsed = {}
    for f in FILES:
        c = Checker()
        c.feed(open(os.path.join(ROOT, f), encoding="utf-8").read())
        c.close()
        parsed[f] = c

    for f in FILES:
        c = parsed[f]
        if c.stack:
            print(f"[{f}] UNCLOSED: {c.stack[-5:]}")
            ok = False
        for e in c.errors[:12]:
            print(f"[{f}] {e}")
            ok = False
        dup = {k: v for k, v in c.ids.items() if v > 1}
        if dup:
            print(f"[{f}] DUPLICATE IDS: {dup}")
            ok = False

    for f in FILES:
        c = parsed[f]
        for h in c.hrefs:
            if h.startswith("http") or h.startswith("mailto:"):
                continue
            if h.startswith("#"):
                if len(h) > 1 and h[1:] not in c.ids:
                    print(f"[{f}] missing anchor {h}")
                    ok = False
                continue
            target, _, frag = h.partition("#")
            if not target:
                continue
            tp = os.path.join(ROOT, target)
            if not os.path.exists(tp):
                print(f"[{f}] missing page {target}")
                ok = False
            elif frag and frag not in parsed.get(target, Checker()).ids:
                print(f"[{f}] missing target anchor {h}")
                ok = False
        for s in c.imgs:
            if s and not s.startswith("http") and not s.startswith("data:"):
                if not os.path.exists(os.path.join(ROOT, s)):
                    print(f"[{f}] missing asset {s}")
                    ok = False

    ref = parsed["references.html"].ids
    for f in FILES:
        src = open(os.path.join(ROOT, f), encoding="utf-8").read()
        nums = sorted({int(m.group(1)) for m in re.finditer(r"references\.html#r(\d+)", src)})
        missing = [n for n in nums if f"r{n}" not in ref]
        if missing:
            print(f"[{f}] citations without entries: {missing}")
            ok = False
        print(f"{f}: cites r{nums}")
    print("OK" if ok else "FAILED")
    return 0 if ok else 1

if __name__ == "__main__":
    sys.exit(main())
