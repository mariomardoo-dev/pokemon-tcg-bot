"""Fetch ALL remaining eras from TCGdex."""
import json, os, time, urllib.request

SETS = {
    # Wizards / Base Era
    "base-set": ("base1", "Base Set"), "jungle": ("base2", "Jungle"),
    "fossil": ("base3", "Fossil"), "base-set-2": ("base4", "Base Set 2"),
    "team-rocket": ("base5", "Team Rocket"),
    # Neo
    "neo-genesis": ("neo1", "Neo Genesis"), "neo-discovery": ("neo2", "Neo Discovery"),
    "neo-revelation": ("neo3", "Neo Revelation"), "neo-destiny": ("neo4", "Neo Destiny"),
    # e-Series
    "expedition": ("ecard1", "Expedition"), "aquapolis": ("ecard2", "Aquapolis"),
    "skyridge": ("ecard3", "Skyridge"),
    # EX Series
    "ruby-sapphire": ("ex1", "Ruby & Sapphire"), "sandstorm": ("ex2", "Sandstorm"),
    "dragon": ("ex3", "Dragon"), "team-magma-aqua": ("ex4", "Team Magma vs Team Aqua"),
    "hidden-legends": ("ex5", "Hidden Legends"), "firered-leafgreen": ("ex6", "FireRed & LeafGreen"),
    "team-rocket-returns": ("ex7", "Team Rocket Returns"), "deoxys": ("ex8", "Deoxys"),
    "emerald": ("ex9", "Emerald"), "unseen-forces": ("ex10", "Unseen Forces"),
    "delta-species": ("ex11", "Delta Species"), "legend-maker": ("ex12", "Legend Maker"),
    "holon-phantoms": ("ex13", "Holon Phantoms"), "crystal-guardians": ("ex14", "Crystal Guardians"),
    "dragon-frontiers": ("ex15", "Dragon Frontiers"), "power-keepers": ("ex16", "Power Keepers"),
    # Diamond & Pearl
    "diamond-pearl": ("dp1", "Diamond & Pearl"), "mysterious-treasures": ("dp2", "Mysterious Treasures"),
    "secret-wonders": ("dp3", "Secret Wonders"), "great-encounters": ("dp4", "Great Encounters"),
    "majestic-dawn": ("dp5", "Majestic Dawn"), "legends-awakened": ("dp6", "Legends Awakened"),
    "stormfront": ("dp7", "Stormfront"), "platinum": ("pl1", "Platinum"),
    "rising-rivals": ("pl2", "Rising Rivals"), "supreme-victors": ("pl3", "Supreme Victors"),
    "arceus": ("pl4", "Arceus"),
    # HeartGold & SoulSilver
    "heartgold-soulsilver": ("hgss1", "HeartGold SoulSilver"), "unleashed": ("hgss2", "Unleashed"),
    "undaunted": ("hgss3", "Undaunted"), "triumphant": ("hgss4", "Triumphant"),
    # Black & White
    "black-white": ("bw1", "Black & White"), "emerging-powers": ("bw2", "Emerging Powers"),
    "noble-victories": ("bw3", "Noble Victories"), "next-destinies": ("bw4", "Next Destinies"),
    "dark-explorers": ("bw5", "Dark Explorers"), "dragons-exalted": ("bw6", "Dragons Exalted"),
    "boundaries-crossed": ("bw7", "Boundaries Crossed"), "plasma-storm": ("bw8", "Plasma Storm"),
    "plasma-freeze": ("bw9", "Plasma Freeze"), "plasma-blast": ("bw10", "Plasma Blast"),
    "legendary-treasures": ("bw11", "Legendary Treasures"),
    # XY
    "xy-base": ("xy1", "XY"), "flashfire": ("xy2", "Flashfire"),
    "furious-fists": ("xy3", "Furious Fists"), "phantom-forces": ("xy4", "Phantom Forces"),
    "primal-clash": ("xy5", "Primal Clash"), "roaring-skies": ("xy6", "Roaring Skies"),
    "ancient-origins": ("xy7", "Ancient Origins"), "breakthrough": ("xy8", "BREAKthrough"),
    "breakpoint": ("xy9", "BREAKpoint"), "fates-collide": ("xy10", "Fates Collide"),
    "steam-siege": ("xy11", "Steam Siege"), "evolutions": ("xy12", "Evolutions"),
    # Sun & Moon
    "sun-moon": ("sm1", "Sun & Moon"), "guardians-rising": ("sm2", "Guardians Rising"),
    "burning-shadows": ("sm3", "Burning Shadows"), "shining-legends": ("sm3.5", "Shining Legends"),
    "crimson-invasion": ("sm4", "Crimson Invasion"), "ultra-prism": ("sm5", "Ultra Prism"),
    "forbidden-light": ("sm6", "Forbidden Light"), "celestial-storm": ("sm7", "Celestial Storm"),
    "dragon-majesty": ("sm7.5", "Dragon Majesty"), "lost-thunder": ("sm8", "Lost Thunder"),
    "team-up": ("sm9", "Team Up"), "unbroken-bonds": ("sm10", "Unbroken Bonds"),
    "unified-minds": ("sm11", "Unified Minds"), "hidden-fates": ("sm115", "Hidden Fates"),
    "cosmic-eclipse": ("sm12", "Cosmic Eclipse"),
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
    cards = []
    for c in data["cards"]:
        num = c["localId"].lstrip("0") or "0"
        cards.append({
            "name": c["name"],
            "image": "",
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
        path = os.path.join(OUT_DIR, f"{name}.json")
        if os.path.exists(path) and os.path.getsize(path) > 1000:
            print(f"{name}: SKIP (exists)")
            continue
        print(f"{name}...", end=" ", flush=True)
        c = fetch_set(name, sid, display)
        total += c
        print(f"{c} cards")
        time.sleep(0.2)
    print(f"\nDONE: {total} new cards")
