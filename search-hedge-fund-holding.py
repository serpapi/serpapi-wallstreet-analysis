# Automated collecting all the hedge funds current holding based on 13F filings.
#
# Algorithm:
#  - Collect all the hedge fund names.
#  - Search SEC filing on Google
#  - Download the filing
#
from serpapi import GoogleSearch
from bs4 import BeautifulSoup
from requests import get
import os
import glob
import sys
import pprint
pp = pprint.PrettyPrinter(indent=4)

def search(q, linked):
  print("search: %s" % q)
  # run search
  parameter = {
    "q": q,
    "api_key": os.getenv("API_KEY")
  }
  client = GoogleSearch(parameter)
  results = client.get_dict()

  # basic error handling
  if "error" in results:
    print("ERROR: " + results["error"])
    sys.exit(1)

  # analyze results
  queue = []
  if not 'knowledge_graph' in results:
    return queue
  for link in results['knowledge_graph']['people_also_search_for']:
    name = link['name'].replace('.', '')
    if name in linked:
      continue
    linked.append(name)
    queue.append(name)
  return queue

# list of the edge fund
linked = []
q = "Melvin capital"
linked.append(q)
cluster = search(q, linked)
while len(cluster) > 0:
  for q in cluster:
    cluster = search(q, linked)
print("company linked to: " + q)
pp.pprint(linked)

# download latest SEC report: F13 as XML if available
links = []
for name in linked:
  # xml file name
  fn = name.replace(' ', '_') + '_report.xml'
  if os.path.exists(fn):
    print("skip: " + fn + " already downloaded")
    continue

  print("search 13F: " + name)
  parameter = {
    "q": name + " 13f-hr site:sec.gov",
    "api_key": os.getenv("API_KEY")
  }
  client = GoogleSearch(parameter)
  results = client.get_dict()
  holding_link = None
  if not 'organic_results' in results:
    print("FAIL: no results found for " + q)
    break

  for result in results["organic_results"]:
    if result["link"][-3:] == "xml":
      holding_link = result["link"].replace('primary_doc.xml', 'infotable.xml')
      break
  if holding_link == None:
    print("FAIL: no SEC report for: " + name)
    break

  print("download: " + holding_link)
  with open(fn, "wb") as file:
    # get request
    response = get(holding_link)
    # write to file
    file.write(response.content)

# parse report
with open("hedge_fund_report.csv", "w") as f:
  suffix = '_report.xml'
  for path in glob.glob("*" + suffix):
    soup = BeautifulSoup(open(path), "lxml")
    tables = soup.find_all('table')
    if len(tables) < 3:
      print("FAIL: invalid report: " + path)
      continue

    data = tables[-1]
    # print(data.get('summary'))
    for row in data.find_all('tr')[3:]: # 3:
      cells = row.find_all('td')
      name = cells[0].string 
      value = int(cells[3].string.replace(',', '')) * 1000
      shares = int(cells[4].string.replace(',', ''))
      position = cells[6].string.lower().strip()
      if len(position) == 0:
        position = "own"
      price_per_share = round(value / shares, 2)
      value_b = round(value / 1000000, 3)
      q = os.path.basename(path).replace(suffix, '').lower()
      print("%s,%sm$,%s$,%s,%s" % (name, value_b, price_per_share, position, q), file=f)
    print("ok: " + path)
  #print(soup.prettify())

print("---")


