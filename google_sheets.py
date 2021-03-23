import json
from pprint import pprint

import httplib2
import googleapiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials

# Файл, полученный в Google Developer Console
# from common import PLATFORM_NAMES
from settings import DOC_ID

CREDENTIALS_FILE = 'creds.json'
# ID Google Sheets документа (можно взять из его URL)


def get_service():
    # Авторизуемся и получаем service — экземпляр доступа к API
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        CREDENTIALS_FILE,
        ['https://www.googleapis.com/auth/spreadsheets',
         'https://www.googleapis.com/auth/drive'])
    httpAuth = credentials.authorize(httplib2.Http())
    service = googleapiclient.discovery.build('sheets', 'v4', http=httpAuth)
    return service


def update_data_in_table(project_name, count_dict, current_datetime, common_extra_charge):
    service = get_service()
    sheet_metadata = service.spreadsheets().get(spreadsheetId='1FDl2_-_vMHnDzLGO-xHE8EcV5rAmKzmJKDRGYgagF0o').execute()
    properties = sheet_metadata.get('sheets')
    for item in properties:
        if item.get("properties").get('title') == project_name:
            sheet_name = (item.get("properties").get('title'))

    # Пример чтения файла
    values = service.spreadsheets().values().get(
        spreadsheetId=DOC_ID,
        range='%s!B3' % project_name,
        majorDimension='COLUMNS'
    ).execute()
    number_of_counts = int(values['values'][0][0])
    current_row = str(5 + number_of_counts)

    count_data = [
            current_datetime,
            str(count_dict['list']),
            count_dict['currency'],
            count_dict['rate'],
            count_dict['extra_charge']
    ]
    service.spreadsheets().values().batchUpdate(
        spreadsheetId=DOC_ID,
        #обновите кол-во строчек и общую наценку
        body={
            "valueInputOption": "USER_ENTERED",
            "data": [
                {
                    "range": "%s!B2" % project_name,
                    "majorDimension": "ROWS",
                    "values": [[str(common_extra_charge)]]
                },
                {
                    "range": "%s!B3" % project_name,
                    "majorDimension": "ROWS",
                    "values": [[str(number_of_counts+1)]]
                },
                {
                    "range": project_name + "!A" + current_row + ":E" + current_row,
                    "majorDimension": "ROWS",
                    "values": [count_data]
                },
            ]
        }
    ).execute()


def init_sheet(project_name):
    with open('data/%s.json' % project_name, 'r+') as file:
        files_data = file.read()
        file_dict = json.loads(files_data)
        file.close()

    number_of_counts = len(file_dict.keys()) - 1
    service = get_service()

    counts_data = []

    for key in file_dict.keys():
        if key == 'common_extra_charge':
            continue
        else:
            counts_data.append(
                [
                    key,
                    str(file_dict[key]['list']),
                    file_dict[key]['currency'],
                    file_dict[key]['rate'],
                    file_dict[key]['extra_charge']
                ]
            )

    service.spreadsheets().values().batchUpdate(
        spreadsheetId=DOC_ID,
        body={
            "valueInputOption": "USER_ENTERED",
            "data": [
                {
                    "range": "%s!A2:B3" % project_name,
                    "majorDimension": "ROWS",
                    "values": [
                        ['Common extra charge:', file_dict['common_extra_charge']],
                        ['Number of counts:', number_of_counts]
                    ]
                },
                {
                    "range": "%s!A4:E4" % project_name,
                    "majorDimension": "ROWS",
                    "values": [['Datetime', 'List of prices', 'Currency', 'Rate', 'Extra charge']]
                },
                {
                    "range": project_name + '!A5:E' + str(5+number_of_counts),
                    "majorDimension": "ROWS",
                    "values": counts_data
                }
            ]
        }
    ).execute()


def update_main_page(all_extra_charges):
    main_page_name = 'Main_page'
    service = get_service()
    sheet_metadata = service.spreadsheets().get(spreadsheetId='1FDl2_-_vMHnDzLGO-xHE8EcV5rAmKzmJKDRGYgagF0o').execute()
    properties = sheet_metadata.get('sheets')
    for item in properties:
        if item.get("properties").get('title') == main_page_name:
            sheet_name = (item.get("properties").get('title'))

    number_of_rows = len(all_extra_charges)

    service.spreadsheets().values().batchUpdate(
        spreadsheetId=DOC_ID,
        # обновите кол-во строчек и общую наценку
        body={
            "valueInputOption": "USER_ENTERED",
            "data": [
                {
                    "range": main_page_name + "!A1:B1",
                    "majorDimension": "ROWS",
                    "values": [['Platform and sellers country', 'Extra charge, %']]
                },
                {
                    "range": main_page_name + "!A2:B" + str(number_of_rows+1),
                    "majorDimension": "ROWS",
                    "values": all_extra_charges
                },
            ]
        }
    ).execute()

# for key in PLATFORM_NAMES.keys():
#     init_sheet(PLATFORM_NAMES[key])