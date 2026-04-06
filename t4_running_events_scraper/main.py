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

# region 4. Extract page text
# takes all visible text from the webpage and stores it in text
# # \n puts content into separate lines
text = soup.get_text("\n")
# endregion

# region 5. Find event lines
# This pattern searches for: dd.mm.yyyy
# \d{2} searches for two digits (day/month)
# \ . searches for a dot
# \d{4} searches for four digits (year)
# \s+ matches one or more spaces
# (.*) captures the rest of the text (event name)
matches = re.findall(r"(\d{2}\.\d{2}\.\d{4})\s+(.*)", text)
# example match: 09.05.2026 Ritma skrējiens 2026 Liepāja, gets stored as
# date = 09.05.2026
# line = Ritma skrējiens 2026 Liepāja

rows = []
# store all found events
for date, line in matches:
    rows.append([date, line])
# endregion

# region 6. Save the filtered rows to CSV
# temporarily (with) open or create events.csv 
# write/overwrite (w) file
# prevents blank lines (newline="")
# handles special latvian characters (encoding="utf-8")
# write in new variable file (as file)
with open("events.csv", "w", newline="", encoding="utf-8") as file:
    # creates CSV writer object and say where to write
    writer = csv.writer(file)
    # write one (header) row
    writer.writerow(["date", "event"])
    # write multiple rows from filtered list
    writer.writerows(rows)

print(f"Saved {len(rows)} events to events.csv")
# endregion