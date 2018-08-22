import urllib.request
from html.parser import HTMLParser
import csv
import json

class BloombergParser(HTMLParser):
    def __init__(self, writer):
        super(BloombergParser, self).__init__()
        self.__writer = writer

    def handle_data(self, data):
        idx = data.find('window.__bloomberg__.bootstrapData')
        if idx > 0:
            json_data = data[idx + 37 : -1]
            json_data = json_data[0: json_data.find('};\n')+1]
            json_obj = json.loads(json_data)
            quote = json_obj['quote']
            ticker = quote['id']
            name = quote['longName']
            sector = quote['gicsSector']
            industry = quote['gicsIndustry']
            desc = quote['companyDescription']
            self.__writer.writerow((ticker, name, sector, industry, desc))
            

with open('tickers.csv', 'r') as ticker_file:
    tickers = csv.reader(ticker_file)
    with open('results.csv', 'w', encoding='utf-8') as output_file:
        output = csv.writer(output_file)
        output.writerow(('Ticker', 'Name', 'Sector', 'SubSector', 'Description'))
        parser = BloombergParser(output)
        for row in tickers:
            ticker = row[0]
            url = "https://www.bloomberg.com/quote/" + ticker
            req=urllib.request.Request(url, headers = {'User-Agent': "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:34.0) Gecko/20100101 Firefox/34.0",'Referer': url})
            url_content = urllib.request.urlopen(req, timeout=10).read().decode('UTF-8')
            parser.feed(url_content)

