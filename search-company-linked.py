# Automated creating a cluster of companies based on their activities
#  The algorithm search starts with one company,
#   then multiple search on Google allows to collect all the companies linked
from serpapi import GoogleSearch
import os
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


# group weeds stock
# q = "Canopy Growth Corporation"
# group auto industry
q = "tesla"

# store the name of the companies linked based on Google
linked = []
# initial a queue to run the search by batch (google shows only few companies per request)
queue = search(q, linked)
while len(queue) > 0:
  for q in queue:
    queue = search(q, linked)

print(">> %s" % q)
print("---")
pp.pprint(linked)

