# -*- coding: utf-8 -*-
"""Pokesniper.se — Pokemon TCG chatbot."""
from flask import Flask, request, jsonify
import json, os

app = Flask(__name__)

# Load products
PRODUCTS_FILE = os.path.join(os.path.dirname(__file__), "products.json")
if os.path.exists(PRODUCTS_FILE):
    with open(PRODUCTS_FILE, encoding="utf-8") as f:
        PRODUCTS = json.load(f)
else:
    PRODUCTS = []

HTML = """<!DOCTYPE html>
<html lang="sv">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Pokesniper.se - Pokemon TCG</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;background:#0d0d0d;color:#e0e0e0;height:100vh;display:flex;flex-direction:column}
.header{background:linear-gradient(180deg,#1a0000,#0d0d0d);padding:24px 20px;text-align:center;border-bottom:1px solid #2a0000}
.header h1{font-size:22px;color:#cc0000;font-weight:700;letter-spacing:2px;text-transform:uppercase}
.header p{font-size:13px;color:#993333;margin-top:4px;letter-spacing:1px}
#count{font-size:11px;color:#662222;margin-top:2px}
#chat{flex:1;overflow-y:auto;padding:16px 20px;display:flex;flex-direction:column;gap:8px}
.msg{max-width:75%;padding:10px 14px;border-radius:6px;line-height:1.5;font-size:13px;border:1px solid #1a1a1a}
.user{background:#1a0000;align-self:flex-end;border-color:#2a0000}
.bot{background:#111;align-self:flex-start;border-color:#1a1a1a}
.bot .p{padding:6px 0;border-bottom:1px solid #181818}
.bot .p:last-child{border:none}
.name{font-weight:600;color:#ff3333}
.price{color:#4ade80;font-weight:500}
.store{color:#777;font-size:11px}
.link a{color:#cc0000;font-size:12px;text-decoration:none}
.link a:hover{color:#ff3333;text-decoration:underline}
.input{background:#0a0a0a;padding:16px 20px;display:flex;gap:8px;border-top:1px solid #1a1a1a}
.input input{flex:1;padding:10px 14px;border:1px solid #222;border-radius:4px;background:#0d0d0d;color:#e0e0e0;font-size:14px;outline:none;transition:border-color .2s}
.input input:focus{border-color:#cc0000}
.input button{padding:10px 20px;border:none;border-radius:4px;background:#cc0000;color:#fff;font-size:13px;cursor:pointer;font-weight:600;letter-spacing:1px;transition:all .2s}
.input button:hover{background:#ff0000}
.typing{color:#662222;font-style:italic;padding:6px 0;font-size:12px}
hr{border:none;border-top:1px solid #181818;margin:4px 0}
</style>
</head>
<body>
<div class=header>
<h1>Pokesniper.se</h1>
<p>Skriv en produkt for att kolla lagret</p>
<div id=count></div>
</div>
<div id=chat>
<div class="msg bot"><b>Välkommen till Pokesniper.se! 🏹</b><br><br>
<i>Sveriges smartaste sökverktyg för Pokémon TCG-lager</i><br><br>
<div style="background:#1a0000;border:1px solid #cc0000;border-radius:6px;padding:12px;margin:8px 0">
<b style="font-size:15px;color:#ff4444">🔍 Sök på vad som helst</b><br>
<span style="font-size:14px;color:#ff9999">
Prova: <b>151, etb, tin, prismatic, mewtwo, pitch black, booster bundle, team rocket, stellar crown, ascended heroes, mega evolution</b> — eller skriv valfri produkt!
</span>
</div>
<b>🛒 43 butiker — 2 670 produkter</b><br>
Vi söker igenom ALLA svenska butiker samtidigt:<br>
Alphaspel • Webhallen • MaxGaming • Coolcard • Swepoke • DragonsLair<br>
Spelochsant • Poketalk • Cardlevels • Kortarkivet • TCG Center • och 30+ fler!<br><br>
<hr><br>
<b>🎮 Discord-servern</b><br>
På vår Discord har vi <b>ännu kraftfullare sökmotorer</b> — bottarna kan mycket mer än hemsidan! 🚀<br><br>
Vi uppdaterar och finslipar bottarna hela tiden 🔧<br>
• Smartare sökningar — bättre matchning, fler resultat<br>
• Fler butiker läggs till löpande<br>
• Nya funktioner som prissänkningslarm och release-kalender<br>
• Botarna blir bara bättre och bättre — allt för att du ska ha bästa kollen! 🔥<br><br>
<b>🤖 Jessie</b> — postar automatiskt i butikskanaler när nya produkter dyker upp. Varje butik har en egen kanal med 🟢/🔴 status<br><br>
<b>🤖 Meowth</b> — din personliga assistent via DM!<br>
• <b>!search</b> — sök i alla butiker med smart matchning<br>
• <b>!track</b> — få DM direkt när en produkt kommer i lager<br>
• <b>!prisvarn</b> — få notis när priset sjunker<br>
• <b>!card / !set</b> — sök Pokémon-kort via TCGdex<br>
• <b>!prisjakt</b> — bästa priset just nu<br><br>
<b>🤖 James</b> — 24h live-feed med statusändringar<br>
<b>🤖 Giovanni</b> — utländska butiker (DK, DE, PL, US)<br>
<b>🤖 Cipher</b> — personlig spårning, upp till 5 trackers<br><br>
<b>📊 Uppdateras var 15:e minut</b> — du missar aldrig ett släpp!<br><br>
<hr><br>
<b>💬 Redo att gå med?</b><br>
👉 <b><a href="https://discord.gg/QRaPfTVHFr" target="_blank" style="color:#60a5fa">discord.gg/QRaPfTVHFr</a></b><br>
Välkommen in i <b>Team Rocket</b>! 🚀 Vi ses på servern — gotta catch 'em all! 🔥<br><br>
<i style="color:#666">Tips: skriv 1-2 ord för snabbast sökning! 👊</i></div>
</div>
<div class=input><input id=q placeholder="Sok produkt..." autofocus><button onclick=sok()>Sok</button></div>
<script>
var i=document.getElementById('q'),c=document.getElementById('chat');
i.addEventListener('keydown',function(e){if(e.key=='Enter')sok()});

// Hamta produktantal
fetch('/count').then(function(r){return r.text()}).then(function(n){document.getElementById('count').textContent='Just nu: '+n+' produkter i databasen'});

function add(t,u){var d=document.createElement('div');d.className='msg '+(u?'user':'bot');d.innerHTML=t;c.appendChild(d);c.scrollTop=c.scrollHeight}
async function sok(){
var q=i.value.trim();if(!q)return;
add(q,1);i.value='';
var t=document.createElement('div');t.className='typing';t.textContent='Letar...';c.appendChild(t);
try{
var r=await fetch('/sok?q='+encodeURIComponent(q)),p=await r.json();
t.remove();
if(!p.length){add('Hittade inget. Forsok: etb, 151, tin, pitch, mewtwo',0);return}
var h='',inne=p.filter(function(x){return x.status=='\u2705'}),ute=p.filter(function(x){return x.status!='\u2705'});
if(inne.length){h+='<b>I LAGER ('+inne.length+'):</b><br>';inne.forEach(function(x){h+='<div class=p><div class=name>'+x.title+'</div><div class=price>'+x.price+'</div><div class=store>'+x.store+'</div><div class=link><a href='+x.url+' target=_blank>Handla har</a></div></div>'})}
if(ute.length){h+='<br><b>SLUT ('+ute.length+'):</b><br>';ute.forEach(function(x){h+='<div class=p><div style=color:#888>'+x.title+'</div><div class=store>'+x.store+'</div></div>'})}
add(h,0);
}catch(e){t.remove();add('Naget gick fel',0)}
}
</script>
</body>
</html>"""

STOP = {"pokemon","tcg","pokemon","the","a","an","max","per","sv","-","box","pack","booster","sv8","sv9","sv10","sv11","sv2a","sv4a","sv7a","sv8a","me05","me04","me03","me02","me25","m1l","m1s","sv9a"}

def search_products(search):
    q = search.lower().strip()
    words = [w for w in q.split() if w not in STOP]
    
    # ETB mapping
    if "etb" in words or "etbs" in words:
        q = q.replace("etb","elite trainer box").replace("etbs","elite trainer box")
    if "sv8a" in q or "terastal" in q.lower():
        q += " " + "terastal festival"
    
    words = [w for w in q.split() if w not in STOP]
    if not words:
        return []
    
    results = []
    seen = set()
    for p in PRODUCTS:
        title = p["title"].lower()
        matched = sum(1 for w in words if w in title)
        # Only require 1 word to match for short queries, N-1 for longer
        needed = 1 if len(words) <= 2 else max(1, len(words) - 1)
        if matched >= needed:
            key = p["title"] + p["store"]
            if key not in seen:
                seen.add(key)
                results.append((matched, p))
    
    results.sort(key=lambda x: (-x[0], 0 if x[1]["status"] == "✅" else 1))
    return [r[1] for r in results[:30]]

@app.route("/")
def index():
    return HTML

@app.route("/sok")
def sok():
    q = request.args.get("q","").strip()
    return jsonify(search_products(q) if q else [])

@app.route("/count")
def count():
    return str(len(PRODUCTS))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
