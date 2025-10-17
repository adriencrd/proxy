#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Minimal, rapide — teste tous les proxys de Https.txt et écrit valid_proxies.txt

import re, sys, time, random, os
from concurrent.futures import ThreadPoolExecutor, as_completed
import requests
from requests.exceptions import RequestException

INPUT = "Https.txt"
OUTPUT = "valid_proxies.txt"
TIMEOUT = 2.0
MAX_WORKERS = 200
PROXY_RE = re.compile(r'^(?:(?:https?|socks5h?)://)?(?:\S+?:\S+?@)?(?:\d{1,3}\.){3}\d{1,3}:\d{2,5}$')

def ok_once(proxy, url):
    p = proxy if "://" in proxy else "http://" + proxy
    proxies = {"http": p, "https": p}
    headers = {"User-Agent":"proxy-tester-mini"}
    t0 = time.time()
    try:
        r = requests.head(url, proxies=proxies, timeout=TIMEOUT, headers=headers, allow_redirects=False, verify=False)
        code = r.status_code
        if code in (405,501):
            r = requests.get(url, proxies=proxies, timeout=TIMEOUT, headers=headers, allow_redirects=False, verify=False)
            code = r.status_code
        return code < 400, int((time.time()-t0)*1000), f"HTTP {code}"
    except RequestException as e:
        return False, int((time.time()-t0)*1000), type(e).__name__

def main():
    infile = sys.argv[1] if len(sys.argv)>1 else INPUT
    url = input("URL à tester (ex: https://example.com) : ").strip() or "https://example.com"
    if "://" not in url: url = "http://" + url

    if not os.path.exists(infile):
        print("Fichier introuvable:", infile); return

    with open(infile, "r", encoding="utf-8", errors="ignore") as f:
        lines = [ln.strip() for ln in f if ln.strip() and not ln.strip().startswith("#")]

    proxies = [ln for ln in lines if PROXY_RE.match(ln)]
    if not proxies:
        print("Aucun proxy valide trouvé dans", infile); return

    random.shuffle(proxies)
    open(OUTPUT, "w").close()
    workers = min(MAX_WORKERS, max(8, len(proxies)))

    with ThreadPoolExecutor(max_workers=workers) as ex:
        futures = {ex.submit(ok_once, p, url): p for p in proxies}
        for fut in as_completed(futures):
            p = futures[fut]
            try:
                ok, ms, msg = fut.result()
            except Exception as e:
                print("[ERR] ", p, e); continue
            if ok:
                print("[OK] ", p, f"({msg}, {ms}ms)")
                with open(OUTPUT, "a", encoding="utf-8") as out:
                    out.write(p + "\n")
            else:
                print("[BAD]", p, f"({msg}, {ms}ms)")

    print("Fini — proxys valides ajoutés dans", OUTPUT)

if __name__ == "__main__":
    main()
