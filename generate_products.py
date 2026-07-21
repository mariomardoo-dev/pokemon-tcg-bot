import sys, json
sys.path.insert(0, r"C:\Users\mario\Desktop\Hermes_Scanner")
from scanner import check_maxgaming, is_wanted_product

results = check_maxgaming()
products = []
for r in results:
    if not is_wanted_product(r[1]):
        continue
    status, title, price, url = r
    store = "MaxGaming"
    products.append({
        "title": title,
        "price": price if price else "",
        "store": store,
        "status": "✅" if status == "✅" else "❌",
        "url": url
    })

with open(r"C:\Users\mario\Desktop\pokemon-hemsida\products.json", "w", encoding="utf-8") as f:
    json.dump(products, f, ensure_ascii=False, indent=2)

print(f"Generated {len(products)} products")
