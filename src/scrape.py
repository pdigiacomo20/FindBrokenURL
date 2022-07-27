import pandas as pd
import requests
from bs4 import BeautifulSoup as soup
import re
from PIL import Image
import os
from io import BytesIO

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

def get_hours():
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

def clean_name(name):
    s1 = name.replace(' ','_').replace('?','').replace('\'','').replace('#','')
    s2 = s1.replace('&','and').replace('!','').replace('\n','')
    return s2


def get_images(url, status_code,item_name):

    if(url !=  'NONE' and str(status_code) == '200'):
        r = requests.get(url)
        soup_in = soup(r.text,'html.parser')
        images = soup_in.find_all('img')

        name_ind = 0
        for image in images:
            name = item_name + str(name_ind) + '.png'
            name_ind += 1
            link = image['src']
            failed = False
            if(link[0] != '/'):
                print('Nothing added to link: ' + link)
                try:
                    response = requests.get(link)
                except Exception as e:
                    print(link)
                    print(e)
                    failed = True
                    name_ind -= 1
            else:
                print('Added https: to front: ' + link)
                try:
                    response = requests.get('https:' + link)
                except Exception as e:
                    print(link)
                    print(e)
                    failed = True
                    name_ind -= 1
                    
            if failed == False:
                im_pil = Image.open(BytesIO(response.content))
                im_pil.save(name,'PNG')

        return name_ind
    else:
        return 0
        

'''
        with open(name , 'wb') as f:
            if(link[0] != '/'):
                print('Regular: ' + link)
                im = requests.get(link)
            else:
                print('Added: ' + link)
                im = requests.get('https:' + link)

            f.write(im.content)
            print('Writing: ' + name)

        im_pil = Image.open(name)
        im_pil.save(name_no_ext + '.png','PNG')

        os.remove(name)

'''

'''
if __name__ == '__main__':
    get_images('https://trihealing.com/')
'''

'''
if __name__ == '__main__':
    cols_to_read = ['Name','WebsiteNew','StatusCodeNew']
    #df = pd.read_excel('SJBus.xlsx',engine='openpyxl',usecols=cols_to_read)
    df = pd.read_csv('out2.csv',encoding="ISO-8859-1",usecols=cols_to_read)
'''

if __name__ == '__main__':
    cols_to_read = ['Name','WebsiteNew','StatusCodeNew','Notes']
    #df = pd.read_excel('SJBus.xlsx',engine='openpyxl',usecols=cols_to_read)
    df = pd.read_csv('out2.csv',encoding="ISO-8859-1",usecols=cols_to_read)

    df['CleanName'] = df['Name'].apply(clean_name)
    df['num_images'] = df.apply(lambda row: get_images(row['WebsiteNew'],row['StatusCodeNew'],row['CleanName']), axis=1)
    df.to_csv('out10.csv')