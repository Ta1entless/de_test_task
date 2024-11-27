import requests
import psycopg2

url = "https://restcountries.com/v3.1/all?fields=cca2,cca3,cioc,name,capital,region,subregion,languages,area,population"

response = requests.get(url, timeout=10)

if response:
    try:
        countries = response.json()

        conn = psycopg2.connect(
            dbname="countries_db",
            user="user",
            password="password",
            host="localhost",
            port="5432"
        )
        cursor = conn.cursor()

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS countries (
            cca2 TEXT PRIMARY KEY,
            cca3 TEXT,
            cioc TEXT,
            name_common TEXT,
            name_official TEXT,
            capital TEXT,
            region TEXT,
            subregion TEXT,
            languages TEXT[],
            area REAL,
            population INTEGER
        )
        ''')

        for country in countries:
            cca2 = country.get('cca2', '')
            cca3 = country.get('cca3', '')
            cioc = country.get('cioc', '')
            name_common = country.get('name', {}).get('common', '')
            name_official = country.get('name', {}).get('official', '')
            capital = ', '.join(country.get('capital', []))
            region = country.get('region', '')
            subregion = country.get('subregion', '')
            languages = list(country.get('languages', {}).values())
            area = country.get('area', 0)
            population = country.get('population', 0)

            cursor.execute('''
            INSERT INTO countries (cca2, cca3, cioc, name_common, name_official, capital, region, subregion, languages, area, population)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (cca2) DO UPDATE SET
                cca3 = EXCLUDED.cca3,
                cioc = EXCLUDED.cioc,
                name_common = EXCLUDED.name_common,
                name_official = EXCLUDED.name_official,
                capital = EXCLUDED.capital,
                region = EXCLUDED.region,
                subregion = EXCLUDED.subregion,
                languages = EXCLUDED.languages,
                area = EXCLUDED.area,
                population = EXCLUDED.population
            ''', (cca2, cca3, cioc, name_common, name_official, capital, region, subregion, languages, area, population))

        conn.commit()
        cursor.close()
        conn.close()

    except requests.exceptions.JSONDecodeError as e:
        print("failed to decode JSON response:", e)
else:
    print(f"failed to retrieve data: {response.status_code}")
