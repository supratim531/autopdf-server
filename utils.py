import os
import logging
import smtplib

from bs4 import BeautifulSoup

from datetime import datetime

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from logging.handlers import RotatingFileHandler


# Email details
email_subject = os.getenv("EMAIL_SUBJECT")
sender_email = os.getenv("SENDER_EMAIL")
sender_email_password = os.getenv("SENDER_EMAIL_PASSWORD")


def setup_logger():
  logger = logging.getLogger()
  logger.setLevel(logging.INFO)
  formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

  console_handler = logging.StreamHandler()
  console_handler.setLevel(logging.INFO)
  console_handler.setFormatter(formatter)
  logger.addHandler(console_handler)

  file_handler = RotatingFileHandler('task.log', maxBytes=1024 * 1024 * 10, backupCount=3)
  file_handler.setLevel(logging.INFO)
  file_handler.setFormatter(formatter)
  logger.addHandler(file_handler)
  return logger


def send_email(receiver_emails, email_body):
  logger = setup_logger()
  logger.info(f"Sending email to {receiver_emails}")

  # Create the MIMEMultipart email object
  msg = MIMEMultipart()
  msg['From'] = sender_email
  msg['Subject'] = email_subject
  msg['To'] = ", ".join(receiver_emails)

  # Add email body
  body = email_body
  msg.attach(MIMEText(body, 'plain'))

  # Sending the email via Gmail's SMTP server
  try:
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:  # SSL connection
      server.set_debuglevel(1)  # Enable debug output
      server.login(sender_email, sender_email_password)
      server.sendmail(sender_email, receiver_emails, msg.as_string())
      print("Email sent successfully!")
      logger.info(f"Email sent successfully to {receiver_emails}")
  except smtplib.SMTPException as e:
    print(f"SMTP error occurred: {e}")
    logger.info(f"SMTP error occurred: {e}")
  except Exception as e:
    print(f"General error occurred: {e}")
    logger.info(f"General error occurred: {e}")


'''
{
  "Please select the relevant one": ["Parent"],
  "Coach/Guardian/Parent Name": ["Sanjay Majumder"],
  "Identification Card (IC | Passport)": ["42424242"],
  "Participant's Name": ["Supratim Majumder"],
  "Participant IC | Passport": ["84848484"],
  "Gender (M/F)": ["Male"],
  "Date of Birth": ["16/06/2002"],
  "Tel": ["9163681672"],
  "Email": ["a@gmail.com"],
  "Address (Street)": ["14, Subhas Pally, BT Road, Baranagar"],
  "Postcode": ["700108"],
  "City": ["Kolkata"],
  "State": ["WB"],
  "Emergency Contact Name": ["Pampa Majumder"],
  "Emergency Number": ["8981702261"],
  "Relationship to Participant": ["Father"],
  "Does your child have any health issues/allergies?": ["Yes"],
  "If YES to any medical conditions, please provide details": ["Re dherrr"],
  "T-Shirt Size": ["XL"],
}
'''
def fill_html_as_pdf(html_file_location, data):
  # Load the HTML file
  with open('pdf.html', 'rb') as file:
    html_content = file.read()

  # Parse the HTML using BeautifulSoup
  soup = BeautifulSoup(html_content, 'html.parser')

  terms_checkboxes = ["agree_1", "agree_2", "agree_3"]
  for term in terms_checkboxes:
    checkbox_term_input = soup.find('input', {'id': term})
    if checkbox_term_input:
      checkbox_term_input['checked'] = 'checked'

  choice_coach_input = soup.find('input', {'id': 'coach'})
  choice_parent_input = soup.find('input', {'id': 'parent'})
  choice_guardian_input = soup.find('input', {'id': 'guardian'})
  choice_senior_input = data["Please select the relevant one"][0]
  if choice_senior_input == "Coach":
    choice_coach_input['checked'] = 'checked'
  elif choice_senior_input == "Parent":
    choice_parent_input['checked'] = 'checked'
  elif choice_senior_input == "Guardian":
    choice_guardian_input['checked'] = 'checked'

  senior_name_input = soup.find('input', {'id': 'senior_name'})
  if senior_name_input:
    senior_name_input['value'] = data["Coach/Guardian/Parent Name"][0]

  senior_passport_input = soup.find('input', {'id': 'senior_passport'})
  if senior_passport_input:
    senior_passport_input['value'] = data["Identification Card (IC | Passport)"][0]

  participant_name_input = soup.find('input', {'id': 'participant_name'})
  if participant_name_input:
    participant_name_input['value'] = data["Participant's Name"][0]

  participant_passport_input = soup.find('input', {'id': 'participant_passport'})
  if participant_passport_input:
    participant_passport_input['value'] = data["Participant IC | Passport"][0]

  gender = data["Gender (M/F)"][0]
  if "M" in gender:
    gender_input = soup.find('input', {'id': 'gender_1'})
    gender_input['value'] = "M"
  elif "F" in gender:
    gender_input = soup.find('input', {'id': 'gender_2'})
    gender_input['value'] = "F"

  dob = data["Date of Birth"][0]
  dob_formatted = datetime.strptime(dob, "%m/%d/%Y").strftime("%m%d%Y")
  digits = [int(char) for char in dob_formatted]
  for i in range(1, 9):
    dob_input = soup.find('input', {'id': f'dob_{i}'})
    dob_input['value'] = digits[i - 1]

  participant_phone_input = soup.find('input', {'id': f'participant_phone'})
  if participant_phone_input:
    participant_phone_input['value'] = data["Tel"][0]

  participant_email_input = soup.find('input', {'id': 'participant_email'})
  if participant_email_input:
    participant_email_input['value'] = data["Email"][0]

  participant_address_textarea = soup.find('textarea', {'id': 'participant_address'})
  if participant_address_textarea:
    participant_address_textarea.string = data["Address (Street)"][0]

  postcode_input = soup.find('input', {'id': 'postcode'})
  if postcode_input:
    postcode_input['value'] = data["Postcode"][0]

  city_input = soup.find('input', {'id': 'city'})
  if city_input:
    city_input['value'] = data["City"][0]

  state_input = soup.find('input', {'id': 'state'})
  if state_input:
    state_input['value'] = data["State"][0]

  emergency_contact_input = soup.find('input', {'id': 'emergency_contact'})
  if emergency_contact_input:
    emergency_contact_input['value'] = data["Emergency Contact Name"][0]

  emergency_number_input = soup.find('input', {'id': 'emergency_number'})
  if emergency_number_input:
    emergency_number_input['value'] = data["Emergency Number"][0]

  relationship_to_participant_input = soup.find('input', {'id': 'relationship_to_participant'})
  if relationship_to_participant_input:
    relationship_to_participant_input['value'] = data["Relationship to Participant"][0]

  sickTrue = data["Does your child have any health issues/allergies?"][0]
  if "Yes" in sickTrue:
    yes_sick_check_input = soup.find('input', {'id': 'yes_sick_check'})
    if yes_sick_check_input:
      yes_sick_check_input['checked'] = 'checked'
    sick_desc_textarea = soup.find('textarea', {'id': 'sick_desc'})
    if sick_desc_textarea:
      sick_desc_textarea.string = data["If YES to any medical conditions, please provide details"][0]
  else:
    no_sick_check_input = soup.find('input', {'id': 'no_sick_check'})
    if no_sick_check_input:
      no_sick_check_input['checked'] = 'checked'

  tshirt_size = data["T-Shirt Size"][0]
  tshirt_size_checkboxes = ["XS", "S", "M", "L", "XL"]
  tshirt_size_choice = tshirt_size_checkboxes.index(tshirt_size)
  size_checkboxes = ["checkbox6", "checkbox7", "checkbox8", "checkbox9", "checkbox10"]
  checkbox_input = soup.find('input', {'id': size_checkboxes[tshirt_size_choice]})
  if checkbox_input:
    checkbox_input['checked'] = 'checked'

  # Save the modified HTML to a new file (or overwrite the original)
  with open(html_file_location, 'wb') as file:
    file.write(str(soup).encode("utf-8"))

  print("New HTML file created successfully!!!")
