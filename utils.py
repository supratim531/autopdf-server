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


{'data': {'City': ['NA'], 'Coach/Guardian/Parent Name:': ['Sanjay Majumder'], "Child's Name:": ['Supratim Majumder'], 'Identification Card No (IC | Passport):': ['NA'], 'Please select the relevant one:\n\n': ['Guardian'], 'Relationship to Participant': ['NA'], 'State': ['NA'], 'Gender (M/F):': ['Male'], 'Email': ['NA'], 'Emergency Contact Number': ['NA'], 'Address': ['NA'], 'Date of Birth\nMonth/Day/Year\n': ['30/10/2024'], 'Tel': ['NA'], 'Timestamp': ['26/10/2024 04:59:59']}}
def fill_html_as_pdf(html_file_location, data):
  # Load the HTML file
  with open('pdf.html', 'rb') as file:
    html_content = file.read()

  # Parse the HTML using BeautifulSoup
  soup = BeautifulSoup(html_content, 'html.parser')

  terms_checkboxes = ["checkbox1", "checkbox2", "checkbox3"]
  for term in terms_checkboxes:
    checkbox_term_input = soup.find('input', {'id': term})
    if checkbox_term_input:
      checkbox_term_input['checked'] = 'checked'

  # Find the input field by its id and set the value for "Name"
  name_input = soup.find('input', {'id': 'child_full_name'})
  if name_input:
    name_input['value'] = data["Child's Name"][0]

  passport = data["Identification Card No (IC | Passport)"][0]
  passport_digits = [int(char) for char in passport if char.isdigit()]
  for i in range(1, 11):
    passport_input = soup.find('input', {'id': f'num_{i}'})
    passport_input['value'] = passport_digits[i - 1]

  gender = data["Gender (M/F)"][0]
  if "M" in gender:
    gender_input = soup.find('input', {'id': 'gender_1'})
    gender_input['value'] = "M"
  elif "F" in gender:
    gender_input = soup.find('input', {'id': 'gender_2'})
    gender_input['value'] = "F"
  else:
    pass

  dob = data['Date of Birth'][0]
  digits = [int(char) for char in dob if char.isdigit()]
  for i in range(1, 9):
    dob_input = soup.find('input', {'id': f'dob_{i}'})
    dob_input['value'] = digits[i - 1]

  phone = data["Tel"][0]
  phone_digits = [int(char) for char in phone if char.isdigit()]
  for i in range(1, 11):
    phone_input = soup.find('input', {'id': f'phn_{i}'})
    phone_input['value'] = phone_digits[i - 1]

  email_input = soup.find('input', {'id': 'email'})
  if email_input:
    email_input['value'] = data["Email"][0]

  postcode = "1234"
  postcode_digit = [int(char) for char in postcode if char.isdigit()]
  for i in range(1, 5):
    postcode_input = soup.find('input', {'id': f'post_{i}'})
    postcode_input['value'] = postcode_digit[i-1]

  city_input = soup.find('input', {'id': 'city'})
  if city_input:
    city_input['value'] = data["City"][0]

  state_input = soup.find('input', {'id': 'state'})
  if state_input:
    state_input['value'] = data["State"][0]

  name_em_input = soup.find('input', {'id': 'name_em'})
  if name_em_input:
    name_em_input['value'] = "Arpan Ghosh"

  name_rel_input = soup.find('input', {'id': 'name_rel'})
  if name_rel_input:
    name_rel_input['value'] = data["Relationship to Participant"][0]

  telephone = data["Emergency Contact Number"][0]
  telephone_digits = [int(char) for char in telephone if char.isdigit()]
  for i in range(1, 11):
    telephone_input = soup.find('input', {'id': f'tel_{i}'})
    telephone_input['value'] = telephone_digits[i - 1]

  sickTrue = "Yes"
  if "Yes" in sickTrue:
    sick_input= soup.find('input', {'id': 'checkbox4'})
    if sick_input:
      sick_input['checked'] = 'checked'
    sick_input_desc= soup.find('input', {'id': 'sick_desc'})
    sick_input_desc['value'] = "I am sick"
  else:
    sick_input= soup.find('input', {'id': 'checkbox5'})
    if sick_input:
      sick_input['checked'] = 'checked'

  size_checkboxes=["checkbox6", "checkbox7", "checkbox8", "checkbox9", "checkbox10"]
  choice = 2
  checkbox_input = soup.find('input', {'id': size_checkboxes[choice-1]})

  if checkbox_input:
    checkbox_input['checked'] = 'checked'

  #doubt
  # addresses = "Maruti Plaza Flat-3A, 244 Gorakshabasi Road, Nagerbaazar South Dumdum(M)"
  addresses = data["Address"][0]
  address = addresses.split(',', 3)
  # print (address)
  for i in range(len(address)):  # Use the length of the address list
    address_input = soup.find('input', {'id': f'address_{i}'})
    if address_input:  # Check if the input exists
      address_input['value'] = address[i].strip()  # Use .strip() to remove leading/trailing spaces
    else:
      pass

  # Save the modified HTML to a new file (or overwrite the original)
  with open(html_file_location, 'wb') as file:
    file.write(str(soup).encode("utf-8"))

  print("New HTML file created successfully!!!")
