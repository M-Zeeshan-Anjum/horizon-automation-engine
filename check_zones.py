# to check account settings on brightdata

import requests

BRIGHT_DATA_API_KEY = "9dd38ee5-36cd-468e-89ea-d8c772ebf38e"
response = requests.get(
    "https://api.brightdata.com/zone/get_active_zones", 
    headers={"Authorization": f"Bearer {BRIGHT_DATA_API_KEY}"}
)

print("--- YOUR ACTIVE HACKATHON ZONES ---")
print(response.text)