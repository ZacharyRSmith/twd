from keys import BING_API_KEY
import json
import urllib, urllib2

def main():
    print "Please enter in your search terms..."
    search_terms = raw_input("> ")
    if not search_terms:
        print "Come on! Give me something to work with!"
        main()

    rslts = run_query(search_terms)
    for i in range(10):
        print i + 1, "\tTitle: " + rslts[i]['title'], "\t\t" + rslts[i]['link']

def run_query(search_terms):
    root_url = 'https://api.datamarket.azure.com/Bing/Search/v1/'
    source   = 'Web'

    results_per_page = 10
    offset           = 0

    query = "'{0}'".format(search_terms)
    query = urllib.quote(query)

    search_url = "{0}{1}?$format=json&$top={2}&$skip={3}&Query={4}".format(
        root_url,
        source,
        results_per_page,
        offset,
        query
    )

    username = ''

    password_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
    password_mgr.add_password(None, search_url, username, BING_API_KEY)

    results = []

    try:
        handler = urllib2.HTTPBasicAuthHandler(password_mgr)
        opener  = urllib2.build_opener(handler)
        urllib2.install_opener(opener)

        response = urllib2.urlopen(search_url).read()

        json_response = json.loads(response)

        for result in json_response['d']['results']:
            results.append({
                    'title': result['Title'],
                    'link': result['Url'],
                    'summary': result['Description']
            })
    except urllib2.URLError, e:
        print "Error when querying the Bing API: ", e

    return results

if __name__ == '__main__':
    main()