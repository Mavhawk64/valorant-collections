import json
import os

import requests
from bs4 import BeautifulSoup

# URL for the main skins directory
URL = "https://valorant.fandom.com/wiki/Weapon_Skins"

response = requests.get(URL)
soup = BeautifulSoup(response.content, "html.parser")

data = []

# Find all tables with class 'wikitable' (there are multiple on the page)
tables = soup.find_all("table", class_="wikitable sortable")

for table in tables:
    if table.find_all("tr")[0].find_all("th")[0].contents[0] != "Image\n":
        continue  # Skip tables that are not skin collections
    tr = table.find_all("tr")[1:]  # Skip header row
    if table.find_all("tr")[0].find_all("th")[-1].contents[0] == "Agent\n":
        for row in tr:
            td = row.find_all("td")
            img_link = (
                td[0].find("a")["href"].split("?")[0]
                if td and td[0] and td[0].find("a") and td[0].find("a")["href"]
                else None
            )
            skin_name = td[1].text.strip() if td and td[1] and td[1].text else None
            skin_type = (
                td[2].find("a").text if td and td[2] and td[2].find("a") else None
            )
            data.append(
                {
                    "img_link": img_link,
                    "edition": None,
                    "skin_name": skin_name,
                    "skin_link": None,
                    "skin_type": skin_type,
                    "melee_name": None,
                }
            )
        continue  # Skip agent tables from further processing
    n_rows = 0
    edition = ""
    skin_name = ""
    skin_link = ""
    for row in tr:
        td = row.find_all("td")
        try:
            # each row will have an img_link and skin_type, but only the first row of each bundle will have the edition and skin_name/skin_link
            if n_rows == 0:
                img_link = (
                    td[0].find("a")["href"].split("?")[0]
                    if td and td[0] and td[0].find("a") and td[0].find("a")["href"]
                    else None
                )
                edition = (
                    td[1].find("span").find("span")["title"]
                    if td
                    and td[1]
                    and td[1].find("span")
                    and td[1].find("span").find("span")
                    and "title" in td[1].find("span").find("span").attrs
                    else None
                )
                skin_name = (
                    td[2].find("a").text if td and td[2] and td[2].find("a") else None
                )
                skin_link = (
                    "https://valorant.fandom.com" + td[2].find("a")["href"]
                    if td and td[2] and td[2].find("a")
                    else None
                )
                skin_type = (
                    td[3].find("a").text if td and td[3] and td[3].find("a") else None
                )
                melee_name = (
                    td[3].text.strip()[len("Melee:") :]
                    if skin_type == "Melee" and td and td[3]
                    else None
                )
                n_rows = int(td[1].get("rowspan", "1;").replace(";", ""))
                data.append(
                    {
                        "img_link": img_link.split("/revision/latest")[0]
                        if img_link
                        else None,
                        "edition": edition,
                        "skin_name": skin_name,
                        "skin_link": skin_link,
                        "skin_type": skin_type,
                        "melee_name": melee_name,
                    }
                )
            else:
                img_link = (
                    td[0].find("a")["href"].split("?")[0]
                    if td and td[0] and td[0].find("a") and td[0].find("a")["href"]
                    else None
                )
                skin_type = (
                    td[1].find("a").text if td and td[1] and td[1].find("a") else None
                )
                melee_name = (
                    td[1].text.strip()[len("Melee:") :]
                    if skin_type == "Melee" and td and td[1]
                    else None
                )
                data.append(
                    {
                        "img_link": img_link.split("/revision/latest")[0]
                        if img_link
                        else None,
                        "edition": edition,
                        "skin_name": skin_name,
                        "skin_link": skin_link,
                        "skin_type": skin_type,
                        "melee_name": melee_name,
                    }
                )
            n_rows -= 1

        except:
            continue  # Skip rows with missing data


# --- OUTPUT CHECK ---
print(f"Found {len(data)} skins.")

# OUTPUT
out_file = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "data", "skins.json"
)
with open(out_file, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=4)
