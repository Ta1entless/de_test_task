import requests
import csv

url = "https://restcountries.com/v3.1/all?fields=cca2,cca3,cioc,name,capital,region,subregion,languages,area,population"

response = requests.get(url, timeout=10)

if response:
    try:
        countries = response.json()

        with open('result.csv', mode='w') as file:
            writer = csv.writer(file)

            headers = ['cca2', 'cca3', 'cioc', 'name.common', 'name.official', 'capital',
                       'region', 'subregion', 'language', 'area', 'population']
            writer.writerow(headers)

            for country in countries:
                cca2 = country.get('cca2', '')
                cca3 = country.get('cca3', '')
                cioc = country.get('cioc', '')
                name_common = country.get('name', {}).get('common', '')
                name_official = country.get('name', {}).get('official', '')
                capital = ', '.join(country.get('capital', []))
                region = country.get('region', '')
                subregion = country.get('subregion', '')
                languages = country.get('languages', {})
                area = country.get('area', 0)
                population = country.get('population', 0)

                for language in languages.values():
                    writer.writerow([cca2, cca3, cioc, name_common, name_official, capital,
                                     region, subregion, language, area, population])
    except requests.exceptions.JSONDecodeError as e:
        print("failed to decode JSON response:", e)
else:
    print(f"failed to retrieve data: {response.status_code}")

