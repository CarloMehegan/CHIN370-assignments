import urllib.request
from bs4 import BeautifulSoup

# url for the Wuxia page in Wikipedia
url = "https://en.wikipedia.org/wiki/Wuxia"

# 
with urllib.request.urlopen(url) as request:
    contents = request.read()

# turn bytes into a string
html_string = contents.decode()

# initialize beautifulsoup to parse the html
soup = BeautifulSoup(html_string, "html.parser")

# get all outgoing links/anchor tags in the html
links = soup.find_all('a')
link_string = ""
for link in links:
    link_text = link.string
    link_url = link.get("href")
    link_string.append(f"{link_text}: {link_url}\n")

# save results to file
with open('wuxia_outgoing_links.txt', 'w', encoding='utf8') as wf:
    wf.write(link_string)