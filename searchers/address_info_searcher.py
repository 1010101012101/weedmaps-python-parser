from searchers.googlemaps_searcher import GoogleMapsClientApi, \
    SearchInfoAboutAddressException
from searchers.weedmaps_searcher import WeedmapsSearcherClient, \
    WeedmapsSearcherClientError


class AddressInfoSearcher:
    def __init__(self):
        self.googlemaps_client = GoogleMapsClientApi()
        self.weedmaps_client = WeedmapsSearcherClient()

    def search(self, address):
        """
        Ищет и объединяет информацию об адресе из ГуглКарт и поисковых систем
        """
        try:
            googlemaps_info_about_place = \
                self.googlemaps_client.search_address_info(address)
        except SearchInfoAboutAddressException:
            googlemaps_info_about_place = {}

        try:
            weedmaps_info_about_place = \
                self.weedmaps_client.search_address_info(address)
        except WeedmapsSearcherClientError:
            weedmaps_info_about_place = {}

        address_info = {
            'googlemaps_phone_number': None,
            'weedmaps_phone_number': None,
            'dba_name': None,
            'website': None,
            'email': None
        }
        address_info.update(googlemaps_info_about_place)
        address_info.update(weedmaps_info_about_place)

        return address_info