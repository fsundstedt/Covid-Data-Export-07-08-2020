import numpy as np
import pandas as pd
import urllib, urllib.request, json

url = 'https://corona-api.com/countries'

response = urllib.request.urlopen(url)

data = json.loads(response.read())

country_data_raw = data['data']

date = (country_data_raw[0]['updated_at'])[0:10]

country_data = []

for country in country_data_raw:
    single_country = {}
    single_country['name'] = country['name']
    single_country['population'] = country['population']
    single_country['deaths'] = country['latest_data']['deaths']
    single_country['total_cases'] = country['latest_data']['confirmed']

    if str(country['latest_data']['calculated']['death_rate'])[0].isdigit():
        single_country['death_rate_%'] = round((country['latest_data']['calculated']['death_rate']), 2)
    else:
        single_country['death_rate_%'] = 'N/A'

    if str(country['latest_data']['confirmed'])[0].isdigit() and str(country['population'])[0].isdigit():
        single_country['population_infected_rate_%'] = round((country['latest_data']['confirmed'] / country['population'] * 100), 3)
    else:
        single_country['population_infected_rate_%'] = 'N/A'

    single_country['date_updated'] = country['updated_at']
    country_data.append(single_country)

df = pd.DataFrame(country_data)

file_name = './covid_data_' + date + '.xlsx'

df.to_excel(file_name)
