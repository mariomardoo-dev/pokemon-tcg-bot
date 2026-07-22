"""Fetch Mega Evolution era sets."""
import json, os, time, urllib.request

SETS = {
    "mega-evolution": ("me01", "Mega Evolution"),
    "phantasmal-flames": ("me02", "Phantasmal Flames"),
    "ascended-heroes": ("me02.5", "Ascended Heroes"),
    "perfect-order": ("me03", "Perfect Order"),
    "chaos-rising": ("me04", "Chaos Rising"),
    "pitch-black": ("me05", "Pitch Black"),
}

OUT_DIR = os.path.join(os.path.dirname(__file__), "static", "sets")

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
        num = c["localId"].lstrip("0") or "0"
        cards.append({
            "name": c["name"],
            "image": f"https://images.pokemontcg.io/{sid}/{num}.png",
            "number": c["localId"],
            "supertype": "Pokémon",
        })
    # Use real rarities from TCGdex if available? No — use distribution
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
    print(f"\nDONE: {total} cards")
