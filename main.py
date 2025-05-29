import requests
import os
import json

API_URL  = "https://db.ygoprodeck.com/api/v7/cardinfo.php"
FILENAME = "YugiohCards.json"

def fetch_all_cards():
    response = requests.get(API_URL)
    if response.status_code == 200:
        return response.json()['data']
    else:
        print(f"Failed to fetch cards: {response.status_code}")
        return []

def encode_cards(cards):
    arena_json = {}
    for card in cards:
        
        try:
            card_type = "Monster"
            if "spell" in card["type"].lower():
                card_type = "Spell"
            elif "trap" in card["type"].lower():
                card_type = "Trap"
            elif "skill" in card["type"].lower():
                card_type = "Skill"
            elif "token" in card["type"].lower():
                card_type = "Token"

            new_card = {
                "id": card["id"],
                "face": {
                    "front": {
                        "name": card["name"],
                        "type": card_type,
                        "cost": 0,
                        "image": card["card_images"][0]["image_url"],
                        "isHorizontal": False
                    }
                },
                "name": card["name"],
                "type": card_type,
                "Type line": card["humanReadableCardType"],
                "cost": 0
            }

            if "archetype" in card:
                new_card["archetype"] = card["archetype"]

            if card_type == "Monster":
                new_card["race"] = card["race"]
                new_card["atk"] = card["atk"]
                new_card["def"] = card["def"]
                new_card["level"] = card["level"]
                new_card["attribute"] = card["attribute"]
                
            elif card_type == "Token":
                new_card["isToken"] = True
            
            arena_json[new_card["id"]] = new_card
        except Exception as e:
            name = card["name"]
            print(f"Exception while processing {name}: [{e}]")

    return arena_json

if __name__ == "__main__":
    cards = fetch_all_cards()

    if cards:
        arena_json = encode_cards(cards)
        
        if os.path.exists(FILENAME):
            os.remove(FILENAME)
        
        with open(FILENAME, "w", encoding="utf8") as f:
            f.write(json.dumps(arena_json, indent=4))