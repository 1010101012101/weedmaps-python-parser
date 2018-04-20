import pandas as pd
from datetime import datetime


class BaseReadWriteXlsx:
    def _read_dataframe_from_input_xls(self, file_path):
        """
        Считать первый лист XLSX файла как датафрейм
        """
        xl = pd.ExcelFile(file_path)
        sheets = xl.sheet_names
        first_sheet = sheets[0]
        df = xl.parse(first_sheet)
        return df

    def _write_dataframe_to_output_xls(self, dataframe, file_path,
                                       sheet_name='Sheet1'):
        """
        Записать датафрейм в лист XLSX файла
        """
        writer = pd.ExcelWriter(file_path, engine='xlsxwriter')
        dataframe.to_excel(writer, sheet_name=sheet_name)
        writer.save()

    def _update_dataframe(self, dataframe):
        raise NotImplementedError

    def read_write_xlsx(self, input_file_path):
        input_dataframe_from_xls = self._read_dataframe_from_input_xls(
            input_file_path)
        updated_dataframe = self._update_dataframe(input_dataframe_from_xls)

        current_datetime_string = datetime.now().strftime('%Y-%m-%d')
        output_xls_file_path = \
            f'{input_file_path} - {current_datetime_string}.xlsx'
        self._write_dataframe_to_output_xls(
            updated_dataframe,
            output_xls_file_path
        )
