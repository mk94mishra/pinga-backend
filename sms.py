#!/usr/bin/env python
 
import urllib.request
import urllib.parse
 
def sendSMS(numbers, message):
    apikey='NmMzMjYzNjE1NTRlNzk0YTM4NDM3NjMxNzI2YTUwNGY='
    sender='PINGAH'
    data =  urllib.parse.urlencode({'apikey': apikey, 'numbers': numbers,
        'message' : message, 'sender': sender})
    data = data.encode('utf-8')
    request = urllib.request.Request("https://api.textlocal.in/send/?")
    f = urllib.request.urlopen(request, data)
    fr = f.read()
    return(fr)
 
# resp =  sendSMS('NmMzMjYzNjE1NTRlNzk0YTM4NDM3NjMxNzI2YTUwNGY=', '918877992098',
#     'PINGAH', 'OTP for PINGA password reset is 7666. Do not share it with anyone.')
