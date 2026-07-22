# -*- coding: utf-8 -*-
"""Pokesniper.se — Sveriges Pokemon TCG-prisjämförelse."""
from flask import Flask, request, jsonify
import json, os, re

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
    if "pokemon" in t or "pokémon" in t or "poké" in t: return True
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
    if "hidden fates" in t or "chilling reign" in t or "fusion strike" in t: return True
    if "evolving skies" in t or "brilliant stars" in t or "lost origin" in t: return True
    if "silver tempest" in t or "crown zenith" in t or "scarlet" in t: return True
    if "paldea" in t or "obsidian flames" in t or "paradox rift" in t: return True
    if "temporal forces" in t or "twilight masquerade" in t or "sur spark" in t: return True
    if "collection box" in t or "premium figure" in t: return True
    if "booster box" in t and "magic" not in t: return True
    if t.startswith("pokémon ") or t.startswith("pokemon ") or "pokémon " in t or "pokemon " in t: return True
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
    return "Övrigt"

def search_products(q, cat=None, sort="relevance", limit=60):
    words = [w for w in q.lower().split() if w not in
             {"pokemon","tcg","pokémon","the","a","an","max","per","sv","-"}]
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
        results.sort(key=lambda x: (-x[0], 0 if x[1]["status"]=="✅" else 1))
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
<title>Pokesniper.se — Jämför priser på Pokémon-kort</title>
<meta name="description" content="Jämför priser på Pokémon TCG från 45+ svenska butiker. 4293 produkter. Hitta bästa pris på ETB, booster box, tins och mer.">
<meta property="og:title" content="Pokesniper.se — Sveriges Pokémon-prisjämförelse">
<meta property="og:description" content="45+ butiker, 4293 produkter. Hitta billigaste Pokémon-korten i Sverige.">

<style>
:root{--bg:#0a0a0a;--bg2:#111;--bg3:#1a1a1a;--red:#cc0000;--red2:#ff2222;--green:#22c55e;--text:#e0e0e0;--muted:#888;--border:#222}
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;background:var(--bg);color:var(--text);min-height:100vh}
a{color:var(--red);text-decoration:none}
a:hover{color:var(--red2)}

header{background:linear-gradient(180deg,#150000,var(--bg));border-bottom:1px solid var(--border);padding:20px;position:sticky;top:0;z-index:100}
.header-inner{max-width:1200px;margin:0 auto;display:flex;align-items:center;gap:16px;flex-wrap:wrap}
.logo{font-size:22px;font-weight:800;color:var(--red);letter-spacing:2px;text-transform:uppercase;white-space:nowrap}
.logo span{color:var(--green);font-size:13px;display:block;letter-spacing:0;font-weight:400;text-transform:none}
.logo span .free{color:var(--red);font-weight:700;font-size:11px;letter-spacing:1px}
.discord-label{color:var(--muted);font-size:11px;text-align:center;margin-bottom:2px}
.discord-badge{background:#1a0000;border:1px solid var(--red);border-radius:8px;padding:8px 12px;color:var(--text);font-size:12px;white-space:nowrap;display:flex;align-items:center;gap:6px;transition:all .2s}
.discord-badge:hover{background:#2a0000;border-color:var(--red2)}
.discord-badge .icon{font-size:16px}
.search-wrap{flex:1;min-width:200px;position:relative}
.search-wrap input{width:100%;padding:12px 16px;background:var(--bg2);border:1px solid var(--border);border-radius:8px;color:var(--text);font-size:15px;outline:none;transition:border-color .2s}
.search-wrap input:focus{border-color:var(--red)}
.search-wrap input::placeholder{color:#555}
.clear-search{position:absolute;right:12px;top:50%;transform:translateY(-50%);background:none;border:none;color:var(--muted);cursor:pointer;font-size:18px;display:none}
.clear-search.visible{display:block}
.header-stats{color:var(--muted);font-size:12px}

nav{max-width:1200px;margin:16px auto 0;display:flex;gap:8px;flex-wrap:wrap;padding:0 20px}
.cat-pill{padding:8px 16px;border-radius:20px;border:1px solid var(--border);background:var(--bg2);color:var(--muted);cursor:pointer;font-size:13px;transition:all .2s;white-space:nowrap}
.cat-pill:hover,.cat-pill.active{background:#1a0000;border-color:var(--red);color:var(--red)}

main{max-width:1200px;margin:0 auto;padding:16px 20px}
.toolbar{display:flex;justify-content:space-between;align-items:center;margin-bottom:12px;flex-wrap:wrap;gap:8px}
.toolbar .count{color:var(--muted);font-size:13px}
.sort-select{padding:8px 12px;background:var(--bg2);border:1px solid var(--border);border-radius:6px;color:var(--text);font-size:13px;outline:none;cursor:pointer}

/* Product group card */
.group-card{background:var(--bg2);border:1px solid var(--border);border-radius:10px;overflow:hidden;transition:all .2s;padding:12px}
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

/* Store rows inside expanded group */
.store-list{display:none;margin-top:12px;padding-top:12px;border-top:1px solid var(--border)}
.group-card.open .store-list{display:block}
.store-row{display:flex;align-items:center;justify-content:space-between;padding:6px 8px;border-radius:6px;transition:background .15s;cursor:pointer;gap:8px}
.store-row:hover{background:var(--bg3)}
.store-row .s-price{color:var(--green);font-weight:600;font-size:14px;white-space:nowrap;min-width:70px}
.store-row .s-store{color:var(--muted);font-size:13px;flex:1;min-width:0}
.store-row .s-status{font-size:11px;padding:2px 8px;border-radius:10px;white-space:nowrap}

.fynd-section{margin-top:32px;border-top:1px solid var(--border);padding-top:20px}
.fynd-section h2{font-size:18px;color:var(--red);margin-bottom:12px;display:flex;align-items:center;gap:8px}
.fynd-section h2 .icon{font-size:22px}

.empty{text-align:center;padding:60px 20px;color:var(--muted)}
.empty .icon{font-size:48px;margin-bottom:12px}
.empty p{font-size:15px}

footer{text-align:center;padding:32px;color:var(--muted);font-size:12px;border-top:1px solid var(--border);margin-top:40px}
footer a{color:var(--muted)}

@media(max-width:600px){
  .header-inner{flex-direction:column;align-items:stretch}
  .logo{text-align:center}
  .group-img{width:70px;height:70px}
}
</style>
</head>
<body>
<header>
<div class=header-inner>
<div class=logo>Pokesniper<span>Scanna, hitta & jämför Pokémon TCG<br><span class=free>HELT GRATIS</span></span></div>
<div class=search-wrap>
<input id=search placeholder="Sök produkt... (t.ex. 151, etb, pitch black, tins)" autofocus>
<button id=clear class=clear-search onclick="clearSearch()">✕</button>
</div>
<div>
<div class=discord-label>Vi finns även i Discord</div>
<a class=discord-badge href="https://discord.gg/QRaPfTVHFr" target=_blank><span class=icon>💬</span> Discord — smartare sök & spårning</a>
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
<option value=price_asc>Pris: lägst först</option>
<option value=price_desc>Pris: högst först</option>
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
Pokesniper.se — Jämför Pokémon TCG-priser hos 45+ svenska butiker · <a href="https://discord.gg/QRaPfTVHFr">Discord</a>
</footer>
<script>
let products=[],activeCat=null,activeSort='relevance',searchQ='';

fetch('/api/products').then(r=>r.json()).then(p=>{
  products=p;
  document.getElementById('stats').textContent=p.length+' produkter · '+new Set(p.map(x=>x.store)).size+' butiker';
  buildCategories();
  doSearch();
  buildFynd();
});

function normalize(t){
  return t.replace(/\s*\(Max\s+\d+\s*(st)?\s*(per\s+(kund|hushåll|person))?\)/gi,'')
          .replace(/\s*\(Max\s+\d+(st)?\s*\/\s*(kund|hushåll)\)/gi,'')
          .replace(/\s*\(Limit\s+\d+\s*per[^)]*\)/gi,'')
          .replace(/\s*\(ENG\)/gi,'').replace(/\s*\(EN\)/gi,'')
          .replace(/\s*\(JP\)/gi,'').replace(/\s*–\s*Förhandsbokning\s*/gi,'')
          .replace(/\s*Förhandsbokning\s*/gi,'').trim();
}

function buildCategories(){
  let cats={};
  products.forEach(p=>{
    let c=catFor(p.title);
    if(!cats[c]) cats[c]=0;
    cats[c]++;
  });
  let order=['ETB','Booster Box','Booster Bundle','Tin','Booster','Box Set','Övrigt'];
  let html=order.filter(c=>cats[c]).map(c=>
    `<button class="cat-pill" data-cat="${c}" onclick="toggleCat('${c}',this)">${c} <span style="opacity:.5;font-size:11px">${cats[c]}</span></button>`
  ).join('');
  html='<button class="cat-pill active" onclick="toggleCat(null,this)">Alla</button>'+html;
  document.getElementById('categories').innerHTML=html;
}

function catFor(t){
  t=' '+t.toLowerCase()+' ';
  if(t.includes('elite trainer box')||t.includes(' etb ')||t.includes(' etbs '))return'ETB';
  if(t.includes('booster box')||t.includes('booster display'))return'Booster Box';
  if(t.includes('booster bundle'))return'Booster Bundle';
  if(t.includes(' tin ')||t.includes(' tins '))return'Tin';
  if(t.includes('booster'))return'Booster';
  if(t.includes('box')||t.includes('collection')||t.includes('premium'))return'Box Set';
  return'Övrigt';
}

function toggleCat(cat,el){
  activeCat=cat===activeCat?null:cat;
  document.querySelectorAll('.cat-pill').forEach(b=>b.classList.remove('active'));
  if(activeCat) el.classList.add('active');
  else document.querySelector('.cat-pill').classList.add('active');
  doSearch();
}

let tmr;
document.getElementById('search').addEventListener('input',function(){
  clearTimeout(tmr);
  document.getElementById('clear').classList.toggle('visible',this.value.length>0);
  tmr=setTimeout(doSearch,200);
});

function clearSearch(){
  document.getElementById('search').value='';
  document.getElementById('clear').classList.remove('visible');
  doSearch();
}

function doSearch(){
  searchQ=document.getElementById('search').value.trim();
  activeSort=document.getElementById('sort').value;
  let filtered=products;
  if(searchQ){
    let words=searchQ.toLowerCase().split(/\\s+/).filter(w=>!['pokemon','tcg','pokémon','the','a','an','max','per','sv','-'].includes(w));
    if(words.includes('etb')){words=words.filter(w=>w!=='etb');words.push('elite','trainer','box');}
    filtered=filtered.filter(p=>{
      let t=p.title.toLowerCase();
      let m=words.filter(w=>w.length>0&&t.includes(w)).length;
      let need=words.length<=2?1:Math.max(1,words.length-1);
      return m>=need;
    });
  }
  if(activeCat) filtered=filtered.filter(p=>catFor(p.title)===activeCat);
  filtered=filtered.filter(p=>isGoodUrl(p.url||''));

  // Group by normalized title
  let groups={};
  filtered.forEach(p=>{
    let key=normalize(p.title);
    if(!groups[key]) groups[key]={title:p.title,image:p.image,items:[]};
    groups[key].items.push(p);
    if(!groups[key].image && p.image) groups[key].image=p.image;
  });

  let groupList=Object.values(groups);
  // Sort groups by cheapest
  groupList.forEach(g=>{
    g.cheapest=Math.min(...g.items.map(p=>parseInt(p.price)||999999));
    g.inStock=g.items.filter(p=>p.status===`✅`).length;
    g.items.sort((a,b)=>(parseInt(a.price)||999999)-(parseInt(b.price)||999999));
  });

  if(activeSort==='price_asc') groupList.sort((a,b)=>a.cheapest-b.cheapest);
  else if(activeSort==='price_desc') groupList.sort((a,b)=>b.cheapest-a.cheapest);
  else if(searchQ) groupList.sort((a,b)=>b.inStock-a.inStock||a.cheapest-b.cheapest);

  document.getElementById('count').textContent=groupList.length+' produkter';
  document.getElementById('empty').style.display=groupList.length?'none':'block';
  document.getElementById('fynd-section').style.display=searchQ||activeCat?'none':'block';
  renderGroups(groupList.slice(0,80));
}

function renderGroups(groups){
  let html=groups.map(g=>{
    let img=g.image?`<img src="${g.image}" alt="" loading=lazy onerror="this.style.display='none';this.nextElementSibling.style.display='block'"><span class=no-img style=display:none>📦</span>`:'<span class=no-img>📦</span>';
    let price=g.cheapest<999999?g.cheapest+' kr':'—';
    let storeRows=g.items.map(p=>{
      let sc=p.status===`✅`?'status-in':'status-out';
      let st=p.status===`✅`?'I lager':'Slut';
      let pr=p.price||'—';
      return`<div class=store-row onclick="event.stopPropagation();window.open('${p.url}','_blank')">
<span class=s-price>${pr}</span><span class=s-store>${p.store}</span>
<span class="card-status ${sc}">${st}</span></div>`;
    }).join('');
    return`<div class=group-card onclick="this.classList.toggle('open')">
<div class=group-header>
<div class=group-img>${img}</div>
<div class=group-info>
<div class=group-title>${g.title}</div>
<div class=group-meta>
<span class=group-price>Från ${price}</span>
<span class=group-stores>${g.items.length} butiker</span>
<span class=group-arrow>▼</span>
</div>
</div>
</div>
<div class=store-list>${storeRows}</div>
</div>`;
  }).join('');
  document.getElementById('grid').innerHTML=html;
}

function isGoodUrl(url){
  let bad=['/collections/','/categories/'];
  if(bad.some(b=>url.includes(b))) return false;
  try{
    let path=new URL(url).pathname.replace(/\\/$/,'').split('/').filter(Boolean);
    let badEnds=['booster-box','booster-packs','tins','etb','booster-bundle','pokemon-boxar','pokemon-elite-trainer-box','pokemon-tins','booster','elite-trainer-box'];
    if(path.length<=2 && badEnds.includes(path[path.length-1].toLowerCase())) return false;
  }catch(e){}
  return true;
}

function buildFynd(){
  let instock=products.filter(p=>p.status===`✅`&&isGoodUrl(p.url||''));
  let groups={};
  instock.forEach(p=>{
    let key=normalize(p.title);
    if(!groups[key]) groups[key]={title:p.title,image:p.image,items:[]};
    groups[key].items.push(p);
    if(!groups[key].image && p.image) groups[key].image=p.image;
  });
  let groupList=Object.values(groups);
  groupList.forEach(g=>{
    g.cheapest=Math.min(...g.items.map(p=>parseInt(p.price)||999999));
    g.items.sort((a,b)=>(parseInt(a.price)||999999)-(parseInt(b.price)||999999));
  });
  groupList.sort((a,b)=>a.cheapest-b.cheapest);
  renderGroups(groupList.slice(0,12));
  document.getElementById('fynd-grid').innerHTML=document.getElementById('grid').innerHTML;
  setTimeout(buildFynd,0); // reset grid
}
// Re-run buildFynd properly
setTimeout(()=>{buildFynd();},500);
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

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
