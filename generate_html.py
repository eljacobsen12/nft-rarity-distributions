"""
Generate HTML from CSV.

@author: EJacobsen
@date: 12/12/2021

"""

import pandas
import codecs

# Append 1 for each Collection.
COLUMNS1 = """  <div class="column">
    <img src="<IMAGE_URL>" alt="<COLLECTION_NAME>" style="width:100%" onclick="openModal();currentSlide(<COLLECTION_ID>)" class="hover-shadow cursor">
  </div>"""

# Append 1 for each Collection.
COLUMNS2 = """
    <div class="mySlides">
      <div class="numbertext"><COLLECTION_ID> / <COLLECTION_TOTAL></div>
      <img src="<IMAGE_URL>" alt="<COLLECTION_NAME>" style="width:100%">
    </div>"""

# Append 1 for each Collection.
COLUMNS3 = """    <div class="column">
      <img class="demo cursor" src="<IMAGE_URL>" alt="<COLLECTION_NAME>" style="width:100%" onclick="currentSlide(<COLLECTION_ID>)">
    </div>"""


CSV = f'C:\\Users\\ejacobsen\\Downloads\\EJacobsen\\crypto_tools\\Convex Labs\\honestnft-shenanigans\\fair_drop\\scatterplots\\image_urls.csv'
urls = pandas.read_csv(CSV)

urlCount = urls.shape[0] #len(urls)
COLS1 = """"""; COLS2 = """"""; COLS3 = """"""

# Loop through CSV of Collections, Create HTML and Add to Template.
i = 0
while i < urlCount:
    c1 = COLUMNS1.replace("<IMAGE_URL>", urls.URL[i])
    c1 = c1.replace("<COLLECTION_NAME>", urls.COLLECTION[i])
    c1 = c1.replace("<COLLECTION_ID>", str(i+1))
    COLS1 += c1

    c2 = COLUMNS2.replace("<IMAGE_URL>", urls.URL[i])
    c2 = c2.replace("<COLLECTION_NAME>", urls.COLLECTION[i])
    c2 = c2.replace("<COLLECTION_ID>", str(i+1))
    c2 = c2.replace("<COLLECTION_TOTAL>", str(urlCount))
    COLS2 += c2

    c3 = COLUMNS3.replace("<IMAGE_URL>", urls.URL[i])
    c3 = c3.replace("<COLLECTION_NAME>", urls.COLLECTION[i])
    c3 = c3.replace("<COLLECTION_ID>", str(i+1))
    COLS3 += c3
    i += 1

HTML_BASE = f'C:\\Users\\ejacobsen\\Downloads\\EJacobsen\\crypto_tools\\Python\\Web3\\nft_rarity_distributions\\backend\\html_template.html'
HTML_SAVE = f'C:\\Users\\ejacobsen\\Downloads\\EJacobsen\\crypto_tools\\Python\\Web3\\nft_rarity_distributions\\backend\\html_output.html'
with open(HTML_BASE, 'r+', encoding='utf-8') as htmlTemplate:
    strHtml = htmlTemplate.read()
    strHtml = strHtml.replace("<REPLACE_WITH_COLUMNS1>", COLS1)
    strHtml = strHtml.replace("<REPLACE_WITH_COLUMNS2>", COLS2)
    strHtml = strHtml.replace("<REPLACE_WITH_COLUMNS3>", COLS3)
    with open(HTML_SAVE, 'w', encoding='utf-8') as htmlSave:
        htmlSave.write(strHtml)
