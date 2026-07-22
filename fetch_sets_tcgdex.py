"""Fetch from TCGdex + assign realistic rarities."""
import json, os, time, urllib.request

SETS = {
    "scarlet-violet": ("sv01", "Scarlet & Violet"),
    "paldea-evolved": ("sv02", "Paldea Evolved"),
    "obsidian-flames": ("sv03", "Obsidian Flames"),
    "paradox-rift": ("sv04", "Paradox Rift"),
    "temporal-forces": ("sv05", "Temporal Forces"),
    "twilight-masquerade": ("sv06", "Twilight Masquerade"),
    "shrouded-fable": ("sv6pt5", "Shrouded Fable"),
    "stellar-crown": ("sv07", "Stellar Crown"),
    "surging-sparks": ("sv08", "Surging Sparks"),
    "prismatic-evolutions": ("sv8pt5", "Prismatic Evolutions"),
    "journey-together": ("sv09", "Journey Together"),
    "destined-rivals": ("sv10", "Destined Rivals"),
    "white-flare": ("sv10pt5w", "White Flare"),
    "black-bolt": ("sv10pt5b", "Black Bolt"),
}

OUT_DIR = os.path.join(os.path.dirname(__file__), "static", "sets")

# Rarity distributions per card count (approximate SV-era)
def assign_rarities(cards):
    n = len(cards)
    for i, c in enumerate(cards):
        pos = i / n  # 0 to 1
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
    
    cards = []
    for c in data["cards"]:
        cards.append({
            "name": c["name"],
            "image": f"https://assets.tcgdex.net/en/sv/{sid}/{c['localId']}",
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
        print(f"{name} ({sid})...", end=" ", flush=True)
        c = fetch_set(name, sid, display)
        total += c
        print(f"{c} cards")
        time.sleep(0.3)
    print(f"\nDONE: {total} cards")
