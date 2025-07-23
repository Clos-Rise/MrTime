from google.oauth2 import service_account
from googleapiclient.discovery import build

scopes = ['https://www.googleapis.com/auth/spreadsheets']
key_file = 'config/service-account-key.json'

creds = service_account.Credentials.from_service_account_file(key_file, scopes=scopes)
service = build('sheets', 'v4', credentials=creds)

sheet_id = '1wUR8P25sgkRtmpLCsgl-MEXgv89rmWeCNeH46TZMAtE'

def write(rng, vals):
    body = {'values': vals}
    return service.spreadsheets().values().update(
        spreadsheetId=sheet_id,
        range=rng,
        valueInputOption='RAW',
        body=body
    ).execute()

def clear(rng):
    service.spreadsheets().values().clear(spreadsheetId=sheet_id, range=rng).execute()

def add(rng, vals):
    body = {'values': vals}
    return service.spreadsheets().values().append(
        spreadsheetId=sheet_id,
        range=rng,
        valueInputOption='RAW',
        insertDataOption='INSERT_ROWS',
        body=body
    ).execute()

def del_row(num):
    req = [{
        "deleteDimension": {
            "range": {
                "sheetId": 0,
                "dimension": "ROWS",
                "startIndex": num - 1,
                "endIndex": num
            }
        }
    }]
    service.spreadsheets().batchUpdate(spreadsheetId=sheet_id, body={"requests": req}).execute()

def del_val(val, col=1):
    res = service.spreadsheets().values().get(spreadsheetId=sheet_id, range='A1:A1000').execute()
    vals = res.get('values', [])
    for i in reversed(range(len(vals))):
        if vals[i] and vals[i][0] == val:
            del_row(i + 1)

# write('A1:B2', [['Erida', 'Test'], ['Hello', 'World']])
# clear('A1:Z100')
# add('A1:B1', [['New','Row']])
# del_row(3)
# del_val('Erida', 1)
