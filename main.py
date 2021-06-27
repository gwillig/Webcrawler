# Import dependencies
from bs4 import BeautifulSoup
import requests
from urllib.parse import quote
from pprint import pprint
import pandas as pd
from googlesearch import search


def WebCrawler_Google(searchTerm):
    """
    @description:
        Saves google results for the search term in a csv file
    @arg
        - searchTerm (str) e.g.
    :return:
    """
    '#0.Step: Define variables'
    terms = ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9', "#")
    cleaningKey = {f"{x}": "" for x in range(0, 10)}
    cleaningKey["#"] = ""
    cleaningKey["."] = ""
    cleaningKey["|"] = ""
    result = {}
    '#1.Step: Get the first 100 google results for search term'
    for i, j in enumerate(search(searchTerm, tbs="qdr:m9", tld='com', lang='en', num=100, stop=100, pause=2)):
        print(i, ": ", j)
        '#2.Step: Parse the results'
        website = requests.get(j)
        soup = BeautifulSoup(website.text, 'html.parser')
        '#2.1.Step: Get the headers'
        website_containers = soup.findAll(['h1', 'h2'])
        '#2.2.Step: Add the result to a dict'
        for el in website_containers:
            header_raw = el.text
            '#2.3.Step: Check if header start with a number or a #'
            if header_raw.startswith(terms):
                '#.step: Clean input'
                headerSpace = header_raw.translate(
                    str.maketrans(cleaningKey)
                )
                '#2.4.Step: remove training and last space'
                header = headerSpace.strip()
                '2.5.#.Step: Check if key is result'
                if header in result:
                    result[f"{header}"] = result[f"{header}"] + 1
                else:
                    result[f"{header}"] = 1
    '#3.Step: Convert result to dataframe'
    df = pd.DataFrame(list(result.items()), columns=['title', 'amount'])
    '#4.Step: Clean the dataframe'
    '#4.1.Step: Drop all rows which contains one of the following key words'
    avoid = ['Top', 'Trends', 'Conclusion', "Post navigation", "Access denied", 'What happened', 'trends'
                                                                                                 'Meta',
             ' Reach Out to Us ', 'Archives', 'Categories', 'Blog', 'What happened?', 'Comments']
    df_finish = df[~df.title.str.contains('|'.join(avoid))]
    '#5.Step: Save the result as csv file'
    df_finish.to_csv(f"{searchTerm}_result_2021.csv", sep=";", index=False, header=True)


if __name__ == '__main__':
    WebCrawler_Google("top+10+web+develeopement+trends+in+2021")

