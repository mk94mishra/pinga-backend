# import mailchimp_transactional as MailchimpTransactional
# from mailchimp_transactional.api_client import ApiClientError

# def run():
#   try:
#     mailchimp = MailchimpTransactional.Client('877cb4df376f85992cb453bfe707bcb1-us20')
#     response = mailchimp.users.ping()
#     print('API called successfully: {}'.format(response))
#   except ApiClientError as error:
#     print('An exception occurred: {}'.format(error.text))

# run()