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
  display:flex;flex-direction:column;align-items:center;gap:8px;
}
.era-btn{
  padding:12px 28px;border-radius:28px;border:2px solid var(--border);
  background:var(--bg2);color:var(--text);cursor:pointer;
  font-size:16px;font-weight:700;transition:all .3s;
  display:flex;align-items:center;gap:10px;
}
.era-btn:hover{border-color:var(--red);box-shadow:0 0 24px rgba(204,0,0,.15)}
.era-btn.open{border-color:var(--red);border-radius:28px 28px 8px 8px}
.era-btn img{height:28px;width:auto}
.era-btn .arrow{font-size:12px;transition:transform .3s;color:var(--muted)}
.era-btn.open .arrow{transform:rotate(180deg)}
.set-grid{
  display:none;flex-wrap:wrap;justify-content:center;gap:8px;
  max-width:900px;background:var(--bg2);border:2px solid var(--red);
  border-top:none;border-radius:0 0 16px 16px;padding:16px;
}
.set-grid.open{display:flex}
.set-btn{
  padding:8px 16px;border-radius:20px;border:1px solid var(--border);
  background:var(--bg3);color:var(--muted);cursor:pointer;
  font-size:13px;transition:all .2s;white-space:nowrap;
}
.set-btn:hover{border-color:var(--red);color:var(--text)}
.set-btn.active{
  background:#1a0000;border-color:var(--red);color:var(--red);
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
  text-transform:uppercase;z-index:1;text-align:center;
}
.booster-pack .pack-sub{
  font-size:10px;color:rgba(255,255,255,.4);letter-spacing:2px;z-index:1;
}
.booster-pack .pack-sim-label{
  font-size:8px;color:rgba(255,255,255,.35);letter-spacing:1px;z-index:1;
  font-weight:300;margin-top:2px;
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
.card-fallback{
  display:flex;align-items:center;justify-content:center;
  width:100%;height:100%;font-size:10px;color:#555;
  text-align:center;padding:4px;word-break:break-word;
  font-weight:600;
}
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
  display:block;margin:14px auto 0;padding:7px 10px;
  font-size:11px;font-weight:500;color:#999;
  background:transparent;border:1px solid #333;
  border-radius:5px;cursor:pointer;
  text-transform:uppercase;letter-spacing:.5px;
  transition:all .2s;
}
.next-pack-btn:hover{
  background:rgba(204,0,0,.12);color:var(--red);
  border-color:rgba(204,0,0,.3);
}
.next-pack-btn:active{transform:scale(.96)}
@keyframes fadeIn{from{opacity:0;transform:translateY(10px)}to{opacity:1;transform:translateY(0)}}

footer{text-align:center;padding:24px;color:var(--muted);font-size:12px;border-top:1px solid var(--border)}

@media(max-width:600px){
  .card{width:95px}.card-img{height:130px}
  .pack-wrapper{width:160px;height:224px}
  .booster-pack .pack-art{width:100px;height:100px;font-size:40px}
  .booster-pack .pack-label{font-size:14px}
  .era-btn{font-size:14px;padding:10px 20px}
  .era-btn img{height:22px}
  .set-btn{padding:6px 12px;font-size:11px}
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
  {rarity:'Rare',weight:120},                      // ~64% — regular holo rare (baseline)
  {rarity:'Double Rare',weight:30},                // ~16% — 1 in 6 packs (3-4 per booster box)
  {rarity:'Illustration Rare',weight:14},          // ~7.5% — 1 in 13 packs (2-3 per box)
  {rarity:'Ultra Rare',weight:10},                 // ~5.3% — 1 in 19 packs
  {rarity:'Special Illustration Rare',weight:2},   // ~1.1% — 1 in 93 packs (<1 per box)
  {rarity:'Hyper Rare',weight:1},                  // ~0.5% — 1 in 187 packs (1 per 4-5 boxes)
];

// ===== ERA DEFINITIONS =====
var ERAS=[
  {id:'sv',name:'Scarlet & Violet',logo:'https://assets.tcgdex.net/en/sv/sv01/logo.png',sets:[
    'scarlet-violet','paldea-evolved','obsidian-flames','151','paradox-rift',
    'paldean-fates','temporal-forces','twilight-masquerade','shrouded-fable','stellar-crown',
    'surging-sparks','prismatic-evolutions','journey-together','destined-rivals',
    'white-flare','black-bolt'
  ]},
  {id:'swsh',name:'Sword & Shield',logo:'https://images.pokemontcg.io/swsh1/logo.png',sets:[
    'sword-shield','rebel-clash','darkness-ablaze','champions-path','vivid-voltage',
    'shining-fates','battle-styles','chilling-reign','evolving-skies','fusion-strike',
    'brilliant-stars','astral-radiance','pokemon-go','lost-origin','silver-tempest','crown-zenith'
  ]},
  {id:'meg',name:'Mega Evolution',logo:'',sets:[
    'mega-evolution','phantasmal-flames','ascended-heroes','perfect-order','chaos-rising','pitch-black'
  ]},
];
var SET_LOGOS={
  'scarlet-violet':'https://images.pokemontcg.io/sv1/logo.png',
  'paldea-evolved':'https://images.pokemontcg.io/sv2/logo.png',
  'obsidian-flames':'https://images.pokemontcg.io/sv3/logo.png',
  '151':'https://images.pokemontcg.io/sv3pt5/logo.png',
  'paradox-rift':'https://images.pokemontcg.io/sv4/logo.png',
  'paldean-fates':'https://images.pokemontcg.io/sv4pt5/logo.png',
  'temporal-forces':'https://images.pokemontcg.io/sv5/logo.png',
  'twilight-masquerade':'https://images.pokemontcg.io/sv6/logo.png',
  'shrouded-fable':'https://images.pokemontcg.io/sv6pt5/logo.png',
  'stellar-crown':'https://images.pokemontcg.io/sv7/logo.png',
  'surging-sparks':'https://images.pokemontcg.io/sv8/logo.png',
  'prismatic-evolutions':'https://images.pokemontcg.io/sv8pt5/logo.png',
  'journey-together':'https://images.pokemontcg.io/sv9/logo.png',
  'destined-rivals':'https://images.pokemontcg.io/sv10/logo.png',
  'white-flare':'https://assets.tcgdex.net/en/sv/sv10.5w/logo.png',
  'black-bolt':'https://assets.tcgdex.net/en/sv/sv10.5b/logo.png',
  // Sword & Shield
  'sword-shield':'https://images.pokemontcg.io/swsh1/logo.png',
  'rebel-clash':'https://images.pokemontcg.io/swsh2/logo.png',
  'darkness-ablaze':'https://images.pokemontcg.io/swsh3/logo.png',
  'champions-path':'https://images.pokemontcg.io/swsh35/logo.png',
  'vivid-voltage':'https://images.pokemontcg.io/swsh4/logo.png',
  'shining-fates':'https://images.pokemontcg.io/swsh45/logo.png',
  'battle-styles':'https://images.pokemontcg.io/swsh5/logo.png',
  'chilling-reign':'https://images.pokemontcg.io/swsh6/logo.png',
  'evolving-skies':'https://images.pokemontcg.io/swsh7/logo.png',
  'fusion-strike':'https://images.pokemontcg.io/swsh8/logo.png',
  'brilliant-stars':'https://images.pokemontcg.io/swsh9/logo.png',
  'astral-radiance':'https://images.pokemontcg.io/swsh10/logo.png',
  'pokemon-go':'https://images.pokemontcg.io/pgo/logo.png',
  'lost-origin':'https://images.pokemontcg.io/swsh11/logo.png',
  'silver-tempest':'https://images.pokemontcg.io/swsh12/logo.png',
  'crown-zenith':'https://images.pokemontcg.io/swsh12pt5/logo.png',
  // Sun & Moon — use TCGdex logos
  'sun-moon':'https://assets.tcgdex.net/en/sm/sm1/logo.png',
  'guardians-rising':'https://assets.tcgdex.net/en/sm/sm2/logo.png',
  'burning-shadows':'https://assets.tcgdex.net/en/sm/sm3/logo.png',
  'shining-legends':'https://assets.tcgdex.net/en/sm/sm3.5/logo.png',
  'crimson-invasion':'https://assets.tcgdex.net/en/sm/sm4/logo.png',
  'ultra-prism':'https://assets.tcgdex.net/en/sm/sm5/logo.png',
  'forbidden-light':'https://assets.tcgdex.net/en/sm/sm6/logo.png',
  'celestial-storm':'https://assets.tcgdex.net/en/sm/sm7/logo.png',
  'dragon-majesty':'https://assets.tcgdex.net/en/sm/sm7.5/logo.png',
  'lost-thunder':'https://assets.tcgdex.net/en/sm/sm8/logo.png',
  'team-up':'https://assets.tcgdex.net/en/sm/sm9/logo.png',
  'unbroken-bonds':'https://assets.tcgdex.net/en/sm/sm10/logo.png',
  'unified-minds':'https://assets.tcgdex.net/en/sm/sm11/logo.png',
  'hidden-fates':'https://assets.tcgdex.net/en/sm/sm115/logo.png',
  'cosmic-eclipse':'https://assets.tcgdex.net/en/sm/sm12/logo.png',
  // Older eras — TCGdex logos
  'xy-base':'https://assets.tcgdex.net/en/xy/xy1/logo.png',
  'flashfire':'https://assets.tcgdex.net/en/xy/xy2/logo.png',
  'furious-fists':'https://assets.tcgdex.net/en/xy/xy3/logo.png',
  'phantom-forces':'https://assets.tcgdex.net/en/xy/xy4/logo.png',
  'primal-clash':'https://assets.tcgdex.net/en/xy/xy5/logo.png',
  'roaring-skies':'https://assets.tcgdex.net/en/xy/xy6/logo.png',
  'ancient-origins':'https://assets.tcgdex.net/en/xy/xy7/logo.png',
  'breakthrough':'https://assets.tcgdex.net/en/xy/xy8/logo.png',
  'breakpoint':'https://assets.tcgdex.net/en/xy/xy9/logo.png',
  'fates-collide':'https://assets.tcgdex.net/en/xy/xy10/logo.png',
  'steam-siege':'https://assets.tcgdex.net/en/xy/xy11/logo.png',
  'evolutions':'https://assets.tcgdex.net/en/xy/xy12/logo.png',
  // BW
  'black-white':'https://assets.tcgdex.net/en/bw/bw1/logo.png',
  'emerging-powers':'https://assets.tcgdex.net/en/bw/bw2/logo.png',
  'noble-victories':'https://assets.tcgdex.net/en/bw/bw3/logo.png',
  'next-destinies':'https://assets.tcgdex.net/en/bw/bw4/logo.png',
  'dark-explorers':'https://assets.tcgdex.net/en/bw/bw5/logo.png',
  'dragons-exalted':'https://assets.tcgdex.net/en/bw/bw6/logo.png',
  'boundaries-crossed':'https://assets.tcgdex.net/en/bw/bw7/logo.png',
  'plasma-storm':'https://assets.tcgdex.net/en/bw/bw8/logo.png',
  'plasma-freeze':'https://assets.tcgdex.net/en/bw/bw9/logo.png',
  'plasma-blast':'https://assets.tcgdex.net/en/bw/bw10/logo.png',
  'legendary-treasures':'https://assets.tcgdex.net/en/bw/bw11/logo.png',
  'heartgold-soulsilver':'https://assets.tcgdex.net/en/hgss/hgss1/logo.png',
  'unleashed':'https://assets.tcgdex.net/en/hgss/hgss2/logo.png',
  'undaunted':'https://assets.tcgdex.net/en/hgss/hgss3/logo.png',
  'triumphant':'https://assets.tcgdex.net/en/hgss/hgss4/logo.png',
  'diamond-pearl':'https://assets.tcgdex.net/en/dp/dp1/logo.png',
  'mysterious-treasures':'https://assets.tcgdex.net/en/dp/dp2/logo.png',
  'secret-wonders':'https://assets.tcgdex.net/en/dp/dp3/logo.png',
  'great-encounters':'https://assets.tcgdex.net/en/dp/dp4/logo.png',
  'majestic-dawn':'https://assets.tcgdex.net/en/dp/dp5/logo.png',
  'legends-awakened':'https://assets.tcgdex.net/en/dp/dp6/logo.png',
  'stormfront':'https://assets.tcgdex.net/en/dp/dp7/logo.png',
  'platinum':'https://assets.tcgdex.net/en/pl/pl1/logo.png',
  'rising-rivals':'https://assets.tcgdex.net/en/pl/pl2/logo.png',
  'supreme-victors':'https://assets.tcgdex.net/en/pl/pl3/logo.png',
  'arceus':'https://assets.tcgdex.net/en/pl/pl4/logo.png',
  'ruby-sapphire':'https://assets.tcgdex.net/en/ex/ex1/logo.png',
  'sandstorm':'https://assets.tcgdex.net/en/ex/ex2/logo.png',
  'dragon':'https://assets.tcgdex.net/en/ex/ex3/logo.png',
  'team-magma-aqua':'https://assets.tcgdex.net/en/ex/ex4/logo.png',
  'hidden-legends':'https://assets.tcgdex.net/en/ex/ex5/logo.png',
  'firered-leafgreen':'https://assets.tcgdex.net/en/ex/ex6/logo.png',
  'team-rocket-returns':'https://assets.tcgdex.net/en/ex/ex7/logo.png',
  'deoxys':'https://assets.tcgdex.net/en/ex/ex8/logo.png',
  'emerald':'https://assets.tcgdex.net/en/ex/ex9/logo.png',
  'unseen-forces':'https://assets.tcgdex.net/en/ex/ex10/logo.png',
  'delta-species':'https://assets.tcgdex.net/en/ex/ex11/logo.png',
  'legend-maker':'https://assets.tcgdex.net/en/ex/ex12/logo.png',
  'holon-phantoms':'https://assets.tcgdex.net/en/ex/ex13/logo.png',
  'crystal-guardians':'https://assets.tcgdex.net/en/ex/ex14/logo.png',
  'dragon-frontiers':'https://assets.tcgdex.net/en/ex/ex15/logo.png',
  'power-keepers':'https://assets.tcgdex.net/en/ex/ex16/logo.png',
  'neo-genesis':'https://assets.tcgdex.net/en/neo/neo1/logo.png',
  'neo-discovery':'https://assets.tcgdex.net/en/neo/neo2/logo.png',
  'neo-revelation':'https://assets.tcgdex.net/en/neo/neo3/logo.png',
  'neo-destiny':'https://assets.tcgdex.net/en/neo/neo4/logo.png',
  'expedition':'https://assets.tcgdex.net/en/ecard/ecard1/logo.png',
  'aquapolis':'https://assets.tcgdex.net/en/ecard/ecard2/logo.png',
  'skyridge':'https://assets.tcgdex.net/en/ecard/ecard3/logo.png',
  'base-set':'https://assets.tcgdex.net/en/base/base1/logo.png',
  'jungle':'https://assets.tcgdex.net/en/base/base2/logo.png',
  'fossil':'https://assets.tcgdex.net/en/base/base3/logo.png',
  'base-set-2':'https://assets.tcgdex.net/en/base/base4/logo.png',
  'team-rocket':'https://assets.tcgdex.net/en/base/base5/logo.png',
  // Mega Evolution
  'mega-evolution':'',
  'phantasmal-flames':'',
  'ascended-heroes':'',
  'perfect-order':'',
  'chaos-rising':'',
  'pitch-black':'',
};
var SET_COLORS={
  'scarlet-violet':'#e0245e','paldea-evolved':'#f59e0b','obsidian-flames':'#ef4444',
  '151':'#e8c547','paradox-rift':'#a855f7','paldean-fates':'#f472b6',
  'temporal-forces':'#06b6d4','twilight-masquerade':'#34d399','shrouded-fable':'#8b5cf6',
  'stellar-crown':'#fbbf24','surging-sparks':'#ff6b35','prismatic-evolutions':'#c4b5fd',
  'journey-together':'#22c55e','destined-rivals':'#dc2626','white-flare':'#f8fafc','black-bolt':'#1e1b4b',
  'sword-shield':'#4f9bc2','rebel-clash':'#e85d3a','darkness-ablaze':'#e04040','champions-path':'#c9a44b',
  'vivid-voltage':'#f5c842','shining-fates':'#f472b6','battle-styles':'#c44b4b','chilling-reign':'#5ba0c8',
  'evolving-skies':'#8bc5e8','fusion-strike':'#b880c8','brilliant-stars':'#f5a623','astral-radiance':'#6db3c4',
  'pokemon-go':'#f5c542','lost-origin':'#c090e0','silver-tempest':'#88b8d8','crown-zenith':'#e8c547',
  // Sun & Moon
  'sun-moon':'#f5a623','guardians-rising':'#4a90d9','burning-shadows':'#e85d3a','shining-legends':'#c9a44b',
  'crimson-invasion':'#8b0000','ultra-prism':'#7b68ee','forbidden-light':'#4169e1','celestial-storm':'#87ceeb',
  'dragon-majesty':'#b8860b','lost-thunder':'#ffd700','team-up':'#ff6347','unbroken-bonds':'#daa520',
  'unified-minds':'#9370db','hidden-fates':'#ff69b4','cosmic-eclipse':'#2f4f4f',
  // XY
  'xy-base':'#4169e1','flashfire':'#ff4500','furious-fists':'#ff8c00','phantom-forces':'#6a0dad',
  'primal-clash':'#00bfff','roaring-skies':'#87ceeb','ancient-origins':'#8b4513','breakthrough':'#ffd700',
  'breakpoint':'#00ced1','fates-collide':'#32cd32','steam-siege':'#708090','evolutions':'#ff6347',
  // Black & White
  'black-white':'#333','emerging-powers':'#228b22','noble-victories':'#daa520','next-destinies':'#4169e1',
  'dark-explorers':'#2f4f4f','dragons-exalted':'#ffd700','boundaries-crossed':'#87ceeb','plasma-storm':'#00bfff',
  'plasma-freeze':'#87cefa','plasma-blast':'#ff4500','legendary-treasures':'#ffd700',
  // HGSS
  'heartgold-soulsilver':'#daa520','unleashed':'#ff6347','undaunted':'#4169e1','triumphant':'#32cd32',
  // Diamond & Pearl
  'diamond-pearl':'#b0c4de','mysterious-treasures':'#daa520','secret-wonders':'#9370db','great-encounters':'#4169e1',
  'majestic-dawn':'#ffd700','legends-awakened':'#ff6347','stormfront':'#708090','platinum':'#c0c0c0',
  'rising-rivals':'#ff4500','supreme-victors':'#ffd700','arceus':'#f5f5dc',
  // EX
  'ruby-sapphire':'#dc143c','sandstorm':'#daa520','dragon':'#4169e1','team-magma-aqua':'#ff4500',
  'hidden-legends':'#9370db','firered-leafgreen':'#ff4500','team-rocket-returns':'#333','deoxys':'#ff6347',
  'emerald':'#32cd32','unseen-forces':'#6a0dad','delta-species':'#ffd700','legend-maker':'#ffa500',
  'holon-phantoms':'#87ceeb','crystal-guardians':'#00bfff','dragon-frontiers':'#ffd700','power-keepers':'#daa520',
  // Neo / e-Series
  'neo-genesis':'#daa520','neo-discovery':'#4169e1','neo-revelation':'#9370db','neo-destiny':'#ff6347',
  'expedition':'#ffd700','aquapolis':'#00bfff','skyridge':'#87ceeb',
  // Wizards / Base
  'base-set':'#ffd700','jungle':'#228b22','fossil':'#708090','base-set-2':'#ffd700','team-rocket':'#333',
  // Mega Evolution
  'mega-evolution':'#ff4500','phantasmal-flames':'#ff6347','ascended-heroes':'#daa520',
  'perfect-order':'#4169e1','chaos-rising':'#8b0000','pitch-black':'#1a1a2e',
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
  var setFiles=[];
  ERAS.forEach(function(e){setFiles=setFiles.concat(e.sets)});
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
  var sel=document.getElementById('setSelector');
  sel.innerHTML='';
  ERAS.forEach(function(era){
    var logoHtml=era.logo?'<img src="'+era.logo+'" alt="">':'<span style=font-size:22px>🎴</span>';
    sel.innerHTML+=
      '<button class=era-btn onclick=toggleEra(this)>'+
        logoHtml+era.name+
        '<span class=arrow>▼</span>'+
      '</button>'+
      '<div class=set-grid id=grid-'+era.id+'></div>';
    var grid=document.getElementById('grid-'+era.id);
    era.sets.forEach(function(key,idx){
      if(!sets[key])return;
      grid.innerHTML+='<button class="set-btn'+(idx===0&&era.id==='sv'?' active':'')+'" data-key="'+key+'" onclick="selectSet(\''+key+'\',this)">'+sets[key].displayName+'</button>';
    });
  });
}

function toggleEra(btn){
  var grid=btn.nextElementSibling;
  grid.classList.toggle('open');
  btn.classList.toggle('open');
}

function selectSet(key,btn){
  activeSet=key;
  document.querySelectorAll('.set-btn').forEach(function(b){b.classList.remove('active')});
  btn.classList.add('active');
  btn.closest('.set-grid').classList.remove('open');
  btn.closest('.set-grid').previousElementSibling.classList.remove('open');
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
        '<div class=pack-sub>Öppna Pokemon Pack!</div>'+
        '<div class=pack-sim-label>Pack Simulator</div>'+
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
  nextBtn.innerHTML='Fortsätt öppna';
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
      (card.image?'<img src="'+card.image+'" alt="'+card.name+'" loading=lazy onerror="this.style.display=\'none\';this.nextElementSibling.style.display=\'flex\'">':'')+
      '<span class=card-fallback style=display:'+(card.image?'none':'flex')+'>'+card.name.substring(0,15)+'</span>'+
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
    available.push({rarity:'ACE SPEC Rare',weight:10});
  if(byRarity['Shiny Ultra Rare']&&byRarity['Shiny Ultra Rare'].length>0)
    available.push({rarity:'Shiny Ultra Rare',weight:8});
  if(byRarity['Shiny Rare']&&byRarity['Shiny Rare'].length>0&&!available.find(function(a){return a.rarity==='Shiny Rare'}))
    available.push({rarity:'Shiny Rare',weight:12});
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
