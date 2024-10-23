import os
import smtplib

from bs4 import BeautifulSoup

from email import encoders
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Email details
sender_email = 'galvanoai13@gmail.com'
sender_password = 'n o y p q g j y i x c k s p i s'
subject = 'Our PDF Automation Project'

def send_email(receiver_email):
  # Create the MIMEMultipart email object
  msg = MIMEMultipart()
  msg['From'] = sender_email
  msg['To'] = receiver_email
  msg['Subject'] = subject

  # Add email body
  body = 'Hi, please find the attached HTML file.'
  msg.attach(MIMEText(body, 'plain'))

  # File attachment path (HTML file)
  file_path = 'filled_pdf.html'

  # Open the HTML file to attach
  with open(file_path, 'rb') as attachment:
    mime_base = MIMEBase('application', 'octet-stream')
    mime_base.set_payload(attachment.read())

  # Encode file in base64
  encoders.encode_base64(mime_base)

  # Add the header for the attachment
  mime_base.add_header('Content-Disposition', f'attachment; filename={os.path.basename(file_path)}')

  # Attach the file to the email
  msg.attach(mime_base)

  # Sending the email via Gmail's SMTP server
  try:
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
      server.starttls()  # Start TLS encryption
      server.login(sender_email, sender_password)  # Login to your email
      server.sendmail(sender_email, receiver_email, msg.as_string())  # Send the email
      print("Email sent successfully!")
  except Exception as e:
    print(f"Failed to send email: {e}")

def fill_html_as_pdf(name, email):
	# Load the HTML file
	with open('pdf.html', 'r') as file:
		html_content = file.read()

	# Parse the HTML using BeautifulSoup
	soup = BeautifulSoup(html_content, 'html.parser')

	# Find the input field by its id and set the value for "Name"
	name_input = soup.find('input', {'id': 'name'})
	if name_input:
		name_input['value'] = name

	# Find the input field by its id and set the value for "Email"
	email_input = soup.find('input', {'id': 'email'})
	if email_input:
		email_input['value'] = email

	# Save the modified HTML to a new file (or overwrite the original)
	with open('filled_pdf.html', 'w') as file:
		file.write(str(soup))

	print("HTML file updated successfully!")
