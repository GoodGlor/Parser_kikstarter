import requests
from bs4 import BeautifulSoup as bs
import json
import random
import csv


class Kickstarter:

    def get_proxies(self) -> list:
        with open('valid_proxies.txt', 'r') as file:
            content = file.readlines()
            return content

    def write_result(self, data: list):
        csv_columns = ['name', 'goal', 'country', 'region', 'category', 'url']
        with open('all_projects.csv', 'a+') as file_csv:
            writer = csv.DictWriter(file_csv, fieldnames=csv_columns)
            file_csv.seek(0)
            content = file_csv.read()
            if len(content) == 0:
                writer.writeheader()
            for value in data:
                writer.writerow(value)

    def parse(self, page: int, sort: str) -> bool:
        seed = random.randint(0, 9999999)

        list_proxies = self.get_proxies()
        proxy = random.choice(list_proxies).replace('\n', '')
        url = f'https://www.kickstarter.com/discover/advanced?sort={sort}&seed={seed}&page={page}'
        try:
            r = requests.get(url, proxies={'http': proxy, 'https': proxy}, timeout=6)
        except (requests.exceptions.ProxyError, requests.exceptions.ConnectTimeout):
            return False
        html_page = r.text

        soup = bs(html_page, 'html.parser')

        all_projects = soup.find_all('div', class_='js-react-proj-card grid-col-12 grid-col-6-sm grid-col-4-lg')
        total_values = []
        for project in all_projects:
            data_project = project.get('data-project')
            try:
                data_json = json.loads(data_project)
            except json.decoder.JSONDecodeError:
                continue
            name_project = data_json['name']
            goal_project = data_json['goal']
            name_region = data_json['location']['displayable_name']
            country = data_json['country']
            url_project = data_json['urls']['web']['project']
            sort = data_json['category']['name']

            total_values.append({
                'name': name_project, 'goal': goal_project, 'country': country, 'region': name_region,
                'category': sort,
                'url': url_project
            })
        self.write_result(total_values)
        print(f'Function "{self.parse.__name__}" ---> Done')

    def run(self):
        sort_type = ['magic', 'popularity', 'newest', 'end_date', 'most_funded', 'most_backed', 'distance']
        for type in sort_type:
            for page in range(1, 5):
                print(f'Index page {page}/200')
                self.parse(page, type)


parser = Kickstarter()
parser.run()
