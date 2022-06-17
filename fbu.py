import pandas as pd
import requests

cols_to_read = ['Name','WebsiteNew']
#df = pd.read_excel('SJBus.xlsx',engine='openpyxl',usecols=cols_to_read)
df = pd.read_csv('out.csv',encoding="ISO-8859-1",usecols=cols_to_read)

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


#get_status_code(df.loc[0,'WebsiteNew'])
#get_status_code('https://sanjose-strong.github.io/home/')


df['StatusCodeNew'] = df['WebsiteNew'].apply(get_status_code)

df.to_csv('out2.csv')