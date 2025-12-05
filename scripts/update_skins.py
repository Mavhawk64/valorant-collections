import requests
from bs4 import BeautifulSoup

# URL for the main skins directory
URL = "https://valorant.fandom.com/wiki/Weapon_Skins"

response = requests.get(URL)
soup = BeautifulSoup(response.content, "html.parser")

collections_data = []

# Find all tables with class 'wikitable' (there are multiple on the page)
tables = soup.find_all("table", class_="wikitable")

for table in tables:
    # Iterate through every row in the table
    for row in table.find_all("tr"):
        # We only care about cells (td), not headers (th)
        cells = row.find_all("td")

        for cell in cells:
            # 1. IDENTIFY TIER
            # The tier name (e.g., "Select:") is usually in a <b> tag
            tier_tag = cell.find("b")
            if tier_tag:
                current_tier = tier_tag.get_text(strip=True).replace(":", "")
            else:
                # Fallback if no bold tag found (sometimes 'Other' sections differ)
                current_tier = "Uncategorized"

            # 2. EXTRACT COLLECTION LINKS
            # All collection links are <a> tags inside this cell
            links = cell.find_all("a")

            for link in links:
                # Extract attributes safely
                href = link.get("href")
                title = link.get("title")

                # specific wiki logic:
                # 1. Check if title exists
                # 2. Check if href exists (is not None)
                # 3. Check if "/wiki/" is inside the href string
                if title and href and "/wiki/" in href:
                    full_url = f"https://valorant.fandom.com{href}"

                    collections_data.append(
                        {
                            "collection_name": title,
                            "tier": current_tier,
                            "url": full_url,
                        }
                    )

# --- OUTPUT CHECK ---
print(f"Found {len(collections_data)} collections.")
# Example output: {'collection_name': 'Reaver Collection', 'tier': 'Premium', 'url': '...'}
print(collections_data[:3])
