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

# split the full page text into separate lines using newline character
lines = text.split("\n")

# create empty list where we will store cleaned lines
clean_lines = []

# loop through each line
for line in lines:
    
    # remove spaces at beginning and end of line
    stripped_line = line.strip()
    
    # check if line is not empty after stripping
    if stripped_line:
        
        # add cleaned line to list
        clean_lines.append(stripped_line)

# replace lines with cleaned version
lines = clean_lines
# endregion

# region 5. Find event lines

# create empty list to store results
rows = []

# loop through lines using index numbers
# we use len(lines) - 1 because we look at the next line (i + 1)
for i in range(len(lines) - 1):

    # get current line
    current_line = lines[i]

    # check if current line is a date (dd.mm.yyyy format)
    if re.fullmatch(r"\d{2}\.\d{2}\.\d{4}", current_line):

        # assume next line contains event name
        event_line = lines[i + 1]

        # sometimes the next line is "INFO"
        # in that case, actual event name is on the next line after that
        if event_line == "INFO":

            # check that we don't go out of list range
            if i + 2 < len(lines):
                event_line = lines[i + 2]

        # add date and event name to results list
        rows.append([current_line, event_line])

# endregion

# region 6. Save the filtered rows to CSV
# with to temporarily open or create events.csv 
# "w" towrite/overwrite file
# newline="" to prevents blank lines 
# "utf-8-sig" to handle special latvian characters
# as file to write in new variable file 
with open("events.csv", "w", newline="", encoding="utf-8-sig") as file:
    # creates CSV writer object and say where to write
    # delimiter=";" to meet Excel expectation in EU for ;
    # quoting=csv.QUOTE_ALL to  prevent Excel from splitting event names that contain commas
    writer = csv.writer(file, delimiter=";", quoting=csv.QUOTE_ALL)
    # write one (header) row
    writer.writerow(["date", "event"])
    # write all extracted rows
    writer.writerows(rows)

# print confirmation message
print(f"Saved {len(rows)} events to events.csv")
# endregion