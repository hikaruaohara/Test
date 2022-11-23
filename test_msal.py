import streamlit as st
from msal import ConfidentialClientApplication
import requests

endpoint = 'https://graph.microsoft.com/v1.0/me'
scope = ['user.read']

params = st.experimental_get_query_params()

app = ConfidentialClientApplication(
    client_id=st.secrets.client_id,
    authority=st.secrets.authority,
    client_credential=st.secrets.client_secret
)

url = app.get_authorization_request_url(scopes=scope)
link = f'[login]({url})'
st.markdown(link, unsafe_allow_html=True)

if st.button("アクセストークンを取得"):
    accounts = app.get_accounts()

    if accounts:
        result = app.acquire_token_silent(scopes=scope, account=accounts[0])
        st.session_state['access_token'] = result['access_token']
        st.write("ログイン済み")
    else:
        result = app.acquire_token_by_authorization_code(code=params.get('code'), scopes=scope)
        st.session_state['access_token'] = result['access_token']
    st.write(result)

if st.button("Graph API呼び出し"):
    access_token = st.session_state.access_token
    header = {'Authorization': f'Bearer {access_token}'}
    response = requests.get(endpoint, headers=header)
    st.write(response.json())


logout = '[logout](https://login.microsoftonline.com/common/oauth2/v2.0/logout)'
st.markdown(logout, unsafe_allow_html=True)
