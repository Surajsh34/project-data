
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
import openai
import time

CREDENTIALS_FILE = "/Users/surajshukla/Desktop/ikproject/myproject/chatboat/utill/token.json"
# Create your views here.

#openai.api_key = "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"
def get_google_sheets_service():
    creds = Credentials.from_service_account_file(CREDENTIALS_FILE, scopes=[
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive",
    ])

    service = build('sheets', 'v4', credentials=creds)
    return service


def update_spreadsheet_value(spreadsheet_id, request, rg):
    service = get_google_sheets_service()
   
    service.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id,
        range=rg,
        valueInputOption='RAW',
        body=request
    ).execute()


def read_a_spreadsheet(spreadsheet_id, sheet_name):
    
    service = get_google_sheets_service()
    print("b")
    cell_ids = "A1:Z1000"

    # Read data and cell IDs from the sheet
    result = service.spreadsheets().values().batchGet(spreadsheetId=spreadsheet_id, ranges=[sheet_name + '!' + cell_ids]).execute()
    data = result.get('valueRanges', [])[0].get('values', [])
    cell_ids = cell_ids.split(':')[0]  # Extract the starting cell ID from the range
   
    datad=[]
    questionset=['C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'AA', 'AB', 'AC', 'AD']
    #for row, row_index in zip(data[1:], range(1, len(data))):
    callindex=2
    for row, row_index in zip(data[1:], range(1, 2)):    
        temp=""
        response=""
        #for col, col_index in zip(row[1:], range(1, len(row))):
        for col, col_index in zip(row[1:], range(1, 5)):
            cell_id = chr(ord(cell_ids[0]) + col_index) + str(int(cell_ids[1:]) + row_index)
            print({col_index}, cell_id )
            k=1
            callindex=callindex+1
            #temp= f"{temp}\n{col_index}:{col}"
            for index in questionset:
                  if k==1:
                     k=2
                  elif k==2:
                    k=3
                    temp= f"{temp}\n{col_index}:{col}"
                    col=temp
                      
                  print(index)
                 # print(col)
                  cell_range = "Call Analysis!"+index +"1"
    
                  mt = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range=cell_range).execute().get("values", [])  
                  yx = [value.replace('\n\n', '').replace('[', '').replace(']', '').replace("['", "").replace("']", "") for row in mt for value in row]
                  #print(yx)
                  prompt= f"question: {yx}\nCall transcript: "+col

                  try:
                     response=openai.ChatCompletion.create(
                           model="gpt-4",
                           messages=[
                               {"role": "system", "content": "You are a helpful assistant."},
                                {"role": "user", "content": prompt},
                           ],
                           temperature=0.7,
                           max_tokens=500,
                           frequency_penalty=0.0

                        )
                  except  Exception as e: 
                     if "Rate limit reached" in str(e):
                         time.sleep(60) 
                         response=openai.ChatCompletion.create(
                           model="gpt-4",
                           messages=[
                               {"role": "system", "content": "You are a helpful assistant."},
                                {"role": "user", "content": prompt},
                           ],
                           temperature=0.7,
                           max_tokens=1000,
                           frequency_penalty=0.0

                        )
                     else:    
                        print(f"Error: {e} ")

                  tempdata=""
                  if 'choices' in response and len(response['choices']) > 0:
                      tempdata = response['choices'][0]["message"]["content"].strip()
                      print(tempdata)
                      rg= "Call Analysis!"+ index + str(callindex)
                      request = {
                            'values': [[tempdata]]
                           }
                      update_spreadsheet_value(spreadsheet_id,request,rg)
                      datad.append({'value': tempdata, 'cell_id': cell_id})
                  else:
                      tempdata = "No response found."
            
    return datad