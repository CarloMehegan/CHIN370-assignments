import urllib.request

# api call, gets the first 500 pages that link to the "Wuxia page"
url = "https://en.wikipedia.org/w/api.php?action=query&format=json&list=backlinks&formatversion=2&bltitle=Wuxia&blfilterredir=all&bllimit=max"

# open url and save contents
with urllib.request.urlopen(url) as request:
    contents = request.read()

# turn bytes into a string
html_string = contents.decode()

# save json to a txt
with open('wuxia_incoming_links.txt', 'w', encoding='utf8') as wf:
    wf.write(html_string)




# use regex to parse the json, for better readability
import re

# get every page title
results = re.findall(r'\"title\":\"(.+?)\"\},', html_string)

# save results to another txt
with open('wuxia_incoming_links_formatted.txt', 'w', encoding='utf8') as wf:
	for r in results:
		wf.write(r + "\n")