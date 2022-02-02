from google.oauth2 import id_token
from google.auth.transport import requests

# (Receive token by HTTPS POST)
# ...
CLIENT_ID = '286345722980-jkgpl9u16ak08kqliehg0f99go3r62ig.apps.googleusercontent.com'
token = 'eyJhbGciOiJSUzI1NiIsImtpZCI6IjllYWEwMjZmNjM1MTU3ZGZhZDUzMmU0MTgzYTZiODIzZDc1MmFkMWQiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL2FjY291bnRzLmdvb2dsZS5jb20iLCJhenAiOiIyODYzNDU3MjI5ODAtaXJrMDY2OWc3MWVicDY2OHY0a2I3ZjAwZ3FxMG5qaHIuYXBwcy5nb29nbGV1c2VyY29udGVudC5jb20iLCJhdWQiOiIyODYzNDU3MjI5ODAtamtncGw5dTE2YWswOGtxbGllaGcwZjk5Z28zcjYyaWcuYXBwcy5nb29nbGV1c2VyY29udGVudC5jb20iLCJzdWIiOiIxMDkyMDc0MzM1ODQ3MTEzMzE5NzQiLCJoZCI6InBpbmdhd2ViLmNvbSIsImVtYWlsIjoic3VubnlAcGluZ2F3ZWIuY29tIiwiZW1haWxfdmVyaWZpZWQiOnRydWUsIm5hbWUiOiJTdW5ueSBHdXB0YSIsInBpY3R1cmUiOiJodHRwczovL2xoMy5nb29nbGV1c2VyY29udGVudC5jb20vYS9BQVRYQUp6ZlV5YVE1Z3NNT0VJdnlXYno1RzhJRFFRRHN2WFgzWW5WOW9Iaz1zOTYtYyIsImdpdmVuX25hbWUiOiJTdW5ueSAiLCJmYW1pbHlfbmFtZSI6Ikd1cHRhIiwibG9jYWxlIjoiZW4iLCJpYXQiOjE2NDM3Nzg1NDEsImV4cCI6MTY0Mzc4MjE0MX0.TMwcNPNKcogq0d55OGEcFII6pvF-gmdLFiEFAr9KuRPIPAoRzJBM9-_ToN6TNQE2AdVWgSgI8z6e267E2oyD6fOtOVyXbT2FL23_MLYpXBVesXB8ShvCHJ9MY3ydH3iD-jl3VmWnzZFWrBWqVmnJ78TZLhtt2By5yRsdwe6-MAeP1PB263tQjtK_wJFds4qUQ3kjpRiX8j7kGAL5kxkrupFAnfRv5dXvbkNs74KbLkZI6Ii0EOJa8FPpRcSJTLqELJfU-HNXbg-DNzky-NclD6i-RSk3Qp61pt45TxZiskmvqlfP0t9TH7dNGy_FfB5kW60xOoawoDz6ePg6p1FLpA'

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