import requests
from bs4 import BeautifulSoup as bs
import csv
import json
import random

PROXY = 'http://194.224.192.226:8080'


class Kickstarter:

    def parse(self, page: int, sort: str):
        seed = random.randint(0, 9999999)

        url = f'https://www.kickstarter.com/discover/advanced?sort={sort}&seed={seed}&page={page}'
        r = requests.get(url, proxies={'http': PROXY, 'https': PROXY})
        html_page = r.text

        soup = bs(html_page, 'html.parser')

        count_of_projects = int(soup.find('h3').text[10:-11].replace(',', ''))

        all_projects = soup.find_all('div', class_='js-react-proj-card grid-col-12 grid-col-6-sm grid-col-4-lg')

        for project in all_projects:
            str_data = str(project)
            data_project = str_data.find('data-project') + 14
            is_disliked = str_data.find('is_disliked') - 2

            preparing_data = str_data[data_project:is_disliked].replace("'", '') + '}'
            try:
                data_json = json.loads(preparing_data)
            except json.decoder.JSONDecodeError:
                continue
            name_project = data_json['name']
            goal_project = data_json['goal']
            name_region = data_json['location']['displayable_name']
            country = data_json['country']
            url_project = data_json['urls']['web']['project']
            sort = data_json['category']['name']

            all_values = {
                'name': name_project, 'goal': goal_project, 'country': country, 'region': name_region,
                'category': sort,
                'url': url_project
            }
            print(all_values)



kik = Kickstarter()
for x in range(1, 10):
    kik.parse(x, 'popularity')
