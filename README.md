# serpapi-wallstreet-analysis
Analyze company business using Google search powered by [SerpApi](http://serpapi.com).

## scripts
### search-company-linked.py
Automated creating a cluster of companies based on their activities.

### search-hedge-fund-holding.py
automated collecting all the hedge funds current holding based on 13F filings.

## TODO
 - [] SEC reports is out of sync with Google. Need to retry on multiple links
 - [] automatic dependenc file
 - [] publish article with back links
 - [] group funds and display the connection using d3.js

# Dependencies
- python3
- libraries
```bash
pip3 install google-search-results
pip3 install beautifulsoup4
pip3 install requests
pip3 install lxml
```