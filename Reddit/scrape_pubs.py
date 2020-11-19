import requests
import pandas as pd
from bs4 import BeautifulSoup
from time import sleep
import sys

sys.setrecursionlimit(10000)

df = pd.read_csv('top_and_controversial_lg_wpub.csv')

data = []

for idx, row in df.iterrows():
    print(f"{idx}/{df.shape[0]}")
    url = row.url 

    if data:
        if row.publisher == data[-1].publisher:
            sleep(1)
    
    try:
        page = requests.get(url, timeout=5)
        soup = BeautifulSoup(page.text, 'html.parser')
    except Exception as e:
        print(e)
        print(row)
        continue
        
    
    
#     print(page.status_code)
    if page.status_code == 200:
        try:
            # row["soup"] = soup  # so I can stop scraping the damn thing
            row["p"] = soup.find('p').getText()
            
            if row.title in soup.title.text:
#                 print("match title", soup.title.text)
                row["titles_match"] = True
            elif row.title in soup.h1:
#                 print(soup.h1.string)
                # check the h1 tag
                row["titles_match"] = True
            else:
#                 print(f"no match. Row title: {row.title} \nSoup title: {soup.title.text} \nH1: {soup.h1}")
                
                row["titles_match"] = False
            data.append(row)
        except Exception as e:
            print(e)
#         print("######")



new_df = pd.DataFrame(data, columns=list(df.columns).extend(["soup","p","titles_match"]))

new_df.to_pickle('top_and_controversial.pkl')
