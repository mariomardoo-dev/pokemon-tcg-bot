# -*- coding: utf-8 -*-
"""Hemsidan — läser James senaste scan och genererar products.json."""
import sys, os, json, subprocess

BASE = r"C:\Users\mario\Desktop\pokemon-hemsida"
SCAN_FILE = r"C:\Users\mario\Desktop\Hermes_Scanner\latest_scan.json"
os.chdir(BASE)

if not os.path.exists(SCAN_FILE):
    print(f"FEL: {SCAN_FILE} finns inte! James måste ha scannat först.")
    sys.exit(1)

with open(SCAN_FILE, encoding="utf-8") as f:
    all_products = json.load(f)

products = []
for p in all_products:
    products.append({
        "title": p.get("title", ""),
        "price": p.get("price", ""),
        "store": p.get("store", "?"),
        "status": p.get("status", "❌"),
        "url": p.get("url", ""),
        "image": p.get("image", "")
    })

stores = len(set(p["store"] for p in products))
in_stock = sum(1 for p in products if p["status"] == "✅")
print(f"{len(products)} produkter fran {stores} butiker ({in_stock} i lager)")

with open("products.json", "w", encoding="utf-8") as f:
    json.dump(products, f, ensure_ascii=False, indent=2)

subprocess.run(["git", "add", "products.json"], capture_output=True)
subprocess.run(["git", "commit", "-m", f"auto: {len(products)}p {stores}s"], capture_output=True)
r = subprocess.run(["git", "push"], capture_output=True, text=True)
if r.returncode == 0:
    print("Pushad! Render bygger om...")
else:
    print(f"Push-fel: {r.stderr.strip()}")
