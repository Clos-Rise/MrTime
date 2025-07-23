# Клиент для работы с Google Docs API


from google.oauth2 import service_account
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/documents']
SERVICE_ACCOUNT_FILE = 'mrtime-466808-d21bd527a457.json'

creds = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE,
    scopes=SCOPES
)

service = build('docs', 'v1', credentials=creds)

DOCUMENT_ID = '1KQO0HKHiuFIxvMtvK2v5PonIyTGIrWfh3EJD9Rx6310'

def write_text(text):
    requests = [
        {
            'insertText': {
                'location': {'index': 1},
                'text': text
            }
        }
    ]
    service.documents().batchUpdate(documentId=DOCUMENT_ID, body={'requests': requests}).execute()

def clear_document():
    doc = service.documents().get(documentId=DOCUMENT_ID).execute()
    length = doc['body']['content'][-1]['endIndex'] - 1
    requests = [
        {'deleteContentRange': {'range': {'startIndex': 1, 'endIndex': length}}}
    ]
    service.documents().batchUpdate(documentId=DOCUMENT_ID, body={'requests': requests}).execute()

def delete_text(text_to_delete):
    doc = service.documents().get(documentId=DOCUMENT_ID).execute()
    content = doc.get('body').get('content')
    requests = []
    for element in content:
        paragraph = element.get('paragraph')
        if not paragraph:
            continue
        for elem in paragraph.get('elements', []):
            txt = elem.get('textRun', {}).get('content', '')
            start_index = elem.get('startIndex')
            if text_to_delete in txt:
                start = start_index + txt.find(text_to_delete)
                end = start + len(text_to_delete)
                requests.append({'deleteContentRange': {'range': {'startIndex': start, 'endIndex': end}}})
    if requests:
        service.documents().batchUpdate(documentId=DOCUMENT_ID, body={'requests': requests}).execute()

def add_text_after(text_to_find, text_to_add):
    doc = service.documents().get(documentId=DOCUMENT_ID).execute()
    content = doc.get('body').get('content')
    for element in content:
        paragraph = element.get('paragraph')
        if not paragraph:
            continue
        for elem in paragraph.get('elements', []):
            txt = elem.get('textRun', {}).get('content', '')
            start_index = elem.get('startIndex')
            if text_to_find in txt:
                insert_index = start_index + txt.find(text_to_find) + len(text_to_find)
                requests = [
                    {'insertText': {'location': {'index': insert_index}, 'text': text_to_add}}
                ]
                service.documents().batchUpdate(documentId=DOCUMENT_ID, body={'requests': requests}).execute()
                return

#write_text('Привет, Erida Docs!\n')
clear_document()
#delete_text('Erida')
# add_text_after('Привет', ' Мир')