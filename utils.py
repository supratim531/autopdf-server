import smtplib

from bs4 import BeautifulSoup

from email import encoders
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


# Email details
sender_email = 'galvanoai13@gmail.com'
sender_password = 'n o y p q g j y i x c k s p i s'
subject = 'PDF Automation Test'


def send_email(receiver_email, user_id):
  # Create the MIMEMultipart email object
  msg = MIMEMultipart()
  msg['From'] = sender_email
  msg['To'] = receiver_email
  msg['Subject'] = subject

  # Add email body
  body = f'Hi, please find the link https://autopdfservermkc.onrender.com/download-pdf/{user_id}'
  msg.attach(MIMEText(body, 'plain'))

  # Sending the email via Gmail's SMTP server
  try:
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
      server.starttls()  # Start TLS encryption
      server.login(sender_email, sender_password)  # Login to your email
      server.sendmail(sender_email, receiver_email, msg.as_string())  # Send the email
      print("Email sent successfully!")
  except Exception as e:
    print(f"Failed to send email: {e}")


def fill_html_as_pdf(html_file_location, child_full_name, dob):
  # Load the HTML file
  with open('pdf.html', 'rb') as file:
    html_content = file.read()

  # Parse the HTML using BeautifulSoup
  soup = BeautifulSoup(html_content, 'html.parser')

  child_full_name_input = soup.find('input', {'id': 'child_full_name'})
  if child_full_name_input:
    child_full_name_input['value'] = child_full_name

  digits = [int(char) for char in dob if char.isdigit()]
  for i in range(1, 9):
    dob_input = soup.find('input', {'id': f'dob_{i}'})
    dob_input['value'] = digits[i - 1]

  # Save the modified HTML to a new file (or overwrite the original)
  with open(html_file_location, 'wb') as file:
    file.write(str(soup).encode("utf-8"))

  print("New HTML file created successfully!!!")
