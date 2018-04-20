import sys

import numpy as np

from read_write_xlsx import BaseReadWriteXlsx
from searchers.weedmaps_searcher import WeedmapsSearcherClient, \
    WeedmapsSearcherClientError


class GetInstaLinkForEmailFromWeedmaps(BaseReadWriteXlsx):
    def update_dataframe(dataframe):
        weedmaps_searcher = WeedmapsSearcherClient()

        rows_count = dataframe.shape[0]
        dataframe = dataframe.replace(np.nan, '', regex=True)
        for current_row_number in range(rows_count):
            email = dataframe['email'][current_row_number]
            current_instagram_link = dataframe['Instagram'][current_row_number]
            if not current_instagram_link:
                try:
                    instagram_link = \
                        weedmaps_searcher.search_instagram_link(email)
                    dataframe['Instagram'][current_row_number] = instagram_link
                except WeedmapsSearcherClientError:
                    pass
        return dataframe


input_file_path = sys.argv[1]

get_insta_link_for_email = GetInstaLinkForEmailFromWeedmaps()

get_insta_link_for_email.read_write_xlsx(input_file_path)

