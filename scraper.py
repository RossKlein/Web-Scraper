import requests
import bs4


def search_google(search, num):
    data = []
    for terms in search:

        params = {'q': terms, 'num': num, 'hl': 'en', 'gl': 'us', 'lr': 'lang_en'}
        r = requests.get('https://www.google.com/search', params=params)
        html = r.text
        data.append(html)
    return data


def search_parse(data, excld, incld):

    total_links = []
    ultra_wanted_links = []
    for html in data:

        soup = bs4.BeautifulSoup(html, 'html.parser')
        exclude = ['youtube',
                   'www.google.com/preferences?',
                   'maps.google',
                   'accounts.google',
                   'www.google.com/intl/en_us/policies/privacy/',
                   'www.google.com/intl/en_us/policies/terms/']
        if excld != ['']:
            exclude.extend(excld)

        include = ['www.',
                   'http']

        include_only = []
        if incld != ['']:
            include_only.extend(incld)
        all_links = []

        for link in soup.find_all('a'):
            all_links.append(link.get('href'))
        valid_links = [links for links in all_links if any(incld in links for incld in include)]
        unwanted_links = [links for links in valid_links if any(excld in links for excld in exclude)]
        wanted_links = [x for x in valid_links if x not in unwanted_links]
        if include_only:
            ultra_wanted_links = [x for x in wanted_links if any(incld in x for incld in include_only)]
        else:
            ultra_wanted_links = wanted_links
        cleaned_links = clean_link(ultra_wanted_links)
        total_links.extend(cleaned_links)
    with open('data.html', 'w') as file:
        hyperlink = '<a target="_blank" rel="noopener noreferrer" style="display: block; font-family: arial; color: black" href="{link}">{text}</a>\n'
        file.write('<div style="background-color: rgb(230, 247, 255)">')
        for items in total_links:
            file.write(hyperlink.format(link=items, text=items))
        file.write('</div>')
    print('There are ', len(total_links), ' results')


def clean_link(dirty_link):
    cleaned_link = [x.replace('/url?q=', '') for x in dirty_link]
    extracleaned_link = []
    for links in cleaned_link:
        line_num = links.find('&sa=')
        shortened_link = links[:line_num]
        extracleaned_link.append(shortened_link)
    return extracleaned_link


num = '20'
inp = input("Number of search results (default is 20):")
if inp != '':
    num = inp

search = input("List search terms seperated by commas without spaces inbetween:")
search = search.split(',')
choice = input('Type either only include or exclude terms:')
if choice == 'include':

    include = input("List of terms to include seperated by commas without space inbetween:")
    include = include.split(',')
    exclude = []
elif choice == 'exclude':
    exclude = input('List terms to exclude seperated by commas without spaces inbetween:')
    exclude = exclude.split(',')
    include = []
else:
    include = []
    exclude = []

html = search_google(search, num)
search_parse(html, exclude, include)

input('Press enter to continue . . .\n')
