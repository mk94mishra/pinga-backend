from google.oauth2 import id_token
from google.auth.transport import requests

# (Receive token by HTTPS POST)
# ...
CLIENT_ID = '286345722980-jkgpl9u16ak08kqliehg0f99go3r62ig.apps.googleusercontent.com'
token = 'eyJhbGciOiJSUzI1NiIsImtpZCI6IjllYWEwMjZmNjM1MTU3ZGZhZDUzMmU0MTgzYTZiODIzZDc1MmFkMWQiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL2FjY291bnRzLmdvb2dsZS5jb20iLCJhenAiOiIyODYzNDU3MjI5ODAtaXJrMDY2OWc3MWVicDY2OHY0a2I3ZjAwZ3FxMG5qaHIuYXBwcy5nb29nbGV1c2VyY29udGVudC5jb20iLCJhdWQiOiIyODYzNDU3MjI5ODAtamtncGw5dTE2YWswOGtxbGllaGcwZjk5Z28zcjYyaWcuYXBwcy5nb29nbGV1c2VyY29udGVudC5jb20iLCJzdWIiOiIxMDkyMDc0MzM1ODQ3MTEzMzE5NzQiLCJoZCI6InBpbmdhd2ViLmNvbSIsImVtYWlsIjoic3VubnlAcGluZ2F3ZWIuY29tIiwiZW1haWxfdmVyaWZpZWQiOnRydWUsIm5hbWUiOiJTdW5ueSBHdXB0YSIsInBpY3R1cmUiOiJodHRwczovL2xoMy5nb29nbGV1c2VyY29udGVudC5jb20vYS9BQVRYQUp6ZlV5YVE1Z3NNT0VJdnlXYno1RzhJRFFRRHN2WFgzWW5WOW9Iaz1zOTYtYyIsImdpdmVuX25hbWUiOiJTdW5ueSAiLCJmYW1pbHlfbmFtZSI6Ikd1cHRhIiwibG9jYWxlIjoiZW4iLCJpYXQiOjE2NDM2OTkyNjgsImV4cCI6MTY0MzcwMjg2OH0.K_SIxje4jvo3Z-IJBglS8iPPJIkUldrEYnqnF-t76JWlwH-ch5pGSlt9cFoIQ-swXf0VqEv4w-YqnypvEn3dM0mypUuWCzJCTgKgJtycLiay73Xr7D4b32z2iqC5TV0_0DkBeoSYWoBAoMl_d8kOCfDzYmHrjE74OOO0EQkg757O1HSL-sABEeKNVRCyxwMQEDFGphJQoItMs08E0VpjphMCUFPHvlpq62cXCG4r7YjK2KhT8x-pAg5PPh-Ws5DFcFWeG_EgIdDRW0z1rOl6M7WOHLNxWX77jsfMhOlQ9jAPkoui22fBRM1CQp74CYk43KRUKarGTkeL6KE0Q-Cnng'

# Specify the CLIENT_ID of the app that accesses the backend:
idinfo = id_token.verify_oauth2_token(token, requests.Request(), CLIENT_ID)

# Or, if multiple clients access the backend server:
# idinfo = id_token.verify_oauth2_token(token, requests.Request())
# if idinfo['aud'] not in [CLIENT_ID_1, CLIENT_ID_2, CLIENT_ID_3]:
#     raise ValueError('Could not verify audience.')

# If auth request is from a G Suite domain:
# if idinfo['hd'] != GSUITE_DOMAIN_NAME:
#     raise ValueError('Wrong hosted domain.')

# ID token is valid. Get the user's Google Account ID from the decoded token.
userid = idinfo
print(userid)