"""Fetch card data from Pokemon TCG API for pack simulator sets."""
import json, time, urllib.request, os

SETS = {
    "151": "sv3pt5",
    "surging-sparks": "sv8",
    "prismatic-evolutions": "sv8pt5",
    "paldean-fates": "sv4pt5",
    "twilight-masquerade": "sv6",
}

OUT_DIR = os.path.join(os.path.dirname(__file__), "static", "sets")
os.makedirs(OUT_DIR, exist_ok=True)

def fetch_set(set_name, set_id):
    """Fetch all cards for a set and save compact JSON."""
    all_cards = []
    page = 1
    
    while True:
        url = f"https://api.pokemontcg.io/v2/cards?q=set.id:{set_id}&pageSize=250&page={page}&select=id,name,rarity,images,number,supertype,subtypes"
        req = urllib.request.Request(url, headers={"User-Agent": "PokesniperPackSim/1.0"})
        
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                data = json.loads(resp.read())
        except Exception as e:
            print(f"  ERROR page {page}: {e}")
            break
        
        for c in data["data"]:
            all_cards.append({
                "name": c["name"],
                "rarity": c.get("rarity", "Common"),
                "image": c.get("images", {}).get("small", ""),
                "number": c.get("number", ""),
                "supertype": c.get("supertype", ""),
            })
        
        print(f"  Page {page}: {len(data['data'])} cards (total so far: {len(all_cards)})")
        
        if len(data["data"]) < 250:
            break
        page += 1
        time.sleep(0.5)  # Rate limit
    
    # Save
    out_path = os.path.join(OUT_DIR, f"{set_name}.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump({"name": set_name, "displayName": set_name.replace("-", " ").title(), "id": set_id, "cards": all_cards}, f, ensure_ascii=False)
    
    print(f"  Saved {len(all_cards)} cards to {out_path}")
    return len(all_cards)

if __name__ == "__main__":
    total = 0
    for name, sid in SETS.items():
        print(f"\n{'='*50}")
        print(f"Fetching: {name} ({sid})")
        print(f"{'='*50}")
        count = fetch_set(name, sid)
        total += count
    
    print(f"\n{'='*50}")
    print(f"DONE! {total} total cards across {len(SETS)} sets")
    print(f"Saved to: {OUT_DIR}")
