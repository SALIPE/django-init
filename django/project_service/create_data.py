import csv
import json


def get_state_acronym(state_name: str) -> str:
    estados = {
        "Acre": "AC",
        "Alagoas": "AL",
        "Amapá": "AP",
        "Amazonas": "AM",
        "Bahia": "BA",
        "Ceará": "CE",
        "Distrito Federal": "DF",
        "Espírito Santo": "ES",
        "Goiás": "GO",
        "Maranhão": "MA",
        "Mato Grosso": "MT",
        "Mato Grosso Do Sul": "MS",
        "Mato Grosso do Sul": "MS",
        "Minas Gerais": "MG",
        "Pará": "PA",
        "Paraíba": "PB",
        "Paraná": "PR",
        "Pernambuco": "PE",
        "Piauí": "PI",
        "Rio De Janeiro": "RJ",
        "Rio de Janeiro": "RJ",
        "Rio Grande Do Norte": "RN",
        "Rio Grande do Norte": "RN",
        "Rio Grande Do Sul": "RS",
        "Rio Grande do Sul": "RS",
        "Rondônia": "RO",
        "Roraima": "RR",
        "Santa Catarina": "SC",
        "São Paulo": "SP",
        "Sao Paulo": "SP",
        "Sergipe": "SE",
        "Tocantins": "TO"
    }
    
    key = state_name.strip().title()
    
    if key in estados:
        return estados[key]
    
    raise ValueError(f"Estado '{state_name}' não encontrado no mapeamento.")
    


def generate_fixture(csv_file, output_file, app_label):
    countries = {}
    states = {}
    cities = []

    country_pk_counter = 1
    state_pk_counter = 1
    city_pk_counter = 1

    with open(csv_file, mode="r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            country_code = row["iso2"].strip()
            country_name = row["country"].strip()
            state_name = row["admin"].strip()
            state_acronym = get_state_acronym(state_name)
            city_name = row["city"].strip()

            if country_code not in countries:
                countries[country_code] = {
                    "model": f"{app_label}.country",
                    "pk": country_pk_counter,
                    "fields": {
                        "name": country_name,
                        "code": country_code
                    }
                }
                country_pk_counter += 1

            state_key = (country_code, state_acronym)
            if state_key not in states:
                states[state_key] = {
                    "model": f"{app_label}.state",
                    "pk": state_pk_counter,
                    "fields": {
                        "name": state_name,
                        "acronym": state_acronym,
                        "country": countries[country_code]["pk"]
                    }
                }
                state_pk_counter += 1

            cities.append({
                "model": f"{app_label}.city",
                "pk": city_pk_counter,
                "fields": {
                    "name": city_name,
                    "state": states[state_key]["pk"]
                }
            })
            city_pk_counter += 1

    # Concatena todos os registros numa lista
    data = []
    for country in sorted(countries.values(), key=lambda x: x["pk"]):
        data.append(country)
    for state in sorted(states.values(), key=lambda x: x["pk"]):
        data.append(state)
    for city in sorted(cities, key=lambda x: x["pk"]):
        data.append(city)

    # Grava o JSON formatado no arquivo de saída
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    csv_file = "br.csv"
    output_file = "address_data.json"
    app_label = "users"
    generate_fixture(csv_file, output_file, app_label)
