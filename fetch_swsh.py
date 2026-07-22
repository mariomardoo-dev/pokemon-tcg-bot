"""Fetch Sword & Shield sets from TCGdex."""
import json, os, time, urllib.request

SETS = {
    "sword-shield": ("swsh1", "Sword & Shield"),
    "rebel-clash": ("swsh2", "Rebel Clash"),
    "darkness-ablaze": ("swsh3", "Darkness Ablaze"),
    "champions-path": ("swsh3.5", "Champion's Path"),
    "vivid-voltage": ("swsh4", "Vivid Voltage"),
    "shining-fates": ("swsh4.5", "Shining Fates"),
    "battle-styles": ("swsh5", "Battle Styles"),
    "chilling-reign": ("swsh6", "Chilling Reign"),
    "evolving-skies": ("swsh7", "Evolving Skies"),
    "fusion-strike": ("swsh8", "Fusion Strike"),
    "brilliant-stars": ("swsh9", "Brilliant Stars"),
    "astral-radiance": ("swsh10", "Astral Radiance"),
    "pokemon-go": ("swsh10.5", "Pokémon GO"),
    "lost-origin": ("swsh11", "Lost Origin"),
    "silver-tempest": ("swsh12", "Silver Tempest"),
    "crown-zenith": ("swsh12.5", "Crown Zenith"),
}

# Map TCGdex IDs to Pokemon TCG API IDs for images
PTCG_IDS = {
    "swsh1": "swsh1", "swsh2": "swsh2", "swsh3": "swsh3", "swsh3.5": "swsh35",
    "swsh4": "swsh4", "swsh4.5": "swsh45", "swsh5": "swsh5", "swsh6": "swsh6",
    "swsh7": "swsh7", "swsh8": "swsh8", "swsh9": "swsh9", "swsh10": "swsh10",
    "swsh10.5": "swsh105", "swsh11": "swsh11", "swsh12": "swsh12", "swsh12.5": "swsh125",
}

OUT_DIR = os.path.join(os.path.dirname(__file__), "static", "sets")

def assign_rarities(cards):
    n = len(cards)
    for i, c in enumerate(cards):
        pos = i / n
        if pos < 0.35: c["rarity"] = "Common"
        elif pos < 0.55: c["rarity"] = "Uncommon"
        elif pos < 0.70: c["rarity"] = "Rare"
        elif pos < 0.80: c["rarity"] = "Double Rare"
        elif pos < 0.88: c["rarity"] = "Illustration Rare"
        elif pos < 0.94: c["rarity"] = "Ultra Rare"
        elif pos < 0.98: c["rarity"] = "Special Illustration Rare"
        else: c["rarity"] = "Hyper Rare"

def fetch_set(name, sid, display):
    url = f"https://api.tcgdex.net/v2/en/sets/{sid}"
    req = urllib.request.Request(url, headers={"User-Agent": "Pokesniper/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read())
    except Exception as e:
        print(f"  ERROR: {e}")
        return 0
    ptcg_id = PTCG_IDS.get(sid, sid)
    cards = []
    for c in data["cards"]:
        num = c["localId"].lstrip("0") or "0"
        cards.append({
            "name": c["name"],
            "image": f"https://images.pokemontcg.io/{ptcg_id}/{num}.png",
            "number": c["localId"],
            "supertype": "Pokémon",
        })
    assign_rarities(cards)
    path = os.path.join(OUT_DIR, f"{name}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump({"name": name, "displayName": display, "id": sid, "cards": cards}, f, ensure_ascii=False)
    return len(cards)

if __name__ == "__main__":
    total = 0
    for name, (sid, display) in SETS.items():
        print(f"{name}...", end=" ", flush=True)
        c = fetch_set(name, sid, display)
        total += c
        print(f"{c} cards")
        time.sleep(0.3)
    print(f"\nDONE: {total} cards across {len(SETS)} sets")
