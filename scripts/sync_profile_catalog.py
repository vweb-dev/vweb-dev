#!/usr/bin/env python3
"""Refresh only public vweb-dev repositories using GitHub's public API."""
from pathlib import Path
import json
import os
import urllib.request

START="<!-- VWEB:PUBLIC-REPOS:START -->"
END="<!-- VWEB:PUBLIC-REPOS:END -->"
BUCKETS=["PHP / Laravel","Shopify / Commerce","Applications & Websites","Utilities & Tools","Community & Upstream"]
def category(x):
    n=x["name"].lower(); lang=(x.get("language") or "").lower()
    if x.get("fork"): return BUCKETS[4]
    if "shopify" in n or lang=="liquid": return BUCKETS[1]
    if lang=="php" or any(k in n for k in ["booking-jules","connect.vweb.dev","taskreminder","vapsstore"]): return BUCKETS[0]
    if any(k in n for k in ["calculator","rdp","openboard","activation","filee","api-anything","motion-design","swarm","typer"]): return BUCKETS[3]
    return BUCKETS[2]
def main():
    repos=[]
    for page in range(1,5):
        headers={"Accept":"application/vnd.github+json","User-Agent":"VWEB.DEV-README-DIRECTORY"}
        token=os.getenv("GH_TOKEN","")
        if token: headers["Authorization"]="Bearer "+token
        url="https://api.github.com/users/vweb-dev/repos?type=owner&per_page=100&page="+str(page)
        with urllib.request.urlopen(urllib.request.Request(url,headers=headers),timeout=30) as request:
            batch=json.load(request)
        repos.extend(x for x in batch if not x.get("private") and x["name"].lower()!="vweb-dev" and x["owner"]["login"].lower()=="vweb-dev")
        if len(batch)<100: break
    groups={k:[] for k in BUCKETS}
    for repo in repos: groups[category(repo)].append(repo)
    out=[START,"## Public project directory","", "**"+str(len(repos))+" public project repositories**, automatically synced from GitHub. Private work remains private.",""]
    for name in BUCKETS:
        if not groups[name]: continue
        out.extend(["### "+name,"","| Repository | GitHub language |","|---|---|"])
        for x in sorted(groups[name],key=lambda q:q["name"].lower()):
            out.append("| ["+x["name"].replace("|","")+" ]("+x["html_url"]+") | "+str(x.get("language") or "Unclassified").replace("|","")+" |")
        out.append("")
    out.extend(["<sub>Only public metadata is used. Directory refresh is scheduled; empty, template and upstream repositories are not necessarily completed VWEB.DEV products.</sub>",END])
    body="\n".join(out)
    target=Path("README.md"); original=target.read_text(encoding="utf8")
    if START in original and END in original:
        a=original.index(START);b=original.index(END,a)+len(END)
        target.write_text(original[:a]+body+original[b:],encoding="utf8")
    else:
        target.write_text(original+"\n\n"+body+"\n",encoding="utf8")
    print("Public repositories indexed:",len(repos))
if __name__=="__main__":main()
