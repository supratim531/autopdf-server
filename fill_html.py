from bs4 import BeautifulSoup

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
