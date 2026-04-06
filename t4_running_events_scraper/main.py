# region 1. Imports

# downloads the webpage
import requests

# reads/parses HTML
from bs4 import BeautifulSoup

# saves data into CSV file
import csv

# helps find dates with pattern matching
import re
# endregion

# region 2. Load webpage

# stores the page address
url = "https://www.sportlat.lv/kalendars/viss"

# sends request to the website
response = requests.get(url)

# gets the HTML code as text
html = response.text
# endregion

# region 3. Parse HTML

# turns raw HTML text into a structure that Python can search through more easily.
soup = BeautifulSoup(html, "html.parser")
# html = the downloaded page source
# "html.parser" = tells BeautifulSoup how to read it
# endregion