import requests
import json

url = 'https://{username}:{password}@{shop}.myshopify.com/admin/api/{api_version}/{resource}.json?limit={limit}'
key = ''
pw = ''
shop = 'jcrt'
api_version = '2020-10'
resources = ['products', 'orders']
limit = '250'

def parseLink(link, key, pw):
    link_split = link.split(',')
    for sublink in link_split:
        split = sublink.split(';')
        if len(split) == 2 and 'next' in split[1]:
            new_link = split[0].replace('<', '').replace('>', '').strip()
            credentials = '{username}:{password}@'.format(username=key, password=pw)
            return '{}{}{}'.format(new_link[:8], credentials, new_link[8:])
    return None

def fetchData():
    for resource in resources:
        more_results = True
        next_url = url.format(username=key, password=pw, shop=shop, api_version=api_version, resource=resource, limit=limit)
        file_count = 0
        while more_results:
            response = requests.get(next_url)
            parsed_response = json.loads(response.text)
            if resource not in parsed_response:
                print(parsed_response)
                more_results = False
            else:
                parsed_response = parsed_response[resource]
                print(resource + ' #' + str(file_count) + ': ' + str(len(parsed_response)) + ' objects')
                with open('{}-{}.json'.format(resource, str(file_count)), 'w') as outfile:
                    for row in parsed_response:
                        outfile.write(json.dumps(row))
                        outfile.write('\n')
                if 'Link' in response.headers:
                    file_count += 1
                    next_url = parseLink(response.headers['Link'], key, pw)
                    if next_url is None:
                        more_results = False
                else:
                    more_results = False
    return 0

fetchData()

# products
#     collections?
# orders (only last 60 days, need to request access for more)
    # refunds, included in orders but can be standalone
    # checkouts (abandoned checkouts)
# analytics
# customers?


# __things to consider__
# pagination
# security, PII
# maybe set up reports for each store in Shopify until we get a UI
# cadence of retrieving data... airflow?
    # every hour, pull data from last timestamp?
