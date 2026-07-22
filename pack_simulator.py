"""Pack simulator HTML page for pokesniper.se — immersive loot-box experience."""
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
  --blue:#3b82f6;
}
*{margin:0;padding:0;box-sizing:border-box}
body{
  font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;
  background:var(--bg);color:var(--text);min-height:100vh;
  overflow-x:hidden;transition:background .6s;
}
body.shake{animation:screenShake .5s ease-out}
body.glow-bg{background:radial-gradient(ellipse at center,#1a0000 0%,var(--bg) 70%)!important}

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

.set-selector{
  max-width:1000px;margin:24px auto 0;padding:0 20px;
  display:flex;gap:10px;flex-wrap:wrap;justify-content:center;
}
.set-btn{
  padding:10px 20px;border-radius:24px;border:1px solid var(--border);
  background:var(--bg2);color:var(--muted);cursor:pointer;
  font-size:14px;transition:all .2s;
}
.set-btn:hover{border-color:var(--red);color:var(--text)}
.set-btn.active{
  background:#1a0000;border-color:var(--red);color:var(--red);
  box-shadow:0 0 20px rgba(204,0,0,.15);
}

main{max-width:1000px;margin:0 auto;padding:16px 20px 40px}

/* ===== PACK STAGE ===== */
.pack-stage{
  display:flex;flex-direction:column;align-items:center;
  padding:20px 20px 0;min-height:360px;position:relative;
}
.pack-stats{
  color:var(--muted);font-size:13px;margin-bottom:8px;text-align:center;
}
.pack-stats b{color:var(--text)}

/* ===== BOOSTER PACK ===== */
.pack-wrapper{
  position:relative;width:200px;height:280px;cursor:pointer;
  perspective:800px;margin:20px 0;
}
.pack-wrapper:hover .booster-pack{transform:translateY(-4px)}
.pack-wrapper:active .booster-pack{transform:scale(.96)}

.booster-pack{
  width:100%;height:100%;border-radius:12px;
  background:linear-gradient(180deg,#1a1a2e 0%,#16213e 30%,#0f3460 50%,#16213e 70%,#1a1a2e 100%);
  border:3px solid #2a2a4a;position:relative;overflow:hidden;
  transition:all .3s ease;box-shadow:0 8px 32px rgba(0,0,0,.5);
  display:flex;flex-direction:column;align-items:center;justify-content:center;
}
.booster-pack::before{
  content:'';position:absolute;inset:6px;border:2px solid rgba(255,255,255,.06);
  border-radius:8px;pointer-events:none;
}
.booster-pack .pack-art{
  width:170px;height:80px;border-radius:8px;
  background:linear-gradient(135deg,#0f3460,#1a1a4e);
  display:flex;align-items:center;justify-content:center;
  font-size:40px;margin-bottom:10px;position:relative;z-index:1;
  overflow:hidden;
}
.booster-pack .pack-art img{width:90%;height:90%;object-fit:contain}
.booster-pack .pack-label{
  font-size:18px;font-weight:800;color:#fff;letter-spacing:4px;
  text-transform:uppercase;z-index:1;
}
.booster-pack .pack-sub{
  font-size:10px;color:rgba(255,255,255,.4);letter-spacing:2px;z-index:1;
}

/* Pack glow — applied before rip */
.booster-pack.charging{animation:packPulse .6s ease-in-out 3}
.booster-pack.charging::after{
  content:'';position:absolute;inset:-10px;border-radius:16px;
  animation:glowPulse .5s ease-in-out 3;
  pointer-events:none;z-index:0;
}
@keyframes packPulse{
  0%,100%{transform:scale(1)}
  50%{transform:scale(1.04)}
}
@keyframes glowPulse{
  0%,100%{box-shadow:0 0 20px var(--glow,var(--red)), inset 0 0 20px var(--glow,var(--red))}
  50%{box-shadow:0 0 50px var(--glow,var(--red)), inset 0 0 40px var(--glow,var(--red))}
}

/* Rip animation — pack splits */
.booster-pack.ripping{
  animation:ripShake .15s ease-in-out 2;
}
@keyframes ripShake{
  0%,100%{transform:rotate(0)}
  25%{transform:rotate(-3deg)}
  75%{transform:rotate(3deg)}
}
.booster-pack.ripped{
  animation:ripApart .5s ease-in forwards;
}
@keyframes ripApart{
  0%{transform:scale(1);opacity:1;filter:blur(0)}
  50%{transform:scale(1.1);opacity:.8;filter:blur(2px)}
  100%{transform:scale(1.4);opacity:0;filter:blur(8px)}
}

/* ===== CARD REVEAL AREA ===== */
.card-stage{
  display:flex;flex-wrap:wrap;justify-content:center;
  gap:10px;margin-top:16px;perspective:1200px;min-height:200px;
}

/* ===== CARDS ===== */
.card{
  width:130px;border-radius:10px;overflow:hidden;
  background:var(--bg3);border:2px solid var(--border);
  cursor:default;position:relative;
  animation:cardEntry .5s cubic-bezier(.34,1.56,.64,1) both;
}
@keyframes cardEntry{
  from{opacity:0;transform:translateY(60px) scale(.5) rotateY(90deg)}
  to{opacity:1;transform:translateY(0) scale(1) rotateY(0)}
}
.card:hover{
  transform:translateY(-8px) scale(1.08);z-index:10;
  box-shadow:0 12px 40px rgba(0,0,0,.4);
}
.card-img{
  width:100%;height:175px;display:flex;align-items:center;
  justify-content:center;background:var(--bg2);overflow:hidden;
}
.card-img img{width:100%;height:100%;object-fit:contain}
.card-info{padding:6px 8px}
.card-name{
  font-size:10px;font-weight:600;line-height:1.3;
  white-space:nowrap;overflow:hidden;text-overflow:ellipsis;
}
.card-rarity{
  font-size:9px;margin-top:3px;font-weight:600;
  padding:1px 7px;border-radius:8px;display:inline-block;
}

/* ===== RARITY COLORS ===== */
.rarity-Common{color:#aaa;border-color:#444}
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

/* Holo shimmer */
@keyframes shimmer{
  0%{background-position:-200% center}
  100%{background-position:200% center}
}
.card.holo::after{
  content:'';position:absolute;inset:0;pointer-events:none;border-radius:10px;
  background:linear-gradient(105deg,transparent 40%,rgba(255,255,255,.06) 45%,rgba(255,255,255,.12) 50%,rgba(255,255,255,.06) 55%,transparent 60%);
  background-size:200% 100%;animation:shimmer 3s infinite;
}

/* Reverse holo */
.card.reverse-holo .card-img{background:linear-gradient(135deg,#1a1a2e,#16213e,#1a1a2e)}

/* Big hit card glow */
.card.big-hit{animation:cardEntry .5s cubic-bezier(.34,1.56,.64,1) both, cardGlow 1.5s ease-in-out infinite}
@keyframes cardGlow{
  0%,100%{box-shadow:0 0 20px var(--hit-glow,rgba(245,158,11,.4))}
  50%{box-shadow:0 0 40px var(--hit-glow,rgba(245,158,11,.7))}
}

/* ===== PARTICLES ===== */
.particle{
  position:fixed;pointer-events:none;z-index:1000;
  font-size:20px;animation:particleFly 1.5s ease-out forwards;
}
@keyframes particleFly{
  0%{opacity:1;transform:translate(0,0) scale(1)}
  100%{opacity:0;transform:translate(var(--px),var(--py)) scale(0)}
}

/* ===== SCREEN SHAKE ===== */
@keyframes screenShake{
  0%,100%{transform:translate(0)}
  10%{transform:translate(-4px,2px)}
  20%{transform:translate(4px,-1px)}
  30%{transform:translate(-3px,-3px)}
  40%{transform:translate(3px,2px)}
  50%{transform:translate(-2px,1px)}
  60%{transform:translate(2px,-2px)}
  70%{transform:translate(-1px,-1px)}
  80%{transform:translate(1px,1px)}
  90%{transform:translate(-1px,2px)}
}

/* ===== OVERLAY FLASH ===== */
.flash-overlay{
  position:fixed;inset:0;pointer-events:none;z-index:999;
  opacity:0;transition:opacity .1s;
}
.flash-overlay.active{opacity:1;transition:opacity 0s}
.flash-overlay.fading{opacity:0;transition:opacity .4s}

/* ===== LOADING ===== */
.loading{text-align:center;padding:60px;color:var(--muted)}
.loading .spinner{
  width:40px;height:40px;border:3px solid var(--border);
  border-top-color:var(--red);border-radius:50%;
  animation:spin .8s linear infinite;margin:0 auto 16px;
}
@keyframes spin{to{transform:rotate(360deg)}}

/* ===== NEXT PACK BUTTON ===== */
.next-pack-btn{
  display:block;margin:16px auto 0;padding:10px 28px;
  font-size:13px;font-weight:600;color:#fff;
  background:linear-gradient(135deg,var(--red),#990000);
  border:none;border-radius:10px;cursor:pointer;
  letter-spacing:1px;text-transform:uppercase;
  box-shadow:0 2px 12px rgba(204,0,0,.25);
  transition:all .25s;animation:fadeIn .3s ease;
}
.next-pack-btn:hover{
  transform:translateY(-1px);
  box-shadow:0 6px 28px rgba(204,0,0,.45);
}
.next-pack-btn:active{transform:scale(.96)}
@keyframes fadeIn{from{opacity:0;transform:translateY(10px)}to{opacity:1;transform:translateY(0)}}

footer{text-align:center;padding:24px;color:var(--muted);font-size:12px;border-top:1px solid var(--border)}

@media(max-width:600px){
  .card{width:95px}.card-img{height:130px}
  .pack-wrapper{width:160px;height:224px}
  .booster-pack .pack-art{width:100px;height:100px;font-size:40px}
  .booster-pack .pack-label{font-size:14px}
}
</style>
</head>
<body>

<div class=flash-overlay id=flashOverlay></div>

<header>
<div class=header-inner>
<div class=logo><a href="/">Pokesniper</a><span>Pack Simulator</span></div>
<a href="/" class=back-link>&larr; Tillbaka till prisjakt</a>
</div>
</header>

<div class=set-selector id=setSelector></div>

<main>
<div class=pack-stage id=packStage>
  <div class=loading id=loading><div class=spinner></div><p>Laddar set...</p></div>
</div>
</main>

<footer>Pokesniper.se &mdash; Pack Simulator</footer>

<script>
// ===== STATE =====
var sets={}, activeSet=null, totalOpened=0, bestPulls={};

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
var GLOW_COLORS={
  'Common':'rgba(170,170,170,.3)','Uncommon':'rgba(34,197,94,.3)',
  'Double Rare':'rgba(234,179,8,.5)','Illustration Rare':'rgba(245,158,11,.6)',
  'Ultra Rare':'rgba(168,85,247,.6)','Special Illustration Rare':'rgba(236,72,153,.7)',
  'Hyper Rare':'rgba(251,191,36,.8)','ACE SPEC Rare':'rgba(217,70,239,.7)',
  'Shiny Rare':'rgba(6,182,212,.6)','Shiny Ultra Rare':'rgba(6,182,212,.8)'
};
var HIT_GLOW={
  'Double Rare':'rgba(234,179,8,.3)','Illustration Rare':'rgba(245,158,11,.4)',
  'Ultra Rare':'rgba(168,85,247,.4)','Special Illustration Rare':'rgba(236,72,153,.5)',
  'Hyper Rare':'rgba(251,191,36,.6)','ACE SPEC Rare':'rgba(217,70,239,.4)',
  'Shiny Rare':'rgba(6,182,212,.4)','Shiny Ultra Rare':'rgba(6,182,212,.5)'
};
var RARE_SLOT_POOL=[
  {rarity:'Double Rare',weight:67},
  {rarity:'Illustration Rare',weight:12},
  {rarity:'Ultra Rare',weight:9},
  {rarity:'Special Illustration Rare',weight:4},
  {rarity:'Hyper Rare',weight:2},
];

// ===== SET LOGOS =====
var SET_LOGOS={
  '151':'https://images.pokemontcg.io/sv3pt5/logo.png',
  'surging-sparks':'https://images.pokemontcg.io/sv8/logo.png',
  'prismatic-evolutions':'https://images.pokemontcg.io/sv8pt5/logo.png',
  'paldean-fates':'https://images.pokemontcg.io/sv4pt5/logo.png',
  'twilight-masquerade':'https://images.pokemontcg.io/sv6/logo.png',
};
var SET_COLORS={
  '151':'#e8c547',
  'surging-sparks':'#ff6b35',
  'prismatic-evolutions':'#c4b5fd',
  'paldean-fates':'#f472b6',
  'twilight-masquerade':'#34d399',
};

// ===== AUDIO (Web Audio API synthesis) =====
var audioCtx=null;
function initAudio(){
  if(audioCtx)return;
  try{audioCtx=new(window.AudioContext||window.webkitAudioContext)()}catch(e){audioCtx=null}
}
function playNoise(dur,freq,type,vol){
  if(!audioCtx)return;
  var o=audioCtx.createOscillator();
  var g=audioCtx.createGain();
  o.type=type||'sawtooth';
  o.frequency.setValueAtTime(freq||200,audioCtx.currentTime);
  o.frequency.exponentialRampToValueAtTime(freq*2||400,audioCtx.currentTime+dur*.3);
  o.frequency.exponentialRampToValueAtTime(50,audioCtx.currentTime+dur);
  g.gain.setValueAtTime(vol||.05,audioCtx.currentTime);
  g.gain.exponentialRampToValueAtTime(.001,audioCtx.currentTime+dur);
  o.connect(g);g.connect(audioCtx.destination);
  o.start();o.stop(audioCtx.currentTime+dur);
}
function sfxRip(){playNoise(.25,100,'sawtooth',.08);setTimeout(function(){playNoise(.15,80,'square',.05)},100)}
function sfxFlip(){playNoise(.08,600,'sine',.03)}
function sfxDing(){playNoise(.3,880,'sine',.06);setTimeout(function(){playNoise(.3,1100,'sine',.04)},150)}
function sfxBigHit(){
  playNoise(.5,1200,'sine',.07);
  setTimeout(function(){playNoise(.4,1600,'sine',.05)},200);
  setTimeout(function(){playNoise(.6,2000,'sine',.04)},350);
}
function sfxSparkle(){playNoise(.1,2000+Math.random()*2000,'sine',.02)}

// ===== PARTICLES =====
function spawnParticles(x,y,count,emoji){
  var emojis=emoji||['✨','⭐','💫','🌟'];
  for(var i=0;i<count;i++){
    var p=document.createElement('div');
    p.className='particle';
    p.textContent=emojis[Math.floor(Math.random()*emojis.length)];
    p.style.left=x+'px';p.style.top=y+'px';
    p.style.setProperty('--px',(Math.random()-.5)*300+'px');
    p.style.setProperty('--py',-(Math.random()*200+100)+'px');
    p.style.animationDelay=Math.random()*.3+'s';
    document.body.appendChild(p);
    setTimeout(function(){p.remove()},1800);
  }
}

// ===== SCREEN FLASH =====
function screenFlash(color){
  var el=document.getElementById('flashOverlay');
  el.style.background=color||'rgba(255,255,255,.15)';
  el.classList.add('active');
  requestAnimationFrame(function(){
    el.classList.remove('active');
    el.classList.add('fading');
    setTimeout(function(){el.classList.remove('fading')},400);
  });
}

// ===== SCREEN SHAKE =====
function screenShake(){
  document.body.classList.add('shake');
  setTimeout(function(){document.body.classList.remove('shake')},500);
}

// ===== LOAD SETS =====
async function loadSets(){
  var setFiles=['151','surging-sparks','prismatic-evolutions','paldean-fates','twilight-masquerade'];
  for(var i=0;i<setFiles.length;i++){
    try{
      var resp=await fetch('/static/sets/'+setFiles[i]+'.json');
      var data=await resp.json();
      sets[data.name]=data;
    }catch(e){console.warn('Failed to load',setFiles[i])}
  }
  if(!Object.keys(sets).length){
    document.getElementById('packStage').innerHTML='<div class=loading><p style=color:var(--red)>Kunde inte ladda data.</p></div>';
    return;
  }
  buildSetSelector();
  activeSet=Object.keys(sets)[0];
  showPackUI();
}

function buildSetSelector(){
  var html='',first=true;
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
  showPackUI();
}

function showPackUI(){
  var set=sets[activeSet];
  var le=document.getElementById('loading');
  if(le) le.style.display='none';
  var bestRarity=bestPulls[activeSet+'_best']||'';
  var bestCard=bestPulls[activeSet+'_bestCard']||'';
  var color=SET_COLORS[activeSet]||'#cc0000';
  var sym=SET_LOGOS[activeSet]||'';
  document.getElementById('packStage').innerHTML=
    '<div class=pack-stats id=packStats>'+
      '<b>'+set.displayName+'</b> &middot; '+set.cards.length+' kort &middot; '+
      '<span id=packCount>'+totalOpened+'</span> packs öppnade'+
      (bestRarity?'<br>Bästa drag: <span style=color:var(--gold)>'+bestCard+'</span> ('+bestRarity+')':'')+
    '</div>'+
    '<div class=pack-wrapper id=packWrapper onclick=ripPack()>'+
      '<div class=booster-pack id=boosterPack style=border-color:'+color+'>'+
        '<div class=pack-art style=background:'+color+'22;border:2px solid '+color+'44>'+
          '<span style=font-size:40px;position:absolute>🎴</span>'+
          (sym?'<img src="'+sym+'" alt="" style=width:90%;height:90%;object-fit:contain;position:relative;z-index:1>':'')+
        '</div>'+
        '<div class=pack-label style=color:'+color+'>'+set.displayName+'</div>'+
        '<div class=pack-sub>10 KORT PER PACK</div>'+
      '</div>'+
    '</div>'+
    '<div class=card-stage id=cardStage></div>';
}

// ===== GENERATE PACK (pre-rip, so we know glow color) =====
function generatePack(){
  var set=sets[activeSet];
  var byRarity={};
  set.cards.forEach(function(c){
    var r=c.rarity||'Common';
    if(!byRarity[r])byRarity[r]=[];
    byRarity[r].push(c);
  });

  var pack=[];
  pack=pack.concat(pickRandom(byRarity['Common']||[],5));
  pack=pack.concat(pickRandom(byRarity['Uncommon']||[],3));

  var available=getAvailableRareSlots(byRarity);
  var rareRarity=pickWeighted(available);
  var rareCards=byRarity[rareRarity]||byRarity['Rare']||[];
  pack=pack.concat(pickRandom(rareCards,1));

  var revHolo=pickRandom(set.cards,1)[0];
  revHolo._reverseHolo=true;
  pack.push(revHolo);

  // Shuffle, reverse holo last
  shuffle(pack);
  var rhIdx=-1;
  for(var i=0;i<pack.length;i++){if(pack[i]._reverseHolo){rhIdx=i;break}}
  if(rhIdx>=0){var rh=pack.splice(rhIdx,1)[0];pack.push(rh)}

  return pack;
}

// ===== BEST RARITY IN PACK =====
function bestRarityInPack(pack){
  var best='Common',bestW=0;
  pack.forEach(function(c){
    var w=RARITY_WEIGHT[c.rarity]||0;
    if(w>bestW){best=c.rarity;bestW=w}
  });
  return best;
}

// ===== RIP PACK! =====
var isRipping=false, lastRip=0;
async function ripPack(){
  if(isRipping||Date.now()-lastRip<2000)return;
  isRipping=true;lastRip=Date.now();
  initAudio();
  try{

  var pack=generatePack();
  var bestRar=bestRarityInPack(pack);
  var glowColor=GLOW_COLORS[bestRar]||GLOW_COLORS['Common'];
  var isBigHit=RARITY_WEIGHT[bestRar]>=6;

  totalOpened++;
  // packCount might not exist during quick-rip
  var pc=document.getElementById('packCount');
  if(pc) pc.textContent=totalOpened;

  var stage=document.getElementById('cardStage');
  var wrapper=document.getElementById('packWrapper');
  var booster=document.getElementById('boosterPack');

  // If wrapper is already gone (quick-rip), skip pack animation
  if(wrapper&&booster&&wrapper.style.display!=='none'){
    wrapper.style.pointerEvents='none';
    booster.style.setProperty('--glow',glowColor);
    booster.classList.add('charging');
    await sleep(1200);
    booster.classList.remove('charging');
    booster.classList.add('ripping');
    sfxRip();
    await sleep(250);
    booster.classList.remove('ripping');
    var rect=booster.getBoundingClientRect();
    var cx=rect.left+rect.width/2,cy=rect.top+rect.height/2;
    spawnParticles(cx,cy,20,['⚡','💥','✨']);
    booster.classList.add('ripped');
    if(isBigHit){
      screenFlash(GLOW_COLORS[bestRar]);
      screenShake();
      sfxBigHit();
      document.body.classList.add('glow-bg');
      setTimeout(function(){document.body.classList.remove('glow-bg')},2000);
      spawnParticles(cx,cy,40,['✨','🌟','💫','⭐','🔥','💎']);
    }
    await sleep(400);
    wrapper.style.display='none';
  } else {
    // Quick-rip: just a flash
    sfxRip();
    if(isBigHit){screenShake();sfxBigHit()}
    await sleep(300);
  }

  // Reveal cards
  stage.innerHTML='';
  var commons=pack.filter(function(c){return(RARITY_WEIGHT[c.rarity]||0)<=1&&!c._reverseHolo});
  var uncommons=pack.filter(function(c){return(RARITY_WEIGHT[c.rarity]||0)===2&&!c._reverseHolo});
  var rarePlus=pack.filter(function(c){var w=RARITY_WEIGHT[c.rarity]||0;return w>=3&&!c._reverseHolo});
  var revHolo=pack.filter(function(c){return c._reverseHolo});

  var revealOrder=commons.concat(uncommons).concat(rarePlus).concat(revHolo);
  for(var i=0;i<revealOrder.length;i++){
    var card=revealOrder[i];
    var w=RARITY_WEIGHT[card.rarity]||0;
    if(w>=6) sfxDing();
    else if(w>=4) sfxSparkle();
    else if(w>=1) sfxFlip();
    revealCard(card,stage,i,w);
    await sleep(w>=6?400:w>=4?280:150);
  }

  pack.forEach(function(c){
    var w=RARITY_WEIGHT[c.rarity]||0;
    var bestW=RARITY_WEIGHT[bestPulls[activeSet+'_best']]||0;
    if(w>bestW){bestPulls[activeSet+'_best']=c.rarity;bestPulls[activeSet+'_bestCard']=c.name}
  });

  // Next pack button
  var nextBtn=document.createElement('button');
  nextBtn.className='next-pack-btn';
  nextBtn.innerHTML='Riv upp nästa!';
  nextBtn.onclick=function(){nextBtn.remove();resetAndRip()};
  stage.appendChild(nextBtn);

  }catch(e){console.warn('ripPack error:',e);showPackUI()}
  finally{isRipping=false}
}

function resetAndRip(){
  document.getElementById('cardStage').innerHTML='';
  var wrapper=document.getElementById('packWrapper');
  if(wrapper) wrapper.style.display='';
  ripPack();
}

function revealCard(card,container,index,weight){
  var rc=RARITY_CLASS[card.rarity]||'Common';
  var isHit=weight>=4;
  var isBigHit=weight>=6;
  var rhClass=card._reverseHolo?' reverse-holo':'';
  var holoClass=isHit?' holo':'';
  var bigClass=isBigHit?' big-hit':'';

  var div=document.createElement('div');
  div.className='card rarity-'+rc+rhClass+holoClass+bigClass;
  div.style.animationDelay=(index*.05)+'s';
  if(isBigHit) div.style.setProperty('--hit-glow',HIT_GLOW[card.rarity]||HIT_GLOW['Double Rare']);

  div.innerHTML=
    '<div class=card-img>'+
      '<img src="'+card.image+'" alt="'+card.name+'" loading=lazy onerror="this.style.display=\'none\';this.parentElement.textContent=\''+card.name.substring(0,3)+'\'">'+
    '</div>'+
    '<div class=card-info>'+
      '<div class=card-name>'+(card._reverseHolo?'⭐ ':'')+card.name+'</div>'+
      '<div class="card-rarity rarity-badge-'+rc+'">'+card.rarity+(card._reverseHolo?' RH':'')+'</div>'+
    '</div>';

  container.appendChild(div);

  // Sparkle for hits
  if(isHit){
    setTimeout(function(){
      var r=div.getBoundingClientRect();
      spawnParticles(r.left+r.width/2,r.top+r.height/2,isBigHit?15:5);
    },400);
  }
}

function sleep(ms){return new Promise(function(r){setTimeout(r,ms)})}

// ===== HELPERS =====
function getAvailableRareSlots(byRarity){
  var available=[];
  for(var j=0;j<RARE_SLOT_POOL.length;j++){
    var entry=RARE_SLOT_POOL[j];
    if(byRarity[entry.rarity]&&byRarity[entry.rarity].length>0){
      available.push({rarity:entry.rarity,weight:entry.weight});
    }
  }
  if(byRarity['ACE SPEC Rare']&&byRarity['ACE SPEC Rare'].length>0)
    available.push({rarity:'ACE SPEC Rare',weight:2});
  if(byRarity['Shiny Ultra Rare']&&byRarity['Shiny Ultra Rare'].length>0)
    available.push({rarity:'Shiny Ultra Rare',weight:5});
  if(byRarity['Shiny Rare']&&byRarity['Shiny Rare'].length>0&&!available.find(function(a){return a.rarity==='Shiny Rare'}))
    available.push({rarity:'Shiny Rare',weight:8});
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
  var s=arr.slice();shuffle(s);return s.slice(0,Math.min(count,arr.length));
}
function shuffle(arr){
  for(var i=arr.length-1;i>0;i--){var j=Math.floor(Math.random()*(i+1));var t=arr[i];arr[i]=arr[j];arr[j]=t}
}

// ===== INIT =====
loadSets();
</script>

</body>
</html>"""
