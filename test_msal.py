import streamlit as st
from msal import ConfidentialClientApplication
import requests

endpoint = 'https://graph.microsoft.com/v1.0/me'
scope = ['https://graph.microsoft.com/.default']

app = ConfidentialClientApplication(
    client_id=st.secrets.client_id,
    authority=st.secrets.authority,
    client_credential=st.secrets.client_secret
)

if st.button("ログイン"):
    accounts = app.get_accounts()

    if accounts:
        result = app.acquire_token_silent(scopes=scope, account=accounts[0])
        st.session_state['access_token'] = result['access_token']
        st.write("ログイン済み")
    else:
        result = app.acquire_token_for_client(scopes=scope)
        st.session_state['access_token'] = result['access_token']
        st.write("ログインしました")
    st.write(result)

if st.button("Graph API"):
    access_token = st.session_state.access_token
    header = {'Authorization': f'Bearer {access_token}'}
    response = requests.get(endpoint, headers=header)
    st.write(response.json())

if st.button("ログアウト"):
    st.session_state['access_token'] = ""
    requests.get('https://login.microsoftonline.com/common/oauth2/v2.0/logout')
