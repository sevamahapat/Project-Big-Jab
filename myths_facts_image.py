# file : myths_facts_image.py
# Authors : dsanmukh, dishantv, jgala, rkacheri, smahapat
# Purpose : this file scrapes images from the url and extracts text from the images

# imported by : myths_facts.py

import io

import pytesseract
from PIL import Image
import requests
from bs4 import BeautifulSoup
import pandas as pd


my_config = r"--psm 4 --oem 3"

# for windows, add the path to tesseract.exe file as shown in README
# for mac, add the path to tesseract as shown in README
pytesseract.pytesseract.tesseract_cmd = "/opt/local/bin/tesseract"


def fetch_image_content():
    url = "https://www.emro.who.int/health-topics/corona-virus/covid-19-vaccine-myth-busters.html"
    r = requests.get(url)
    urls = []
    soup = BeautifulSoup(r.content, "html.parser")
    for a in soup.find_all('a'):
        if a.img:
            st1 = "https://www.emro.who.int"
            st2 = st1 + a.img['src']
            urls.append(st2)
    img_url = urls[5:]
    return img_url


# cropping image to get a more accurate text extraction
def extract_content_ocr(img_url):
    count = 1
    count1 = 1
    myths = []
    facts = []

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

    for i in img_url:
        r = requests.get(i, headers=headers)
        img = Image.open(io.BytesIO(r.content))
        if count == 13:
            img = img.crop((350, 127, 750, 350))
            fact = pytesseract.image_to_string(img, config=my_config)
            fact = fact.replace("\n", ' ')
            facts.append(fact.strip())

        elif count > 6 and count != 13:
            img = img.crop((360, 90, 750, 360))
            fact = pytesseract.image_to_string(img, config=my_config)
            fact = fact.replace("\n", ' ')
            facts.append(fact.strip())

        elif count != 13:
            if count == 4:
                img = img.crop((375, 170, 750, 300))
                fact = pytesseract.image_to_string(img, config=r"--psm 4 --oem 3")
                fact = fact.replace("\n", " ")
                facts.append(fact.strip())

            else:
                img = img.crop((375, 185, 750, 300))
                fact = pytesseract.image_to_string(img, config=r"--psm 4 --oem 3")
                fact = fact.replace("\n", " ")
                facts.append(fact.strip())

        count += 1

    for i in img_url:
        r = requests.get(i, headers=headers)
        img = Image.open(io.BytesIO(r.content))

        if count1 == 13:
            img = img.crop((0, 127, 350, 350))
            myth = pytesseract.image_to_string(img, config=my_config)
            myth = myth.replace("\n", ' ')
            myths.append(myth.strip())

        elif count1 > 6 and count1 != 13:
            img = img.crop((0, 110, 375, 360))
            myth = pytesseract.image_to_string(img, config=my_config)
            myth = myth.replace("|", "I")
            myth = myth.replace("\n", " ")
            myths.append(myth.strip())

        elif count1 != 13:
            img = img.crop((0, 200, 375, 300))
            myth = pytesseract.image_to_string(img, config=my_config)
            myth = myth.replace("|", "I")
            myth = myth.replace("\n", " ")
            myths.append(myth.strip())

        count1 += 1
    return myths, facts, count


def ocr_content_to_df(myths, facts, count):
    my_dict = {"Sr. No.": range(1, count), "Myths": myths, "Facts": facts}
    ocr_df = pd.DataFrame(my_dict, columns=['Sr. No.', "Myths", "Facts"])
    ocr_df.set_index("Sr. No.", inplace=True)
    return ocr_df


def ocr_df_to_excel(ocr_df):
    ocr_df.to_excel("cleaned_data_ocr.xlsx")


def print_cli(count, myths, facts):
    for i in range(len(myths)):
        print(f'--------------Myth Buster {i + 1}--------------')
        print(f'''Myth: {myths[i]}
Fact: {facts[i]}''')


def main():
    img_url = fetch_image_content()
    myths, facts, count = extract_content_ocr(img_url)
    ocr_df = ocr_content_to_df(myths, facts, count)
    print_cli(count, myths, facts)


if __name__ == '__main__':
    main()
