import requests
from bs4 import BeautifulSoup

def get_countries():
    response = requests.get("https://www.worldometers.info/geography/flags-of-the-world/")
    soup = BeautifulSoup(response.content, "html.parser")

    data = soup.find_all("div", style="font-weight:bold; padding-top:10px")

    return [str(item.text).lower() for item in data]


