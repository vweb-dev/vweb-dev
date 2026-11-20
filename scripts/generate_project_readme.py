#!/usr/bin/env python3
"""Generate a code-derived README panel while keeping all existing author content."""
from __future__ import annotations
import collections
import html
import json
import os
from pathlib import Path
import subprocess

START = "<!-- VWEB:AUTO-README:START -->"
END = "<!-- VWEB:AUTO-README:END -->"
ASSET = "assets/vweb-readme-banner.svg"
EXTS = {".php":"PHP",".liquid":"Liquid",".ts":"TypeScript",".tsx":"TypeScript",".js":"JavaScript",".jsx":"JavaScript",".py":"Python",".html":"HTML",".css":"CSS",".json":"JSON",".java":"Java",".cs":"C#",".go":"Go",".rb":"Ruby"}
EXCLUDE = {"node_modules","vendor",".git",".vweb-readme-tools","dist","build","coverage",".next",".cache"}
def git(*args):
    try:
        return subprocess.check_output(["git",*args], stderr=subprocess.DEVNULL).decode("utf8","replace").strip()
    except Exception:
        return ""
def main():
    root=Path(".")
    name=os.environ.get("GITHUB_REPOSITORY",root.resolve().name).split("/")[-1]
    tracked=[x for x in git("ls-files","-z").split(chr(0)) if x]
    paths=[x for x in tracked if not EXCLUDE.intersection(Path(x).parts) and not any(z in Path(x).name.lower() for z in [".env","secret","password","credential",".key",".pem","token"])]
    counts=collections.Counter(EXTS[Path(x).suffix.lower()] for x in paths if Path(x).suffix.lower() in EXTS)
    folders=collections.Counter(Path(x).parts[0] for x in paths if len(Path(x).parts)>1 and not Path(x).parts[0].startswith("."))
    stack=[]
    check={"artisan":"Laravel","composer.json":"PHP / Composer","layout/theme.liquid":"Shopify Liquid Theme","shopify.app.toml":"Shopify App","next.config.ts":"Next.js","next.config.js":"Next.js","next.config.mjs":"Next.js","vite.config.ts":"Vite","vite.config.js":"Vite","Dockerfile":"Docker","manifest.webmanifest":"PWA"}
    stack += [label for file,label in check.items() if file in paths]
    for filename in ["package.json","composer.json"]:
        if filename not in paths: continue
        try:
            data=json.loads(Path(filename).read_text(encoding="utf8"))
            dependencies={**data.get("dependencies",{}),**data.get("devDependencies",{}),**data.get("require",{})}
            for dependency,label in [("next","Next.js"),("react","React"),("typescript","TypeScript"),("laravel/framework","Laravel"),("@shopify/shopify-app-react-router","Shopify App")]:
                if dependency in dependencies: stack.append(label)
        except (ValueError,OSError,TypeError): pass
    stack=sorted(set(stack))
    revision=os.environ.get("GITHUB_SHA","")[:12] or git("rev-parse","--short=12","HEAD")
    tech="  /  ".join(stack[:5] or [lang for lang,count in counts.most_common(3)] or ["SOURCE PROJECT"])
    brand=html.escape(name[:40])
    tech_html=html.escape(tech[:100])
    svg='''<svg xmlns="http://www.w3.org/2000/svg" width="1180" height="280" viewBox="0 0 1180 280" role="img" aria-label="PROJECT_NAME project overview"><title>PROJECT_NAME — project overview</title><defs><linearGradient id="gold"><stop stop-color="#f5e6c9"/><stop offset="1" stop-color="#c9a96e"/></linearGradient><style>text{font-family:Inter,Arial,sans-serif}.ring{transform-origin:980px 143px;animation:turn 28s linear infinite}@keyframes turn{to{transform:rotate(360deg)}}@media(prefers-reduced-motion:reduce){.ring{animation:none!important}}</style></defs><rect width="1180" height="280" rx="16" fill="#090d13"/><path d="M30 234H800" stroke="#c9a96e" stroke-width="1.6"/><text x="31" y="53" fill="#a8dec0" font-size="14" font-weight="650" letter-spacing="2">VWEB.DEV  /  SOURCE CODE</text><text x="29" y="125" fill="url(#gold)" font-size="56" font-weight="800">PROJECT_NAME</text><text x="32" y="166" fill="#f5f0e8" font-size="21">PROJECT ENGINEERING OVERVIEW</text><text x="32" y="207" fill="#aeb5bf" font-size="17">PROJECT_TECH</text><text x="31" y="260" fill="#c9a96e" font-size="12">SOURCE-DERIVED TECHNICAL SNAPSHOT</text><circle cx="980" cy="143" r="111" fill="none" stroke="#705a3c"/><g class="ring"><circle cx="980" cy="143" r="105" fill="none" stroke="#f5e6c9" stroke-width="3" stroke-dasharray="60 600"/></g><path d="M980 58L1058 99V191L980 230L902 191V99Z" fill="#17202b" stroke="#c9a96e" stroke-width="2"/><text x="980" y="136" font-size="29" fill="#f5e6c9" text-anchor="middle" font-weight="750">BUILD</text><text x="980" y="170" font-size="23" fill="#f5f0e8" text-anchor="middle">BETTER</text></svg>'''
    svg=svg.replace("PROJECT_NAME",brand).replace("PROJECT_TECH",tech_html)
    Path("assets").mkdir(exist_ok=True)
    Path(ASSET).write_text(svg,encoding="utf8")
    tick=chr(96)
    languages=", ".join(n+" ("+str(v)+")" for n,v in counts.most_common(6)) or "Not detected"
    topdirs=", ".join(folders.keys()) if not folders else ", ".join(p for p,n in folders.most_common(7))
    fragment="\n".join([
        START, '<div align="center"><img src="'+ASSET+'" width="100%" alt="'+brand+' project graphic" /></div>',
        "", "### Code-derived project snapshot", "",
        "| Attribute | Detected value |", "|---|---|",
        "| Latest source revision | "+tick+revision+tick+" |",
        "| Tracked files reviewed | "+str(len(paths))+" |",
        "| Framework and platform indicators | "+html.escape(tech or "Not detected")+" |",
        "| Source file types | "+html.escape(languages)+" |",
        "| Main directories | "+html.escape(topdirs or "No tracked directories")+" |",
        "", "> This section is regenerated from tracked filenames and manifests on code updates. It is not a QA or production-readiness certification. Handwritten project documentation is preserved.",
        END
    ])
    readme=Path("README.md")
    old=readme.read_text(encoding="utf8") if readme.exists() else "# "+name+"\n"
    if START in old and END in old:
        a=old.index(START);b=old.index(END,a)+len(END)
        new=old[:a]+fragment+old[b:]
    else:
        new=fragment+"\n\n"+old
    readme.write_text(new,encoding="utf8")
    print("Prepared",name,"revision",revision,"files",len(paths))
if __name__=="__main__":
    main()
