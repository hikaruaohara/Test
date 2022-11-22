import streamlit as st
from msal import PublicClientApplication
import requests

client_id = '8a020a5d-9708-4fa4-aad8-424f65f3982c'
client_secret = 'tkg8Q~YwkNZg~rOAOsx1-m4Z5IarINmOJMQoib9f'
authority = 'https://login.microsoftonline.com/8aeae41b-7510-41db-89ad-800a906ce494'
endpoint = 'https://graph.microsoft.com/v1.0/me'
scope = ['https://graph.microsoft.com/User.Read.All']

app = PublicClientApplication(
    client_id=client_id,
    authority=authority
)

if st.button("ログイン"):
    accounts = app.get_accounts()
    st.write(accounts)

    if accounts:
        result = app.acquire_token_silent(scopes=scope, account=accounts[0])
        st.session_state['access_token'] = result['access_token']
        st.write("ログイン済み")
    else:
        result = app.acquire_token_interactive(scopes=scope)
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
