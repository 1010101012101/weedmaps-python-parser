import sys

from read_write_xlsx import BaseReadWriteXlsx
from searchers.address_info_searcher import AddressInfoSearcher


class GetAddressInfoFromMaps(BaseReadWriteXlsx):
    def update_dataframe(dataframe):
        address_info_searcher = AddressInfoSearcher()

        rows_count = dataframe.shape[0]
        for current_row_number in range(rows_count):
            address_search_string = dataframe['Legal Business Name'][current_row_number] + \
                            dataframe['Address'][current_row_number]

            address_info = address_info_searcher.search(address_search_string)

            dataframe['Phone Google'][current_row_number] = \
                address_info['googlemaps_phone_number']
            dataframe['DBA'][current_row_number] = \
                address_info['dba_name']
            dataframe['Website'][current_row_number] = \
                address_info['website']
            dataframe['Phone Weedmaps'][current_row_number] = \
                address_info['weedmaps_phone_number']
            dataframe['Email'][current_row_number] = \
                address_info['email']

        return dataframe


get_address_from_maps = GetAddressInfoFromMaps()

input_file_path = sys.argv[1]

get_address_from_maps.read_write_xlsx(input_file_path)