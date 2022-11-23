import streamlit as st
from msal import ConfidentialClientApplication
import requests

endpoint = 'https://graph.microsoft.com/v1.0/me'
scope = ['user.read']

app = ConfidentialClientApplication(
    client_id=st.secrets.client_id,
    authority=st.secrets.authority,
    client_credential=st.secrets.client_secret
)

url = app.get_authorization_request_url(scopes=scope)
link = f'[login]({url})'
st.markdown(link, unsafe_allow_html=True)

if st.button("アクセストークンを取得"):
    print(requests.get(url=url).url)
    accounts = app.get_accounts()

    if accounts:
        result = app.acquire_token_silent(scopes=scope, account=accounts[0])
        st.session_state['access_token'] = result['access_token']
        st.write("ログイン済み")
    else:
        # result = app.acquire_token_by_authorization_code(
        # code='0.AWsAyHPuBES0vE-ghXA8i5KDV17SDCIY17JHkDz-SyYomLxrAD0.AgABAAIAAAD--DLA3VO7QrddgJg7WevrAgDs_wQA9P8ZxKTuPV0CGIxctdChnFngWFX76q_CXhGD_4x6Hf20fhm6JDr1NWdtUzJp2gYFy8typZ3-4PaqhXfEv1zL8aBa9IA6HCvA52AZyv61sjKHelOddOLDS0kA3wgYAOKjO7x9qfh7mSBCBWeoUYvUXBz78HJyrzjldTUisWBj8OwNY9mnxd1L-tow74hdPYaww9s0rso5LHGV-0ePc7bTyH_dSQGvRAIhIhSka34-0a22BCscybGBNzjFmJeR8Kx9zlA3g1R-bjq5sq8dJ5FLG0RI45Nvihgk4qiUwWcu2lYMswLE362dNO6mJ7F17a9R7FHYvRdOYNy5LGkTDSc-X4PBDjqgWnYWBOsjXWxJoaQClhARKvJggx14ZaDtWC6CCqpXOZRsRZqtW5EbMCa7vkkvc0A8LSCSJG0va4iUlDQI7vMNQ_F7-I57VLJmeF9fNoX6wMKSKgRmXWBVe0px1GTHG2O6W4u39ngYkkfR0c6n45BSxLA68R0Otr5OrCd_eVokmk5M3mhOD5tB8ZRz-VdJ0t8et1JOSJidzkJ0ROWYCCRmrbTcsD1oYv-qW0U6S6h1SRmQ2qOKWRk00PXY-ZENmtlZt_lBR-DPFZunkkJUdOweR0bwnKvt5obu23cuoMUrfnzLdfTTo1oYHe-SWRt_SqdbfiyhWOrQLB1ShEC6DRu9tyqNGMy_jBsIF3PRrIykgSwbgIcDctzSRBOHtEaRy0ipHssusPY-pC3Be1hZdtu9q_bSb5r6m7uU7aSVmoyVMZZxawrVjkx3nlH5M8CgUQRs5KiW8RgO700GFkqF5KpGkCO65wrIk27-ZajEKWIsIObvdfTEAutsOAbs4YTjyViLoODloj0ZfnDeUVcTVoK39Nd7nfgtubxLpvOrTmXZzmFImxjYvikXRQcUIVAxuUKgrVNhzpIftXQEkyHxxCMYZM6KNnbkMaWc4EF5GwjLTZbX3J3YgDvatB0C', scopes=scope)
        # result = app.acquire_token_by_username_password(username='cmj14001@ict.nitech.ac.jp', password='aKGOB5uP3xjaly!', scopes=scope)
        # result = app.acquire_token_for_client(scopes=scope)
        # st.session_state['access_token'] = result['access_token']
        # result = app.acquire_token_by_authorization_code(code=result['access_token'], scopes=scope)
        st.write("ログインしました")
    st.write(result)

if st.button("Graph API呼び出し"):
    access_token = st.session_state.access_token
    header = {'Authorization': f'Bearer {access_token}'}
    response = requests.get(endpoint, headers=header)
    st.write(response.json())


if st.button("ログアウト"):
    st.session_state['access_token'] = ""
    requests.get('https://login.microsoftonline.com/common/oauth2/v2.0/logout')

logout = '[logout](https://login.microsoftonline.com/common/oauth2/v2.0/logout)'
st.markdown(logout, unsafe_allow_html=True)
