import numpy as np
import pandas as pd
import urllib, urllib.request, json
from xlsxwriter.utility import xl_rowcol_to_cell

url = 'https://corona-api.com/countries'

response = urllib.request.urlopen(url)

data = json.loads(response.read())

country_data_raw = data['data']

date = (country_data_raw[0]['updated_at'])[0:10]

country_data = []

for country in country_data_raw:
    single_country = {}
    single_country['name'] = country['name']
    if single_country['name'] == 'USA':
        single_country['population'] = 329964713
    else:
        single_country['population'] = country['population']

    single_country['deaths'] = country['latest_data']['deaths']
    single_country['total_cases'] = country['latest_data']['confirmed']

    if str(country['latest_data']['calculated']['death_rate'])[0].isdigit():
        single_country['infected_death_rate_%'] = round((country['latest_data']['calculated']['death_rate']), 2)
    else:
        single_country['infected_death_rate_%'] = 'N/A'

    if str(country['latest_data']['confirmed'])[0].isdigit() and str(single_country['population'])[0].isdigit():
        single_country['population_infected_rate_%'] = round((country['latest_data']['confirmed'] / single_country['population'] * 100), 3)
    else:
        single_country['population_infected_rate_%'] = 'N/A'

    if str(country['latest_data']['deaths'])[0].isdigit() and str(single_country['population'])[0].isdigit():
        single_country['population_death_rate_%'] = round((country['latest_data']['deaths'] / single_country['population'] * 100), 4)
    else:
        single_country['population_death_rate_%'] = 'N/A'

    single_country['date_updated'] = country['updated_at']
    country_data.append(single_country)

df = pd.DataFrame(country_data)

file_name = './data_sets/covid_data_' + date + '.xlsx'

writer = pd.ExcelWriter(file_name, engine='xlsxwriter')
df.to_excel(writer, index=True, sheet_name='data')

workbook = writer.book
worksheet = writer.sheets['data']
worksheet.set_column('B:B', 30)
worksheet.set_column('C:H', 15)
worksheet.set_column('I:I', 23)

writer.save()