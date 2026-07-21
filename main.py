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
body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;background:#1a1a2e;color:#eee;height:100vh;display:flex;flex-direction:column}
.header{background:#16213e;padding:20px;text-align:center;border-bottom:2px solid #e94560}
.header h1{font-size:24px;color:#e94560}
.header p{font-size:14px;color:#888;margin-top:5px}
#count{font-size:12px;color:#666}
#chat{flex:1;overflow-y:auto;padding:20px;display:flex;flex-direction:column;gap:12px}
.msg{max-width:80%;padding:12px 16px;border-radius:12px;line-height:1.4;font-size:14px}
.user{background:#0f3460;align-self:flex-end;border-bottom-right-radius:4px}
.bot{background:#16213e;align-self:flex-start;border-bottom-left-radius:4px}
.bot .p{padding:8px 0;border-bottom:1px solid #333}
.bot .p:last-child{border:none}
.name{font-weight:600;color:#e94560}
.price{color:#4ade80}
.store{color:#888;font-size:12px}
.link a{color:#60a5fa;font-size:12px}
.input{background:#16213e;padding:15px 20px;display:flex;gap:10px;border-top:1px solid #333}
.input input{flex:1;padding:12px 16px;border:1px solid #333;border-radius:8px;background:#1a1a2e;color:#eee;font-size:15px;outline:none}
.input input:focus{border-color:#e94560}
.input button{padding:12px 24px;border:none;border-radius:8px;background:#e94560;color:#fff;font-size:15px;cursor:pointer}
.input button:hover{background:#d63851}
.typing{color:#666;font-style:italic;padding:8px}
.hint{color:#555;font-size:12px;text-align:center;padding:10px}
</style>
</head>
<body>
<div class=header>
<h1>Pokesniper.se</h1>
<p>Skriv en produkt for att kolla lagret</p>
<div id=count></div>
</div>
<div id=chat>
<div class="msg bot">Hej! Välkommen till <b>Pokesniper.se</b> 🔥<br><br>
<b>🔍 Sök på</b> 151, etb, tin, prismatic, mewtwo, pitch, booster — eller valfri produkt!<br><br>
<b>🛒 43 butiker — 2670 produkter</b><br>
Allt fran svenska butiker pa ett stalle: Alphaspel, Webhallen, MaxGaming, Coolcard, Swepoke, DragonsLair och manga fler!<br><br>
<b>🤖 Discord-bottar</b><br>
Vi har ocksa bottar pa Discord som overvakar lagret i realtid:<br>
• <b>Jessie</b> — postar i butikskanaler nar nya produkter kommer<br>
• <b>Meowth</b> — sok, tracka och fa DM nar nagot kommer i lager<br>
• <b>Giovanni</b> — utlandska butiker<br>
• <b>Cipher</b> — personlig sparning<br>
• <b>James</b> — 24h live-feed med statusandringar<br><br>
<b>💬 Discord:</b> Sag till mig sa fixar jag invite-lank!<br><br>
<i>Tips: skriv 1-2 ord, t.ex. &quot;151&quot; eller &quot;team rocket&quot;</i></div>
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
