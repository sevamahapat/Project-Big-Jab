# file : myths_facts.py
# Authors : dsanmukh, dishantv, jgala, rkacheri, smahapat
# Purpose : this file aggregates myths and facts from the other files - text and image

# imported by : covid_main.py
# imports : myths_facts_image.py, myths_facts_text.py


import pandas as pd

import myths_facts_image
import myths_facts_text


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
        
def get_maf_data():
    print('Scraping data from images...please wait ~30-45s')
    img_url = myths_facts_image.fetch_image_content()
    myths_ocr, facts_ocr, count_ocr = myths_facts_image.extract_content_ocr(img_url)
    content1, content2 = myths_facts_text.fetch_html_content()
    myths, facts, ind = myths_facts_text.extract_myths_and_facts(content1, content2)
    myths_final = myths + myths_ocr
    facts_final = facts + facts_ocr
    ind_final = len(ind) + count_ocr
    
    return myths_final, facts_final, ind_final


def main():
    print('Scraping data from images...please wait ~30-45s')
    img_url = myths_facts_image.fetch_image_content()
    myths_ocr,facts_ocr,count_ocr=myths_facts_image.extract_content_ocr(img_url)
    content1, content2 = myths_facts_text.fetch_html_content()
    myths, facts, ind = myths_facts_text.extract_myths_and_facts(content1, content2)
    myths_final=myths+myths_ocr
    facts_final=facts+facts_ocr
    ind_final=len(ind)+count_ocr
    df = create_df(ind_final, myths_final, facts_final)
    print_cli(ind_final, myths_final, facts_final)
    


if __name__ == '__main__':
    main()