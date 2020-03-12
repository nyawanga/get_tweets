import xlsxwriter
import csv
import sys
import os
import re
sys.path.append("../")

# import pandas as pd
import pygsheets
# from lib.db_connection_roam import get_connection                           # from the db connection module
from oauth2client.service_account import ServiceAccountCredentials

def to_excel(data, start_row, start_col, workbook_name, sheet_name):
    """
        - data should be a list of lists
        - start_row, start_col are integers
        - workbook_name, sheet_name as text
    """
    with xlsxwriter.Workbook(workbook_name) as workbook:
        worksheet = workbook.add_worksheet( sheet_name )

        for _ in tuple(data):
            for idx, item in enumerate(_):
                col = idx
                worksheet.write(start_row, start_col, item)
            start_row+= 1
            # print(start_row)
            print("data saved to file !")

def to_csv(data, file_name, mode):
    """
        - data as a list of lists
        - file_name as text
        - mode as "w", "a"
    """
    with open(file_name, mode, encoding='utf-8') as f:
        csv_writer = csv.writer(f, dialect='excel', lineterminator='\n', quoting=csv.QUOTE_NONNUMERIC)
        [csv_writer.writerow(row) for row in data]
        print("data saved to file !")


def to_gsheets(data, rows, cols, cols_order, start_cell=(2, 1), tab_name="Data", as_df=False):
    credentials = get_credentials()
    sheet_access = credentials.open_by_key(worksheet_key)
    first_row = start_cell[0]
    last_row = rows + 1
    end_cell = (rows, cols)

    try:
        tab = sheet_access.worksheet_by_title(tab_name)
        print("deleting data from range {} ... ".format(start_cell))
        print("-" * 100)
        # tab.clear('A{0}:H{1}'.format(first_row, last_row))
        tab.clear(start=start_cell, end=end_cell)
        col_names = tab.get_values(start=(1, 1), end=(1, cols))[0]
        sort_data = [[row[item] for item in col_names] for row in data]
#         sort_data = ['' for item in sort_data if item is None]
        # print(col_names)
        print("updating data now ...")
        if as_df:
            # print("testing")
            data = pd.DataFrame(data, columns=cols_order)
            data = data[col_names]
            # print(data.head(2))
            tab.set_dataframe(data, start_cell, fit=True, copy_head=False, escape_formulae=True)
        else:
            # print(sort_data[:2])
            # tab.update_values(crange='A{0}:H{1}'.format(first_row, last_row), values=data, extend=True)
            tab.update_values(crange=start_cell, values=sort_data, extend=True)
    except pygsheets.exceptions.WorksheetNotFound:
        print("{} sheet not found".format(tab_name))
        sys.exit(1)
    except Exception as err:
        print("{} got when attempting to get the sheet {}".format(err, tab_name))
    finally:
        print("-" * 100)



