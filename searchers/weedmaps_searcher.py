import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


class WeedmapsSearcherClientError(Exception):
    pass


class WeedmapsSearcherClient:
    def __init__(self):
        self.driver = webdriver.Chrome()

    def search_address_info(self, address_search_string):
        try:
            weedmaps_link = self.\
                get_weedmaps_link_for_address_in_google(address_search_string)
            address_info = self.\
                get_address_info_from_weedmaps(weedmaps_link)
            print(f'Address info for {address_search_string} is {address_info}')
            return address_info
        except Exception as e:
            raise WeedmapsSearcherClientError(e)

    def search_instagram_link(self, email_search_string):
        try:
            weedmaps_link = self. \
                get_weedmaps_link_for_address_in_bing(email_search_string)
            instagram_link = self\
                .get_instagram_link_from_weedmaps_page(weedmaps_link)
            return instagram_link
        except Exception as e:
            raise WeedmapsSearcherClientError(e)


    def get_weedmaps_link_for_address_in_google(self, address):
        """
        Пытаемся найти и получить первую ссылку на weedmaps в Гугле
        """

        self.driver.get('http://www.google.com')
        input_element = self.driver.find_element_by_name('q')
        input_element.send_keys(address)
        input_element.submit()

        RESULTS_LOCATOR = 'div h3 a'

        time.sleep(5)

        page1_results = self.driver.find_elements(
            By.CSS_SELECTOR, RESULTS_LOCATOR
        )

        for item in page1_results:
            if item.get_attribute('href').startswith('https://weedmaps.com'):
                return item

    def get_weedmaps_link_for_address_in_bing(self, address):
        """
        Пытаемся найти и получить первую ссылку на weedmaps в Бинг
        """

        self.driver.get('http://www.bing.com')
        input_element = self.driver.find_element_by_id('sb_form_q')
        input_element.send_keys(address)
        input_element.submit()

        RESULTS_LOCATOR = 'div h2 a'

        page1_results = self.driver.find_elements(
            By.CSS_SELECTOR, RESULTS_LOCATOR
        )


        for item in page1_results:
            href = item.get_attribute('href')
            if href.startswith('https://weedmaps.com'):
                print(href)
                return href

    def get_address_info_from_weedmaps(self, weedmaps_link):
        if not weedmaps_link:
            return {}
        main_window = self.driver.current_window_handle
        weedmaps_link.send_keys(Keys.COMMAND + Keys.RETURN)
        self.driver.find_element_by_tag_name('body').send_keys(
            Keys.COMMAND + Keys.TAB)
        tabs = self.driver.window_handles
        self.driver.switch_to.window(tabs[1])

        time.sleep(5)
        try:
            phone = self.driver.find_element_by_css_selector(
                'div.listing-contacts a[itemprop="telephone"]'
            ).text
        except Exception:
            phone = None

        try:
            email = self.driver.find_element_by_css_selector(
                'div.listing-contacts a[itemprop="email"]'
            ).text
        except Exception:
            email = None

        address_info = {
            'weedmaps_phone_number': phone,
            'email': email
        }

        self.driver.close()
        self.driver.switch_to_window(main_window)

        return address_info

    def get_instagram_link_from_weedmaps_page(self, weedmaps_link):
        if not weedmaps_link:
            return None

        main_window = self.driver.current_window_handle
        self.driver.execute_script(f'window.open("{weedmaps_link}");')

        self.driver.find_element_by_tag_name('body').send_keys(
            Keys.COMMAND + Keys.TAB
        )

        tabs = self.driver.window_handles
        self.driver.switch_to.window(tabs[1])

        time.sleep(5)

        try:
            details_link = self.driver\
                .find_element_by_css_selector('.item-details a')
            details_link.click()
        except Exception:
            details_link = None

        try:
            instagram_link = self.driver\
                .find_element_by_css_selector(
                '.details-card-item-data#instagram a'
            ).get_attribute('href')
        except Exception:
            instagram_link = None

        self.driver.close()
        self.driver.switch_to_window(main_window)

        return instagram_link