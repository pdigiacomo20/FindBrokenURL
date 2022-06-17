import pandas as pd
import requests
from bs4 import BeautifulSoup as soup
import re


cols_to_read = ['Name','WebsiteNew','StatusCodeNew']
#df = pd.read_excel('SJBus.xlsx',engine='openpyxl',usecols=cols_to_read)
df = pd.read_csv('out2.csv',encoding="ISO-8859-1",usecols=cols_to_read)

def get_status_code(url):
    '''
    response = requests.get(url)
    header = response.headers
    '''
    if(url == 'NONE'):
        return -2

    try:
        header = requests.head(url,verify=True)
        return header.status_code
    except requests.exceptions.SSLError:
        header = requests.head(url,verify=False)
        return header.status_code
    except:
        return -1

with open('out9.txt', "w", encoding="utf-8") as f:
    df_linkgood = df[df['StatusCodeNew'] == 200]
    for index,row in df_linkgood.iterrows():
        link = row.loc['WebsiteNew']
        name = row.loc['Name']

        htmltext = requests.get(link).text

        doc = soup(htmltext,'html.parser')

        #all_finds = doc.find_all('p',string=re.compile(r'pm'))

        pat = r'(\d{1,2})(:\d{1,2})*(\s)*(am|pm|Am|Pm|AM|PM)*(\s)*[-toTO]+(\s)*(\d{1,2})(:\d{1,2})*(\s)*(am|pm|Am|Pm|AM|PM)+'
        all_finds = doc(text=re.compile(pat))

        find_parents = list(map(lambda x: x.parent,all_finds))
        #all_finds = doc.find_all('p')

        #all_finds = re.findall(r'.{2}pm.{2}',htmltext)
        counter = 0

        for item_ind in range(len(all_finds)):
            f.write(f'{counter}#############710##################\n')
            f.write(f'{name}######################\n')
            f.write(all_finds[item_ind]+'\n')
            f.write(str(find_parents[item_ind])+'\n')
            counter += 1

    '''
    for item in all_finds:
        print(item)
        print('########################################################')
    '''

    #print(doc.find_all('a'))
    #print(doc.prettify())