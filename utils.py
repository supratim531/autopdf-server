import os
import time
import smtplib
import pyautogui
import subprocess

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

# def html_to_pdf():
# pdf_name= input("Enter your own pdf file name (without extension): ")
# chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
# html_file_path = r"file:///D:/startup/automation_pdf/test.html"
# subprocess.Popen([chrome_path, html_file_path])
# time.sleep(5)
# pyautogui.hotkey('ctrl', 'p')
# time.sleep(2)
# pyautogui.press('enter')
# time.sleep(3)
# pyautogui.press('enter')
# time.sleep(3)
# save_location = f"D:\\startup\\automation_pdf\\pdf_storage\\{pdf_name}.pdf"
# pyautogui.write(save_location)
# pyautogui.press('enter')
# time.sleep(2)
# print(f"PDF saved successfully as {save_location}!")