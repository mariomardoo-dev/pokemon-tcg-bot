"""Pack simulator HTML page for pokesniper.se."""
PACKS_HTML = r"""<!DOCTYPE html>
<html lang="sv">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Pack Simulator — Pokesniper.se</title>
<style>
:root{
  --bg:#0a0a0a;--bg2:#111;--bg3:#1a1a1a;
  --red:#cc0000;--red2:#ff2222;--green:#22c55e;
  --text:#e0e0e0;--muted:#888;--border:#222;
  --gold:#f59e0b;--purple:#a855f7;--pink:#ec4899;
  --blue:#3b82f6;--cyan:#06b6d4;--magenta:#d946ef;
}
*{margin:0;padding:0;box-sizing:border-box}
body{
  font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;
  background:var(--bg);color:var(--text);min-height:100vh;
  overflow-x:hidden;
}
/* ===== HEADER ===== */
header{
  background:linear-gradient(180deg,#150000,var(--bg));
  border-bottom:1px solid var(--border);padding:16px 20px;
  position:sticky;top:0;z-index:100;
}
.header-inner{
  max-width:1000px;margin:0 auto;display:flex;
  align-items:center;justify-content:space-between;flex-wrap:wrap;gap:12px;
}
.logo{font-size:20px;font-weight:800;color:var(--red);letter-spacing:2px;text-transform:uppercase}
.logo a{color:var(--red);text-decoration:none}
.logo span{color:var(--muted);font-size:12px;display:block;letter-spacing:0;font-weight:400;text-transform:none}
.back-link{color:var(--muted);font-size:13px;text-decoration:none;transition:color .2s}
.back-link:hover{color:var(--text)}

/* ===== SET SELECTOR ===== */
.set-selector{
  max-width:1000px;margin:24px auto 0;padding:0 20px;
  display:flex;gap:10px;flex-wrap:wrap;justify-content:center;
}
.set-btn{
  padding:10px 20px;border-radius:24px;border:1px solid var(--border);
  background:var(--bg2);color:var(--muted);cursor:pointer;
  font-size:14px;transition:all .2s;white-space:nowrap;
}
.set-btn:hover{border-color:var(--red);color:var(--text)}
.set-btn.active{
  background:#1a0000;border-color:var(--red);color:var(--red);
  box-shadow:0 0 20px rgba(204,0,0,.15);
}

/* ===== MAIN AREA ===== */
main{max-width:1000px;margin:0 auto;padding:16px 20px 40px}

/* ===== PACK AREA ===== */
.pack-area{
  display:flex;flex-direction:column;align-items:center;
  padding:40px 20px;min-height:300px;
}
.pack-stats{
  color:var(--muted);font-size:13px;margin-bottom:20px;
  text-align:center;
}
.pack-stats b{color:var(--text)}

/* ===== OPEN BUTTON ===== */
.open-btn{
  padding:20px 60px;font-size:22px;font-weight:800;
  background:linear-gradient(135deg,var(--red),#990000);
  color:#fff;border:none;border-radius:16px;
  cursor:pointer;text-transform:uppercase;letter-spacing:3px;
  transition:all .3s;position:relative;overflow:hidden;
  box-shadow:0 4px 30px rgba(204,0,0,.3);
}
.open-btn:hover{
  transform:translateY(-2px);
  box-shadow:0 8px 40px rgba(204,0,0,.5);
}
.open-btn:active{transform:scale(.96)}
.open-btn:disabled{
  opacity:.5;cursor:not-allowed;transform:none;
  box-shadow:0 2px 10px rgba(204,0,0,.1);
}
.open-btn .icon{font-size:28px;margin-right:4px}

/* ===== CARD REVEAL ===== */
.card-reveal{
  display:flex;flex-wrap:wrap;justify-content:center;
  gap:12px;margin-top:24px;perspective:1200px;
}
.card{
  width:140px;border-radius:10px;overflow:hidden;
  background:var(--bg3);border:2px solid var(--border);
  transition:all .4s cubic-bezier(.34,1.56,.64,1);
  opacity:0;transform:translateY(40px) scale(.8);
  cursor:default;
}
.card.revealed{
  opacity:1;transform:translateY(0) scale(1);
}
.card:hover{
  transform:translateY(-6px) scale(1.05);
  z-index:10;
}
.card-img{
  width:100%;height:190px;display:flex;align-items:center;
  justify-content:center;background:var(--bg2);
  overflow:hidden;position:relative;
}
.card-img img{
  width:100%;height:100%;object-fit:contain;
  transition:transform .3s;
}
.card:hover .card-img img{transform:scale(1.08)}
.card-info{padding:8px 10px}
.card-name{
  font-size:11px;font-weight:600;line-height:1.3;
  white-space:nowrap;overflow:hidden;text-overflow:ellipsis;
}
.card-rarity{
  font-size:10px;margin-top:4px;font-weight:600;
  padding:2px 8px;border-radius:10px;display:inline-block;
}

/* ===== RARITY COLORS ===== */
.rarity-Common{color:#aaa;border-color:#555}
.rarity-Uncommon{color:#22c55e;border-color:#166534}
.rarity-Rare{color:#3b82f6;border-color:#1e40af}
.rarity-Double{color:#eab308;border-color:#a16207}
.rarity-Illustration{color:#f59e0b;border-color:#b45309}
.rarity-Ultra{color:#a855f7;border-color:#7e22ce}
.rarity-Special{color:#ec4899;border-color:#be185d}
.rarity-Hyper{color:#fbbf24;border-color:#b45309}
.rarity-ACE{color:#d946ef;border-color:#a21caf}
.rarity-Shiny{color:#06b6d4;border-color:#0e7490}

.rarity-badge-Common{background:rgba(170,170,170,.15);color:#aaa}
.rarity-badge-Uncommon{background:rgba(34,197,94,.15);color:#22c55e}
.rarity-badge-Rare{background:rgba(59,130,246,.15);color:#3b82f6}
.rarity-badge-Double{background:rgba(234,179,8,.15);color:#eab308}
.rarity-badge-Illustration{background:rgba(245,158,11,.15);color:#f59e0b}
.rarity-badge-Ultra{background:rgba(168,85,247,.15);color:#a855f7}
.rarity-badge-Special{background:rgba(236,72,153,.15);color:#ec4899}
.rarity-badge-Hyper{background:rgba(251,191,36,.15);color:#fbbf24}
.rarity-badge-ACE{background:rgba(217,70,239,.15);color:#d946ef}
.rarity-badge-Shiny{background:rgba(6,182,212,.15);color:#06b6d4}

/* ===== PULL SUMMARY ===== */
.pull-summary{
  text-align:center;margin-top:24px;padding:16px;
  background:var(--bg2);border:1px solid var(--border);
  border-radius:12px;display:none;
}
.pull-summary h3{
  font-size:15px;color:var(--red);margin-bottom:10px;
}
.pull-summary .pulls{
  display:flex;gap:16px;justify-content:center;flex-wrap:wrap;
}
.pull-item{text-align:center}
.pull-item .count{font-size:24px;font-weight:800}
.pull-item .label{font-size:10px;color:var(--muted);text-transform:uppercase}

/* ===== FOOTER ===== */
footer{
  text-align:center;padding:24px;color:var(--muted);
  font-size:12px;border-top:1px solid var(--border);
}

/* ===== ANIMATIONS ===== */
@keyframes shimmer{
  0%{background-position:-200% center}
  100%{background-position:200% center}
}
.card.holo-effect{
  position:relative;
}
.card.holo-effect::after{
  content:'';position:absolute;inset:0;
  background:linear-gradient(105deg,
    transparent 40%,rgba(255,255,255,.08) 45%,
    rgba(255,255,255,.15) 50%,rgba(255,255,255,.08) 55%,
    transparent 60%);
  background-size:200% 100%;
  animation:shimmer 3s infinite;
  pointer-events:none;border-radius:10px;
}

/* ===== LOADING ===== */
.loading{
  text-align:center;padding:60px;color:var(--muted);
}
.loading .spinner{
  width:40px;height:40px;border:3px solid var(--border);
  border-top-color:var(--red);border-radius:50%;
  animation:spin .8s linear infinite;margin:0 auto 16px;
}
@keyframes spin{to{transform:rotate(360deg)}}

/* ===== MOBILE ===== */
@media(max-width:600px){
  .card{width:100px}
  .card-img{height:140px}
  .open-btn{padding:16px 40px;font-size:18px}
  .set-selector{gap:6px}
  .set-btn{padding:8px 14px;font-size:12px}
}

/* ===== REVERSE HOLO SHINE ===== */
.card.reverse-holo .card-img{
  background:linear-gradient(135deg,#1a1a2e,#16213e,#1a1a2e);
}
.card.reverse-holo .card-name::after{
  content:' ⭐';font-size:10px;
}
</style>
</head>
<body>

<header>
<div class=header-inner>
<div class=logo><a href="/">Pokesniper</a><span>Pack Simulator</span></div>
<a href="/" class=back-link>&larr; Tillbaka till prisjakt</a>
</div>
</header>

<div class=set-selector id=setSelector></div>

<main>
<div class=pack-area id=packArea>
  <div class=loading id=loading>
    <div class=spinner></div>
    <p>Laddar set...</p>
  </div>
</div>
</main>

<footer>Pokesniper.se &mdash; Pack Simulator</footer>

<script>
// ===== STATE =====
var sets={}, activeSet=null, totalOpened=0, bestPulls={};

// ===== RARITY MAPPING =====
var RARITY_CLASS={
  'Common':'Common','Uncommon':'Uncommon','Rare':'Rare',
  'Double Rare':'Double','Illustration Rare':'Illustration',
  'Ultra Rare':'Ultra','Special Illustration Rare':'Special',
  'Hyper Rare':'Hyper','ACE SPEC Rare':'ACE',
  'Shiny Rare':'Shiny','Shiny Ultra Rare':'Shiny'
};
var RARITY_WEIGHT={
  'Common':0,'Uncommon':1,'Rare':2,'Double Rare':3,
  'Illustration Rare':4,'Ultra Rare':5,
  'Special Illustration Rare':6,'Hyper Rare':7,
  'ACE SPEC Rare':8,'Shiny Rare':4,'Shiny Ultra Rare':5
};

// ===== RARE SLOT ODDS (realistic SV-era pull rates) =====
// Based on community data from 1000s of pack openings
var RARE_SLOT_POOL=[
  {rarity:'Double Rare',weight:67},             // ~67% — guaranteed holo or better in rare slot
  {rarity:'Illustration Rare',weight:12},       // ~12% — 1 in 8 packs
  {rarity:'Ultra Rare',weight:9},               // ~9% — 1 in 11 packs
  {rarity:'Special Illustration Rare',weight:4}, // ~4% — 1 in 25 packs
  {rarity:'Hyper Rare',weight:2},               // ~2% — 1 in 50 packs
];

// ===== LOAD SETS =====
async function loadSets(){
  var setFiles=['151','surging-sparks','prismatic-evolutions','paldean-fates','twilight-masquerade'];
  var loaded=0;
  
  for(var i=0;i<setFiles.length;i++){
    try{
      var resp=await fetch('/static/sets/'+setFiles[i]+'.json');
      var data=await resp.json();
      sets[data.name]=data;
      loaded++;
    }catch(e){
      console.warn('Failed to load',setFiles[i],e);
    }
  }
  
  if(loaded===0){
    document.getElementById('packArea').innerHTML='<div class=loading><p style=color:var(--red)>Kunde inte ladda set-data. Försök igen senare.</p></div>';
    return;
  }
  
  buildSetSelector();
  activeSet=Object.keys(sets)[0];
  showPackUI();
}

// ===== BUILD SET SELECTOR =====
function buildSetSelector(){
  var html='';
  var first=true;
  for(var key in sets){
    html+='<button class="set-btn'+(first?' active':'')+'" onclick="selectSet(\''+key+'\',this)">'+sets[key].displayName+'</button>';
    first=false;
  }
  document.getElementById('setSelector').innerHTML=html;
}

function selectSet(key,btn){
  activeSet=key;
  document.querySelectorAll('.set-btn').forEach(function(b){b.classList.remove('active')});
  btn.classList.add('active');
  document.getElementById('cardReveal').innerHTML='';
  document.getElementById('pullSummary').style.display='none';
}

// ===== SHOW PACK UI =====
function showPackUI(){
  var set=sets[activeSet];
  document.getElementById('loading').style.display='none';
  document.getElementById('packArea').innerHTML=
    '<div class=pack-stats id=packStats>'+
      '<b>'+set.displayName+'</b> &middot; '+set.cards.length+' kort &middot; '+
      '<span id=packCount>0</span> packs öppnade'+
    '</div>'+
    '<button class=open-btn id=openBtn onclick=openPack()>'+
      '<span class=icon>&#128230;</span> Riv upp!'+
    '</button>'+
    '<div class=card-reveal id=cardReveal></div>'+
    '<div class=pull-summary id=pullSummary>'+
      '<h3>Dragna kort</h3>'+
      '<div class=pulls id=pullList></div>'+
    '</div>';
}

// ===== OPEN PACK =====
var isOpening=false;

async function openPack(){
  if(isOpening)return;
  isOpening=true;
  
  var btn=document.getElementById('openBtn');
  btn.disabled=true;
  btn.innerHTML='<span class=icon>&#9889;</span> River upp...';
  
  var reveal=document.getElementById('cardReveal');
  reveal.innerHTML='';
  document.getElementById('pullSummary').style.display='none';
  
  var set=sets[activeSet];
  
  // Group cards by rarity
  var byRarity={};
  set.cards.forEach(function(c){
    var r=c.rarity||'Common';
    if(!byRarity[r])byRarity[r]=[];
    byRarity[r].push(c);
  });
  
  // Generate pack
  var pack=[];
  
  // 5 Commons
  pack=pack.concat(pickRandom(byRarity['Common']||[],5));
  
  // 3 Uncommons
  pack=pack.concat(pickRandom(byRarity['Uncommon']||[],3));
  
  // 1 Rare slot (weighted)
  var rareSlotRarities=getAvailableRareSlots(byRarity);
  var rareRarity=pickWeighted(rareSlotRarities);
  var rareCards=byRarity[rareRarity]||byRarity['Rare']||[];
  pack=pack.concat(pickRandom(rareCards,1));
  
  // 1 Reverse Holo (any card, any rarity - but we mark it)
  var allCards=set.cards;
  var revHolo=pickRandom(allCards,1)[0];
  revHolo._reverseHolo=true;
  pack.push(revHolo);
  
  // Shuffle reveal order (reverse holo last)
  shuffle(pack);
  // Move reverse holo to last
  var rhIdx=-1;
  for(var i=0;i<pack.length;i++){if(pack[i]._reverseHolo){rhIdx=i;break}}
  if(rhIdx>=0){
    var rh=pack.splice(rhIdx,1)[0];
    pack.push(rh);
  }
  
  // Animate reveal
  totalOpened++;
  document.getElementById('packCount').textContent=totalOpened;
  
  for(var i=0;i<pack.length;i++){
    await sleep(i===0?300:180);
    revealCard(pack[i],reveal,i);
  }
  
  // Show summary after a short delay
  await sleep(600);
  showPullSummary(pack);
  
  btn.disabled=false;
  btn.innerHTML='<span class=icon>&#128230;</span> Riv upp igen!';
  isOpening=false;
}

function getAvailableRareSlots(byRarity){
  // Build weighted list based on what the set actually has
  var available=[];
  for(var j=0;j<RARE_SLOT_POOL.length;j++){
    var entry=RARE_SLOT_POOL[j];
    if(byRarity[entry.rarity] && byRarity[entry.rarity].length>0){
      available.push({rarity:entry.rarity,weight:entry.weight});
    }
  }
  // Also check for ACE SPEC and Shiny variants
  if(byRarity['ACE SPEC Rare'] && byRarity['ACE SPEC Rare'].length>0){
    available.push({rarity:'ACE SPEC Rare',weight:2});
  }
  if(byRarity['Shiny Ultra Rare'] && byRarity['Shiny Ultra Rare'].length>0){
    available.push({rarity:'Shiny Ultra Rare',weight:5});
  }
  if(byRarity['Shiny Rare'] && byRarity['Shiny Rare'].length>0 && !available.find(function(a){return a.rarity==='Shiny Rare'})){
    available.push({rarity:'Shiny Rare',weight:8});
  }
  return available;
}

function pickWeighted(items){
  var total=0;
  items.forEach(function(item){total+=item.weight});
  var rand=Math.random()*total;
  var cumulative=0;
  for(var i=0;i<items.length;i++){
    cumulative+=items[i].weight;
    if(rand<=cumulative)return items[i].rarity;
  }
  return items[items.length-1].rarity;
}

function pickRandom(arr,count){
  var shuffled=arr.slice();
  shuffle(shuffled);
  return shuffled.slice(0,Math.min(count,arr.length));
}

function shuffle(arr){
  for(var i=arr.length-1;i>0;i--){
    var j=Math.floor(Math.random()*(i+1));
    var tmp=arr[i];arr[i]=arr[j];arr[j]=tmp;
  }
}

function sleep(ms){return new Promise(function(r){setTimeout(r,ms)})}

// ===== REVEAL CARD =====
function revealCard(card,container,index){
  var rc=RARITY_CLASS[card.rarity]||'Common';
  var isHolo=rc==='Double'||rc==='Illustration'||rc==='Ultra'||rc==='Special'||rc==='Hyper'||rc==='Shiny';
  var rhClass=card._reverseHolo?' reverse-holo':'';
  var holoClass=isHolo?' holo-effect':'';
  
  var div=document.createElement('div');
  div.className='card rarity-'+rc+rhClass+holoClass;
  div.style.transitionDelay=(index*0.05)+'s';
  div.innerHTML=
    '<div class=card-img>'+
      '<img src="'+card.image+'" alt="'+card.name+'" loading=lazy onerror="this.src=\'data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 140%22><rect fill=%22%23111%22 width=%22100%22 height=%22140%22/><text fill=%22%23555%22 x=%2250%22 y=%2270%22 text-anchor=%22middle%22 font-size=%2212%22>'+encodeURIComponent(card.name.substring(0,15))+'</text></svg>\'">'+
    '</div>'+
    '<div class=card-info>'+
      '<div class=card-name>'+(card._reverseHolo?'&#11088; ':'')+card.name+'</div>'+
      '<div class="card-rarity rarity-badge-'+rc+'">'+card.rarity+(card._reverseHolo?' Reverse Holo':'')+'</div>'+
    '</div>';
  
  container.appendChild(div);
  
  // Trigger animation
  requestAnimationFrame(function(){
    requestAnimationFrame(function(){
      div.classList.add('revealed');
    });
  });
}

// ===== PULL SUMMARY =====
function showPullSummary(pack){
  var counts={};
  pack.forEach(function(c){
    counts[c.rarity]=counts[c.rarity]||[];
    counts[c.rarity].push(c);
  });
  
  var rarityOrder=['Common','Uncommon','Rare','Double Rare','Illustration Rare','Ultra Rare',
    'Special Illustration Rare','Hyper Rare','ACE SPEC Rare','Shiny Rare','Shiny Ultra Rare'];
  
  // Track best pulls
  pack.forEach(function(c){
    var w=RARITY_WEIGHT[c.rarity]||0;
    var bestW=RARITY_WEIGHT[bestPulls[activeSet+'_best']]||0;
    if(w>bestW){
      bestPulls[activeSet+'_best']=c.rarity;
      bestPulls[activeSet+'_bestCard']=c.name;
    }
  });
  
  var html='';
  rarityOrder.forEach(function(r){
    if(counts[r]){
      var rc=RARITY_CLASS[r]||'Common';
      html+='<div class=pull-item><div class="count rarity-badge-'+rc+'">'+counts[r].length+'</div><div class=label>'+r+'</div></div>';
    }
  });
  
  var summ=document.getElementById('pullSummary');
  document.getElementById('pullList').innerHTML=html;
  summ.style.display='block';
  
  // Update stats
  var bestRarity=bestPulls[activeSet+'_best']||'';
  var bestCard=bestPulls[activeSet+'_bestCard']||'';
  document.getElementById('packStats').innerHTML=
    '<b>'+sets[activeSet].displayName+'</b> &middot; '+sets[activeSet].cards.length+' kort &middot; '+
    '<span id=packCount>'+totalOpened+'</span> packs öppnade'+
    (bestRarity?'<br>Bästa drag: <span style=color:var(--gold)>'+bestCard+'</span> ('+bestRarity+')':'');
}

// ===== INIT =====
loadSets();
</script>

</body>
</html>"""
