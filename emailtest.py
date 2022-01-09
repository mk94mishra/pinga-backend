import emails
message = emails.html(html="<p>Hi!<br>Here is your receipt...",
                        subject="Your receipt No. 567098123",
                        mail_from=('Some Store', 'manish@pingaweb.com'))


r = message.send(to='mk94mishra@gmail.com', smtp={'host': 'pingaweb.com', 'timeout': 5})
assert r.status_code == 250