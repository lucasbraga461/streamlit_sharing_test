import streamlit as st
import pandas as pd
from google.oauth2 import service_account
import pygsheets

# Create a connection object.
credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],
    scopes=[
        "https://www.googleapis.com/auth/spreadsheets",
    ],
)
client = pygsheets.authorize(custom_credentials=credentials)
sheet = client.open_by_key('1hU-HwHPI61lHjAtECxsWJUjWQ1e_sSOeION72757pKs')
wk = sheet.worksheet_by_title('Sheet1')

st.title("Give your score prediction for Serbia vs. Brazil")
user_input_name = st.text_area("What's your name") #, "Jorge Almeida")
user_input1 = st.text_input("Serbia") #,0)
user_input2 = st.text_input("Brazil") #,0)
def input_from_user(wk, user_input_name, user_input1, user_input2):
    dat = pd.DataFrame(sheet.worksheet_by_title('Sheet1').range('A2:C1000', returnas='matrix'), 
        columns=['Name of the person', 'Team 1 score','Team 2 score'])
    lastrow = int(dat[(dat['Name of the person']!='') &\
                 (dat['Team 1 score']!='') & (dat['Team 2 score']!='')].shape[0]+1)
    newrow = lastrow+1
    return newrow

st.title("Predictions so far")

def main(wk, user_input_name, user_input1, user_input2):
    newrow = input_from_user(wk, user_input_name, user_input1, user_input2)
    wk.update_values(f'A{newrow}:C{newrow}', 
        values=[[user_input_name, user_input1, user_input2]],majordim='ROWS')
    dat = pd.DataFrame(sheet.worksheet_by_title('Sheet1').range(f'A2:C{newrow}', returnas='matrix'), 
        columns=['Name of the person', 'Team 1 score','Team 2 score'])
    st.write(dat)

if __name__ == "__main__":
    main(wk, user_input_name, user_input1, user_input2)
