import selenium.common.exceptions
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class Proxies:
    def __init__(self):
        options = Options()
        options.add_argument('--headless')
        cwd = os.getcwd()
        self._browser = webdriver.Chrome(f'{cwd}/chromedriver',
                                         chrome_options=options)
        self._url_proxy_cz = 'http://free-proxy.cz/en/proxylist/country/all/https/ping/all'

    def proxy_cz(self, page: int) -> None:
        url = f'{self._url_proxy_cz}/{page}'
        self._browser.get(url)
        self._browser.implicitly_wait(2)
        export_ips = self._browser.find_element_by_xpath('/html/body/div[2]/div[2]/div[5]/span').click()
        list_ips = self._browser.find_element_by_xpath('/html/body/div[2]/div[2]/div[6]').text
        with open('list_proxies.csv', 'a') as f:
            f.writelines(list_ips + '\n')

    def proxy_list_net(self) -> None:
        url = 'https://free-proxy-list.net/'
        self._browser.get(url)
        all_rows = self._browser.find_elements_by_tag_name('tr')
        num_rows = len(all_rows)
        all_proxies = []
        for tr in range(1, num_rows):
            https_xpath = f'/html/body/section[1]/div/div[2]/div/table/tbody/tr[{tr}]/td[7]'
            ip_xpath = f'/html/body/section[1]/div/div[2]/div/table/tbody/tr[{tr}]/td[1]'
            port_xpath = f'/html/body/section[1]/div/div[2]/div/table/tbody/tr[{tr}]/td[2]'

            try:
                https = self._browser.find_element_by_xpath(https_xpath).text
            except selenium.common.exceptions.NoSuchElementException:
                break

            if https == 'no':
                continue
            else:
                ip = self._browser.find_element_by_xpath(ip_xpath).text
                port = self._browser.find_element_by_xpath(port_xpath).text
                proxy_https = f'http://{ip}:{port}\n'
                all_proxies.append(proxy_https)

        with open('list_proxies.csv', 'w') as f:
            f.writelines(all_proxies)

    def run(self):
        self.proxy_list_net()
        for page in range(1, 6):
            self.proxy_cz(page)
        self._browser.close()



proxy = Proxies()
proxy.run()
