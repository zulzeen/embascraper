import csv

from bs4 import BeautifulSoup


def extract_embassies():
    source_file = "./inChina_embassies.html"
    with open(source_file, 'r') as html:
        soup = BeautifulSoup(html, "html.parser")
    return [line.text.strip().split("[")[0] for line in soup.find_all("li")]


def extract_consulates():
    source_file = "./inChina_consulates.html"
    consulates = []
    with open(source_file, 'r') as html:

        soup = BeautifulSoup(html, "html.parser")
        for city in soup.find_all("h3"):
            countries = [item.text.strip().split("(")[0].split('[')[0]
                          for item
                          in city.find_next_sibling().find_all('li')]
            if not countries:
                countries = [item.text.strip().split("(")[0].split('[')[0]
                              for item
                              in city.find_next_sibling("div").find_all('li')]
            consulates += [(city.text.split('[')[0], country) for country in countries]
    return consulates


def extract_chinese_missions():
    with open('./ofChina_current.html', 'r') as source_file:
        soup = BeautifulSoup(source_file, 'html.parser')

    missions = []
    for continent in soup.find_all('h3'):
        name = continent.text.replace('[edit]', '')
        current_country = ''
        for mission in continent.find_next_sibling('table').find_all('tr')[1:]:
            if country := mission.find('th'):
                current_country = country.text.strip()

            location, mission_type = [t.text.strip() for t in mission.find_all('td')]
            missions.append((name, current_country, mission_type, location))
    return missions


if __name__ == "__main__":
    # source: https://en.wikipedia.org/wiki/List_of_diplomatic_missions_in_China
    with open("./inChina.csv", "w") as output_file:
        csv_output = csv.writer(output_file)
        csv_output.writerow(('city', 'mission_type', 'country'))

        for embassy in extract_embassies():
            csv_output.writerow(('Beijing', 'Embassy', embassy))

        for consulate in extract_consulates():
            csv_output.writerow((consulate[0], 'Consulate', consulate[1]))

    # source: https://en.wikipedia.org/wiki/List_of_diplomatic_missions_of_China
    with open("./ofChina.csv", "w") as output_file:
        csv_output = csv.writer(output_file)
        csv_output.writerow(('continent', 'country', 'mission_type', 'city'))

        for entry in extract_chinese_missions():
            csv_output.writerow(entry)