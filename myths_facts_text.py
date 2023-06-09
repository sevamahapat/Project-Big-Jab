# file : myths_facts_text.py
# Authors : dsanmukh, dishantv, jgala, rkacheri, smahapat
# Purpose : this file extract

# imported by : myths_facts.py


import pandas as pd
import requests
from bs4 import BeautifulSoup


def fetch_html_content():
    url = "https://www.cdc.gov/coronavirus/2019-ncov/vaccines/facts.html"

    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")
    content1 = soup.find_all("h2", class_="card-title mb-1 h4 text-left")
    content2 = soup.find_all("div", class_="fs11")
    # content3 = soup.find_all("p")
    return content1, content2


def extract_myths_and_facts(content1, content2):
    myths = []
    facts = []
    ind = []
    count = 1
    for myth, fact, in zip(content1, content2):
        myth = myth.text
        fact = fact.text

        myths.append(myth[6:])
        facts.append(fact[6:])
        ind.append(count)
        count += 1
    return myths, facts, ind


def create_df(ind, myths, facts):
    my_dict = {"Sr. No.": ind, "Myths": myths, "Facts": facts}
    df = pd.DataFrame(my_dict, columns=['Sr. No.', "Myths", "Facts"])
    df.set_index("Sr. No.", inplace=True)
    return df


def convert_to_excel(df):
    df.to_excel("cleaned_data.xlsx")

def print_cli(ind, myths, facts):
    for i in range(len(myths)):
        print(f'--------------Myth Buster {i+1}--------------')
        print(f'''Myth: {myths[i]}
Fact: {facts[i]}''')


def main():
    content1, content2 = fetch_html_content()
    myths, facts, ind = extract_myths_and_facts(content1, content2)
    df = create_df(ind, myths, facts)
    print_cli(ind, myths, facts)


if __name__ == '__main__':
    main()
