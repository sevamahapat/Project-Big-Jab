# file : stats_visualization.py
# Authors : dsanmukh, dishantv, jgala, rkacheri, smahapat
# Purpose : using csv data source to clean, process, analyze and visualize COVID data

# imported by : covid_main.py

import time

import plotly.express as px
import plotly.io as pio
import pandas as pd

pio.renderers.default = 'png'

df = pd.read_csv("./country_vaccinations.csv")

def fetch_csv():
    from selenium import webdriver

    driver = webdriver.Chrome()

    url = "https://ourworldindata.org/covid-vaccinations"

    driver.get(url)
    time.sleep(1)

    download_button = driver.find_element(by='xpath', value="/html/body/main/article/div[3]/div[2]/div/div/section["
                                                            "1]/div[2]/div/figure/div/div[3]/div/div[4]/div["
                                                            "2]/nav/ul/li[5]/a")
    download_button.click()

    actual_download = driver.find_element(by='xpath', value='/html/body/main/article/div[3]/div[2]/div/div/section['
                                                            '1]/div[2]/div/figure/div/div[3]/div/div[5]/div/div['
                                                            '2]/div/button/div[1]/h3')
    actual_download.click()


def about_df():
    print(df.columns)
    print(df.info())
    print(df.describe())


def fetch_dashboard_data():
    total_doses_vax = df['total_vaccinations'].sum()
    single_dose_vax = df['people_vaccinated'].sum()
    double_dose_vax = df['people_fully_vaccinated'].sum()

    return single_dose_vax, double_dose_vax, total_doses_vax


def getDfA():
    dfA = pd.read_csv('./country_vaccinations_by_manufacturer.csv')
    return dfA


# 1
def daily_vaccinations_usa(countryCode):
    dfA = df[df['iso_code'] == countryCode]
    liste = list(set(dfA['country']))

    fig = px.scatter(x=dfA['date'], y=dfA['daily_vaccinations'], title='Country {}'.format(liste[0]))

    x = fig.show()
    x = fig.write_image('img1.png')


# 2
def daily_vaccinations_by_country_new():
    df_last_date = df[df['date'] == "2022-02-04"]  # last date
    # ddf_last_datef = df[['country', 'daily_vaccinations']].sort_values(by="daily_vaccinations", ascending=False)
    fig = px.treemap(df_last_date, path=[px.Constant('daily_vaccinations'), 'country'], values="daily_vaccinations",
                     hover_data=['country'])
    x = fig.show()
    x = fig.write_image('img2.png')


# 3
def daily_vaccinations_by_country_old():
    fig = px.treemap(df, path=[px.Constant('daily_vaccinations'), 'country'], values='daily_vaccinations',
                     hover_data=['country'])
    x = fig.show()
    x = fig.write_image('img3.png')


# 4
def people_vaccinated_per_hundred():
    df_new = df[df['date'] == '2022-02-04']
    df_new = df_new.sort_values(by='people_vaccinated_per_hundred', ascending=False)

    fig = px.bar(df_new.head(10), x='country', y='people_vaccinated_per_hundred',
                 title='People Vaccinated per Hundred for the Date 2022-02-04')
    x = fig.show()
    x = fig.write_image('img4.png')

    df_new = df_new.sort_values(by='people_fully_vaccinated_per_hundred', ascending=False)

    fig = px.bar(df_new.head(10), x='country', y='people_fully_vaccinated_per_hundred',
                 title='People Fully Vaccinated per Hundred for the Date 2022-02-04')

    x = fig.show()
    x = fig.write_image('img5.png')


# 5
def most_used_vaccine(location):

    dfA = getDfA()

    dfA = dfA[dfA['location'] == location]

    fig = px.bar(x=dfA['vaccine'], y=dfA['total_vaccinations'],
                 title='Most Used Vaccine for {}'.format(location))

    x = fig.show()
    x = fig.write_image('img6.png')


# 6
def most_used_vaccines_world():
    total = dfA.groupby('vaccine').sum()

    fig = px.bar(x=total.index, y=total['total_vaccinations'],
                 title='Most Used Vaccine in the World')

    x = fig.show()
    x = fig.write_image('img7.png')


# 7
def vaccine_comparison_europe():
    dfA = getDfA()
    europeanUnion = dfA[dfA['location'] == 'European Union']

    fig = px.line(europeanUnion, x="date", y="total_vaccinations", color='vaccine', title='European Union Vaccination')
    x = fig.show()
    x = fig.write_image('img8.png')


def main():
    daily_vaccinations_usa('USA')  # 1
    daily_vaccinations_by_country_new()  # 2
    daily_vaccinations_by_country_old()  # 3
    people_vaccinated_per_hundred()  # 4
    most_used_vaccine('United States')  # 5
    most_used_vaccines_world()  # 6
    vaccine_comparison_europe()  # 7


dfA = getDfA()
dfA = dfA[dfA.date == '2022-02-04']
dfA.head()

if __name__ == '__main__':
    main()

