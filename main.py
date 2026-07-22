# -*- coding: utf-8 -*-
"""Pokesniper.se — Sveriges Pokemon TCG-prisjämförelse."""
from flask import Flask, request, jsonify, send_from_directory
import json, os, re
from pack_simulator import PACKS_HTML

app = Flask(__name__)
PRODUCTS_FILE = os.path.join(os.path.dirname(__file__), "products.json")
with open(PRODUCTS_FILE, encoding="utf-8") as f:
    PRODUCTS = json.load(f)

# --- filters ---
NON_POKEMON = {"lorcana","digimon","gundam","star wars","riftbound","magic:","flesh and blood",
               "one piece","disney","final fantasy","yugioh","yu-gi-oh","meta zoo","flesh&blood",
               "ultra pro","sleeves","deck box","binder","toploader","playmat","album",
               "portfolio","zipfolio","dice","sugarrush","tcgprotect","ultimate guard","gamegenic",
               "dragon shield","foldable","commander","playmats","prereleasekit"}

def is_pokemon(title):
    t = title.lower()
    for np in NON_POKEMON:
        if np in t: return False
    if "pokemon" in t or "pok\u00e9mon" in t or "pok\u00e9" in t: return True
    if "etb" in t or "elite trainer" in t: return True
    if "booster" in t and "display" in t: return True
    if "booster bundle" in t: return True
    if " booster " in t and "pack" not in t: return True
    if " tin " in t or t.endswith(" tin") or " tins " in t: return True
    if "battle deck" in t: return True
    if "blister" in t: return True
    if "premium collection" in t or "illustration collection" in t: return True
    if "checklane" in t or "poster collection" in t: return True
    if "mega evolution" in t or "ascended heroes" in t or "pitch black" in t: return True
    if "prismatic evolutions" in t or "stellar crown" in t or "shrouded fable" in t: return True
    if any(x in t for x in ["hidden fates","chilling reign","fusion strike","evolving skies",
                             "brilliant stars","lost origin","silver tempest","crown zenith",
                             "paldea","obsidian flames","paradox rift","temporal forces",
                             "twilight masquerade","sur spark"]): return True
    if "collection box" in t or "premium figure" in t: return True
    if "booster box" in t and "magic" not in t: return True
    if t.startswith("pok\u00e9mon ") or t.startswith("pokemon "): return True
    if " me" in t and ("evolution" in t or "booster" in t or "etb" in t): return True
    return False

BAD_URL = {"/collections/","/categories/"}
BAD_ENDS = {"booster-box","booster-packs","tins","etb","booster-bundle","pokemon-boxar",
            "pokemon-elite-trainer-box","pokemon-tins","booster","elite-trainer-box"}

def is_good_url(url):
    for b in BAD_URL:
        if b in url: return False
    from urllib.parse import urlparse
    parsed = urlparse(url)
    path_parts = [p for p in parsed.path.rstrip("/").split("/") if p]
    if path_parts:
        last = path_parts[-1].lower()
        if last in BAD_ENDS and len(path_parts) <= 2:
            return False
    return True

CAT_KEYS = {
    "ETB": ["elite trainer box"," etb "," etbs "],
    "Booster Box": ["booster box","booster display"],
    "Booster Bundle": ["booster bundle"],
    "Tin": [" tin "," tins "],
    "Booster": ["booster"],
    "Box Set": ["box","collection","premium"],
}

def cat_for(title):
    t = f" {title.lower()} "
    for cat, keys in CAT_KEYS.items():
        if any(k in t for k in keys):
            return cat
    return "\u00d6vrigt"

def norm(t):
    """Normalize product title for grouping."""
    hadEtb = bool(re.search(r'\b(?:elite trainer box|etb)\b', t, re.I))
    t = re.sub(r'\s*\(Max\s+\d+\s*(st)?\s*(per\s+(kund|hushåll|person))?\)', '', t, flags=re.I)
    t = re.sub(r'\s*\(Max\s+\d+(st)?\s*/\s*(kund|hushåll)\)', '', t, flags=re.I)
    t = re.sub(r'\s*\(Limit\s+\d+\s*per[^)]*\)', '', t, flags=re.I)
    t = re.sub(r'\s*\((ENG?|JP)\)\s*', '', t, flags=re.I)
    t = re.sub(r'\s*[\u2013\u2014\u2012-]\s*F\u00f6rhandsbokning\s*', '', t, flags=re.I)
    t = re.sub(r'\s*F\u00f6rhandsbokning\s*', '', t, flags=re.I)
    t = re.sub(r'^(Pok\u00e9mon\s*TCG[:\s,-]+|Pokemon\s*TCG[:\s,-]+|Pok\u00e9mon[:\s,-]+|Pokemon[:\s,-]+)', '', t, flags=re.I)
    t = re.sub(r'^(Mega\s*(?:&|and)?\s*Evolution\s*\d*\.?\d*[:\s,-]+|ME\d+\s+|Mega\s*Evolution\s*\d*\.?\d*\s+)', '', t, flags=re.I)
    t = re.sub(r'^[\u2013\u2014\u2012-]\s*', '', t)
    t = re.sub(r'\bElite\s+Trainer\s+Box\b', 'ETB', t, flags=re.I)
    t = re.sub(r'^(?:ETB\s*[\u2013\u2014\u2012-]\s*)?(Mega\s*(?:&|and)?\s*Evolution\s*\d*\.?\d*[:\s,-]+|ME\d+\s+|Mega\s*Evolution\s*\d*\.?\d*\s+)', '', t, flags=re.I)
    t = re.sub(r'^[\u2013\u2014\u2012-]\s*', '', t)
    t = re.sub(r'^(Mega\s*(?:&|and)?\s*Evolution\s*\d*\.?\d*[:\s,-]+|ME\d+\s+|Mega\s*Evolution\s*\d*\.?\d*\s+)', '', t, flags=re.I)
    t = re.sub(r'\s*[\u2013\u2014\u2012-]\s*Elite\s+Trainer\s+Box\b', ' ETB', t, flags=re.I)
    t = re.sub(r'\bElite\s+Trainer\s+Box\b', 'ETB', t, flags=re.I)
    t = re.sub(r'\bBooster\s+Display\s+Box\b', 'Booster Box', t, flags=re.I)
    t = re.sub(r'\s*\(ETB\)\s*', ' ETB ', t, flags=re.I)
    t = re.sub(r'\s+ETB\s+ETB\b', ' ETB', t, flags=re.I)
    t = re.sub(r'\s*[\u2013\u2014\u2012-]\s*ETB\b', ' ETB', t, flags=re.I)
    t = re.sub(r'\s+', ' ', t).strip().lower()
    if hadEtb and not re.search(r'\betb\b', t): t += ' etb'
    return t

def group_products(products):
    """Group products by normalized title, sort cheapest first within each group."""
    groups = {}
    for p in products:
        k = norm(p["title"])
        if k not in groups:
            groups[k] = {"title": p["title"], "image": p.get("image",""), "items": []}
        groups[k]["items"].append(p)
        if not groups[k]["image"] and p.get("image"):
            groups[k]["image"] = p["image"]
    
    result = []
    for g in groups.values():
        g["items"].sort(key=lambda x: int(re.sub(r'[^0-9]','',x.get("price","999999")) or "999999"))
        g["count"] = len(g["items"])
        g["cheapest"] = g["items"][0]["price"]
        g["in_stock"] = sum(1 for p in g["items"] if p.get("status") == "\u2705")
        result.append(g)
    
    result.sort(key=lambda x: (-x["in_stock"], int(re.sub(r'[^0-9]','',x.get("cheapest","999999")) or "999999")))
    return result

def search_products(q, cat=None, sort="relevance", limit=60):
    words = [w for w in q.lower().split() if w not in
             {"pokemon","tcg","pok\u00e9mon","the","a","an","max","per","sv","-"}]
    if "etb" in words:
        words = [w for w in words if w != "etb"] + ["elite","trainer","box"]
    results = []
    seen = set()
    for p in PRODUCTS:
        if not is_pokemon(p["title"]): continue
        if not is_good_url(p.get("url","")): continue
        if cat and cat_for(p["title"]) != cat: continue
        t = p["title"].lower()
        if not words:
            results.append(p)
            continue
        matched = sum(1 for w in words if len(w)>0 and w in t)
        needed = 1 if len(words)<=2 else max(1, len(words)-1)
        if matched >= needed:
            key = p["title"]+p["store"]
            if key not in seen:
                seen.add(key)
                results.append((matched, p))
    if words:
        results.sort(key=lambda x: (-x[0], 0 if x[1]["status"]=="\u2705" else 1))
        results = [r[1] for r in results]
    if sort == "price_asc":
        def _pr(x):
            try: return int(re.sub(r"[^0-9]","",x["price"])) if x["price"] else 999999
            except: return 999999
        results.sort(key=_pr)
    elif sort == "price_desc":
        def _pr2(x):
            try: return -int(re.sub(r"[^0-9]","",x["price"])) if x["price"] else -999999
            except: return -999999
        results.sort(key=_pr2)
    return results[:limit]

HTML = """<!DOCTYPE html>
<html lang="sv">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Pokesniper.se — J\u00e4mf\u00f6r priser p\u00e5 Pok\u00e9mon-kort</title>
<meta name="description" content="J\u00e4mf\u00f6r priser p\u00e5 Pok\u00e9mon TCG fr\u00e5n 45+ svenska butiker. 4293 produkter. Hitta b\u00e4sta pris p\u00e5 ETB, booster box, tins och mer.">
<meta property="og:title" content="Pokesniper.se — Sveriges Pok\u00e9mon-prisj\u00e4mf\u00f6relse">
<meta property="og:description" content="45+ butiker, 4293 produkter. Hitta billigaste Pok\u00e9mon-korten i Sverige.">
<style>
:root{--bg:#0a0a0a;--bg2:#111;--bg3:#1a1a1a;--red:#cc0000;--red2:#ff2222;--green:#22c55e;--text:#e0e0e0;--muted:#888;--border:#222}
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;background:var(--bg);color:var(--text);min-height:100vh}
a{color:var(--red);text-decoration:none}a:hover{color:var(--red2)}
header{background:linear-gradient(180deg,#150000,var(--bg));border-bottom:1px solid var(--border);padding:20px;position:sticky;top:0;z-index:100}
.header-inner{max-width:1200px;margin:0 auto;display:flex;align-items:center;gap:16px;flex-wrap:wrap}
.logo{font-size:22px;font-weight:800;color:var(--red);letter-spacing:2px;text-transform:uppercase;white-space:nowrap}
.logo span{color:var(--green);font-size:13px;display:block;letter-spacing:0;font-weight:400;text-transform:none}
.logo span .free{color:var(--red);font-weight:700;font-size:11px;letter-spacing:1px}
.disc-label{color:var(--muted);font-size:11px;text-align:center;margin-bottom:2px}
.disc-badge{background:#5865F2;border:1px solid #5865F2;border-radius:8px;padding:8px 12px;color:#fff;font-size:12px;white-space:nowrap;display:flex;align-items:center;gap:6px;transition:all .2s}
.disc-badge:hover{background:#4752C4;border-color:#4752C4}.disc-badge .icon{font-size:16px;font-weight:700}
.search-wrap{flex:1;min-width:200px;position:relative}
.search-wrap input{width:100%;padding:12px 16px;background:var(--bg2);border:1px solid var(--border);border-radius:8px;color:var(--text);font-size:15px;outline:none;transition:border-color .2s}
.search-wrap input:focus{border-color:var(--red)}.search-wrap input::placeholder{color:#555}
.clear-search{position:absolute;right:12px;top:50%;transform:translateY(-50%);background:none;border:none;color:var(--muted);cursor:pointer;font-size:18px;display:none}
.clear-search.visible{display:block}
nav{max-width:1200px;margin:16px auto 0;display:flex;gap:8px;flex-wrap:wrap;padding:0 20px}
.cat-pill{padding:8px 16px;border-radius:20px;border:1px solid var(--border);background:var(--bg2);color:var(--muted);cursor:pointer;font-size:13px;transition:all .2s;white-space:nowrap}
.cat-pill:hover,.cat-pill.active{background:#1a0000;border-color:var(--red);color:var(--red)}
main{max-width:1200px;margin:0 auto;padding:16px 20px}
.toolbar{display:flex;justify-content:space-between;align-items:center;margin-bottom:12px;flex-wrap:wrap;gap:8px}
.toolbar .count{color:var(--muted);font-size:13px}
.sort-select{padding:8px 12px;background:var(--bg2);border:1px solid var(--border);border-radius:6px;color:var(--text);font-size:13px;outline:none;cursor:pointer}
.group-card{background:var(--bg2);border:1px solid var(--border);border-radius:10px;overflow:hidden;transition:all .2s;padding:12px;margin-bottom:8px}
.group-card:hover{border-color:var(--red)}
.group-header{display:flex;gap:12px;cursor:pointer;align-items:flex-start}
.group-img{width:100px;height:100px;border-radius:8px;overflow:hidden;background:var(--bg3);flex-shrink:0;display:flex;align-items:center;justify-content:center}
.group-img img{width:100%;height:100%;object-fit:contain}
.group-img .no-img{font-size:32px;opacity:.3}
.group-info{flex:1;min-width:0}
.group-title{font-size:14px;font-weight:600;line-height:1.3}
.group-meta{display:flex;align-items:center;gap:8px;margin-top:6px;font-size:13px}
.group-price{color:var(--green);font-weight:700;font-size:16px}
.group-stores{color:var(--muted);font-size:12px}
.group-arrow{color:var(--muted);font-size:14px;transition:transform .2s;margin-left:8px}
.group-card.open .group-arrow{transform:rotate(180deg)}
.store-list{display:none;margin-top:12px;padding-top:12px;border-top:1px solid var(--border)}
.group-card.open .store-list{display:block}
.store-row{display:flex;align-items:center;justify-content:space-between;padding:6px 8px;border-radius:6px;transition:background .15s;cursor:pointer;gap:8px}
.store-row:hover{background:var(--bg3)}
.store-row .s-price{color:var(--green);font-weight:600;font-size:14px;white-space:nowrap;min-width:70px}
.store-row .s-store{color:var(--muted);font-size:13px;flex:1;min-width:0}
.store-row .s-status{font-size:11px;padding:2px 8px;border-radius:10px;white-space:nowrap}
.s-in{background:rgba(34,197,94,.1);color:var(--green)}.s-out{background:rgba(239,68,68,.15);color:#ef4444}
.fynd-section{margin-top:32px;border-top:1px solid var(--border);padding-top:20px}
.fynd-section h2{font-size:18px;color:var(--red);margin-bottom:12px;display:flex;align-items:center;gap:8px}
.fynd-section h2 .icon{font-size:22px}
.empty{text-align:center;padding:60px 20px;color:var(--muted)}
.empty .icon{font-size:48px;margin-bottom:12px}.empty p{font-size:15px}
footer{text-align:center;padding:32px;color:var(--muted);font-size:12px;border-top:1px solid var(--border);margin-top:40px}
footer a{color:var(--muted)}
@media(max-width:600px){.header-inner{flex-direction:column;align-items:stretch}.logo{text-align:center}.group-img{width:70px;height:70px}}
</style>
</head>
<body>
<header>
<div class=header-inner>
<div class=logo>Pokesniper<span>Scanna, hitta &amp; j\u00e4mf\u00f6r Pok\u00e9mon TCG<br><span class=free>HELT GRATIS</span></span></div>
<div class=search-wrap>
<input id=search placeholder="S\u00f6k produkt... (t.ex. 151, etb, pitch black, tins)" autofocus>
<button id=clear class=clear-search onclick="clearSearch()">\u2715</button>
</div>
<div>
<div class=disc-label>Vi finns \u00e4ven i Discord</div>
<a class=disc-badge href="https://discord.gg/QRaPfTVHFr" target=_blank><span class=icon><svg width=16 height=16 viewBox="0 0 24 24" fill=white><path d="M20.317 4.37a19.791 19.791 0 0 0-4.885-1.515.074.074 0 0 0-.079.037c-.21.375-.444.864-.608 1.25a18.27 18.27 0 0 0-5.487 0 12.64 12.64 0 0 0-.617-1.25.077.077 0 0 0-.079-.037A19.736 19.736 0 0 0 3.677 4.37a.07.07 0 0 0-.032.027C.533 9.046-.32 13.58.099 18.057a.082.082 0 0 0 .031.057 19.9 19.9 0 0 0 5.993 3.03.078.078 0 0 0 .084-.028 14.09 14.09 0 0 0 1.226-1.994.076.076 0 0 0-.041-.106 13.107 13.107 0 0 1-1.872-.892.077.077 0 0 1-.008-.128 10.2 10.2 0 0 0 .372-.292.074.074 0 0 1 .077-.01c3.928 1.793 8.18 1.793 12.062 0a.074.074 0 0 1 .078.01c.12.098.246.198.373.292a.077.077 0 0 1-.006.127 12.299 12.299 0 0 1-1.873.892.077.077 0 0 0-.041.107c.36.698.772 1.362 1.225 1.993a.076.076 0 0 0 .084.028 19.839 19.839 0 0 0 6.002-3.03.077.077 0 0 0 .032-.054c.5-5.177-.838-9.674-3.549-13.66a.061.061 0 0 0-.031-.03zM8.02 15.33c-1.183 0-2.157-1.085-2.157-2.419 0-1.333.956-2.419 2.157-2.419 1.21 0 2.176 1.096 2.157 2.42 0 1.333-.956 2.418-2.157 2.418zm7.975 0c-1.183 0-2.157-1.085-2.157-2.419 0-1.333.955-2.419 2.157-2.419 1.21 0 2.176 1.096 2.157 2.42 0 1.333-.946 2.418-2.157 2.418z"/></svg></span> Discord — smartare sök &amp; spårning</a>
</div>
<div class=header-stats id=stats></div>
</div>
</header>
<nav id=categories></nav>
<main>
<div class=toolbar>
<div class=count id=count></div>
<select class=sort-select id=sort onchange="doSearch()">
<option value=relevance>Relevans</option>
<option value=price_asc>Pris: l\u00e4gst f\u00f6rst</option>
<option value=price_desc>Pris: h\u00f6gst f\u00f6rst</option>
</select>
</div>
<div id=grid></div>
<div class=empty id=empty style=display:none>
<div class=icon>🔍</div>
<p>Hittade inga produkter</p>
</div>
<div class=fynd-section id=fynd-section style=display:none>
<h2><span class=icon>🔥</span> Dagens fynd — billigaste i lager</h2>
<div id=fynd-grid></div>
</div>
</main>
<footer>
Pokesniper.se — J\u00e4mf\u00f6r Pok\u00e9mon TCG-priser hos 45+ svenska butiker \u00b7 <a href="https://discord.gg/QRaPfTVHFr">Discord</a>
</footer>
<script>
console.log('JS loaded');
document.getElementById('stats').textContent = 'Laddar...';
fetch('/api/groups?q=&cat=&sort=relevance')
  .then(function(r){return r.json()})
  .then(function(data){
    document.getElementById('stats').textContent = data.total_products + ' produkter';
    document.getElementById('categories').innerHTML = '<button class=cat-pill>Test</button>';
  })
  .catch(function(e){
    document.getElementById('stats').textContent = 'Fel: ' + e.message;
  });
</script>
</body>
</html>"""

@app.route("/")
def index():
    return HTML

@app.route("/api/products")
def api_products():
    filtered = [p for p in PRODUCTS if is_pokemon(p["title"]) and is_good_url(p.get("url",""))]
    return jsonify(filtered)

@app.route("/api/groups")
def api_groups():
    q = request.args.get("q","").strip()
    cat = request.args.get("cat")
    sort = request.args.get("sort","relevance")
    limit = int(request.args.get("limit","80"))
    only_stock = request.args.get("only_stock","0") == "1"
    
    results = search_products(q, cat, sort, 200)
    
    # Count categories for all results
    all_products = [p for p in PRODUCTS if is_pokemon(p["title"]) and is_good_url(p.get("url",""))]
    cats = {}
    for p in all_products:
        c = cat_for(p["title"])
        cats[c] = cats.get(c, 0) + 1
    
    grouped = group_products(results)
    
    if only_stock:
        grouped = [g for g in grouped if g["in_stock"] > 0]
    
    # Count total unique stores in results
    stores = set()
    for g in grouped:
        for p in g["items"]:
            stores.add(p["store"])
    
    return jsonify({
        "groups": grouped[:limit],
        "total_products": len(all_products),
        "total_stores": len(set(p["store"] for p in all_products)),
        "categories": cats
    })

@app.route("/api/search")
def api_search():
    q = request.args.get("q","").strip()
    cat = request.args.get("cat")
    sort = request.args.get("sort","relevance")
    return jsonify(search_products(q, cat, sort))

@app.route("/sok")
def sok():
    q = request.args.get("q","").strip()
    return jsonify(search_products(q) if q else [])

@app.route("/google15a64bbd69393fe9.html")
def google_verify():
    return "google-site-verification: google15a64bbd69393fe9.html"

@app.route("/sitemap.xml")
def sitemap():
    popular = ["151","etb","tin","prismatic","mewtwo","pitch+black","team+rocket","booster+bundle","ascended+heroes","mega+evolution","stellar+crown","booster","elite+trainer+box","summer+ex","battle+deck","greninja","charizard","pokemon","tcg"]
    lines = ['<?xml version="1.0" encoding="UTF-8"?>']
    lines.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')
    lines.append('  <url><loc>https://pokesniper.se/</loc><priority>1.0</priority></url>')
    for q in popular:
        lines.append(f'  <url><loc>https://pokesniper.se/sok?q={q}</loc><priority>0.8</priority></url>')
    lines.append('</urlset>')
    return "\n".join(lines), 200, {"Content-Type": "application/xml"}

@app.route("/count")
def count():
    return str(len(PRODUCTS))

@app.route("/packs")
def packs():
    return PACKS_HTML

@app.route("/static/sets/<path:filename>")
def static_sets(filename):
    sets_dir = os.path.join(os.path.dirname(__file__), "static", "sets")
    return send_from_directory(sets_dir, filename)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
