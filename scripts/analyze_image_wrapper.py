import json
import os
import time
from io import BytesIO

import google.generativeai as genai
import requests
from dotenv import load_dotenv
from PIL import Image

dev = False  # Set to True for local testing

load_dotenv()
# 1. Get your free API key here: https://aistudio.google.com/app/apikey
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

genai.configure(api_key=GOOGLE_API_KEY)

# Use Flash - it's fast, cheap (free tier), and smart enough for tagging
model = genai.GenerativeModel("gemini-2.5-flash")


def get_valorant_tags(image_url):
    try:
        # 1. Download the image first
        response = requests.get(image_url)
        response.raise_for_status()

        # Convert to a format Gemini accepts (PIL Image)
        img_data = Image.open(BytesIO(response.content))

        # 2. The Prompt
        # We specifically ask for the *aesthetic* and *theme* to get tags like "evil" or "aquatic"
        prompt = (
            "Analyze this Valorant weapon skin. "
            "Generate a list of 8-12 descriptive tags focusing on its theme, "
            "visual effects, colors, mood, and material (e.g., metallic, organic). "
            "Do not use generic tags like 'gun' or 'weapon'. "
            "If it looks underwater, use tags like 'aquatic, coral'. "
            "If it looks dark/purple, use tags like 'ominous, ghost'. "
            "Return ONLY the tags as a comma-separated list."
        )

        # 3. Generate Content
        response = model.generate_content([prompt, img_data])

        # Clean up the text (remove brackets if the AI adds them)
        tags = response.text.strip().replace("[", "").replace("]", "")
        # Convert to list and strip whitespace
        tags = [tag.strip() for tag in tags.split(",")]
        return tags

    except Exception as e:
        print(f"Error processing {image_url}: {e}")
        print("Exiting to avoid rate limit issues. Please try again tomorrow.")
        exit(1)


if __name__ == "__main__" and dev:
    # --- Example Usage ---
    # Replace these with real Valorant skin URLs
    skin_urls = [
        "https://static.wikia.nocookie.net/valorant/images/9/95/Abyssal_Phantom.png/revision/latest",  # Abyssal (Underwater)
        "https://static.wikia.nocookie.net/valorant/images/2/27/Reaver_Vandal.png/revision/latest",  # Reaver (Dark/Ghost)
    ]

    print("Starting tagging job...")

    for url in skin_urls:
        tags = get_valorant_tags(url)
        print(f"\nURL: {url}\nTags: [{tags}]")

        # IMPORTANT: The Free Tier limit is 15 requests per minute.
        # We sleep 4 seconds to be safe (60s / 15 = 4s).
        time.sleep(4)
elif __name__ == "__main__":
    with open(
        os.path.join(os.path.dirname(__file__), "../data/skins_with_tags.json")
    ) as f:
        skins_with_tags = json.load(f)

    with open(os.path.join(os.path.dirname(__file__), "../data/skins.json")) as f:
        skins_data = json.load(f)
        # merge existing tags
        for skin_with_tags in skins_with_tags:
            for skin in skins_data:
                if (
                    skin_with_tags["skin_name"] == skin["skin_name"]
                    and skin_with_tags["skin_type"] == skin["skin_type"]
                    and skin_with_tags["melee_name"] == skin["melee_name"]
                ):
                    skin["tags"] = skin_with_tags.get("tags", [])
                    print(
                        f"Merged tags for skin: {skin['skin_name']} ({skin['skin_type']}) -- Tags: {skin.get('tags', [])}"
                    )
                    break

        for skin in skins_data:
            img_link = skin.get("img_link")
            if img_link and not skin.get("tags"):
                print(
                    f"Processing skin: {skin.get('skin_name')} {skin.get('melee_name') if skin.get('skin_type') == 'Melee' else skin.get('skin_type')}"
                )
                tags = get_valorant_tags(img_link)
                skin["tags"] = tags
                # save to file after each skin to avoid data loss
                with open(
                    os.path.join(
                        os.path.dirname(__file__), "../data/skins_with_tags.json"
                    ),
                    "w",
                ) as f:
                    json.dump(skins_data, f, indent=4)
                print(
                    f"Processed skin: {skin.get('skin_name')} {skin.get('melee_name') if skin.get('skin_type') == 'Melee' else skin.get('skin_type')} - Tags: {tags}"
                )
                # time.sleep(4)  # Respect rate limit
    with open(
        os.path.join(os.path.dirname(__file__), "../data/skins_with_tags.json"), "w"
    ) as f:
        json.dump(skins_data, f, indent=4)
    print("Tagging job completed. Results saved to skins_with_tags.json.")
