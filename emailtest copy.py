from mailchimp_marketing import Client

mailchimp = Client()
mailchimp.set_config({
  "api_key": "94220505153ac2703bea9f37d3711c93-us20",
  "server": "us20"
})

response = mailchimp.ping.get()
print(response)