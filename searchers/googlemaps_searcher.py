import googlemaps
import os
from googlemaps.exceptions import ApiError


class SearchInfoAboutAddressException(Exception):
    pass


class GoogleMapsApiClientError(Exception):
    pass


class GoogleMapsClientApi:
    def __init__(self):
        GOOGLE_MAPS_API_KEY = os.environ['GOOGLE_MAPS_API_KEY']
        self.gmaps = googlemaps.Client(key=GOOGLE_MAPS_API_KEY)

    def get_place_id_from_geocode_response(self, address):
        """
        Выполняем геокодирование по адресу, возвращаем place_id
        """
        try:
            geocode_response = self.gmaps.geocode(address)
            if not geocode_response:
                raise GoogleMapsApiClientError(
                    'Googlemaps geocode response empty'
                )
            place_id = geocode_response[0]['place_id']
            return place_id
        except (ApiError, KeyError) as e:
            raise GoogleMapsApiClientError(e)

    def get_info_about_place(self, place_id):
        """
        Если находим Место по place_id, то выбираем оттуда DBA имя, сайт, телефон
        """
        try:
            googlemaps_place = self.gmaps.place(place_id)['result']
        except ApiError as e:
            raise GoogleMapsApiClientError(e)

        international_phone_number = googlemaps_place\
            .get('international_phone_number')
        name = googlemaps_place.get('name')
        website = googlemaps_place.get('website')

        place = {
            'googlemaps_phone_number': international_phone_number,
            'dba_name': name,
            'website': website,
        }

        return place

    def search_address_info(self, address):
        """
        Интерфейс для получения DBA имени, сайта,
        телефона Места по его адресу на Гугл-карте
        """
        try:
            place_id = self.get_place_id_from_geocode_response(address)
            address_info = self.get_info_about_place(place_id)
            return address_info
        except GoogleMapsApiClientError as e:
            raise SearchInfoAboutAddressException(e)