import os

from database import Base, engine, get_db

from dotenv import load_dotenv

from fastapi import Depends, FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from models import User

from sqlalchemy.orm import Session

from utils import send_email, fill_html_as_pdf

from uuid import uuid4


# Load environment variables from .env file
load_dotenv()
admin_email = os.getenv("ADMIN_EMAIL")
backend_url = os.getenv("BACKEND_URL")

# Initialize FastAPI app
app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Create the database tables
Base.metadata.create_all(bind=engine)

app.mount("/static", StaticFiles(directory="static"), name="static")

app.add_middleware(
	CORSMiddleware,
  allow_credentials=True,
	allow_origins=['*'],
  allow_methods=["*"],
  allow_headers=["*"],
)


@app.get("/")
async def read_root():
	return {"message": "Welcome to FastAPI server"}


@app.get("/health")
async def health():
	return {"message": "FastAPI server is up & running"}


@app.post("/form-submit")
async def form_submit(request: Request, db: Session = Depends(get_db)):
	try:
		# Get the data sent by the Google Form
		data = await request.json()
		print("user-data:", data)
		print("metadata of user-data:", dir(data))

		# email = data['data']['Email'][0]
		# print("Check user's email:", email)

		# Generate a unique UUID
		user_id = str(uuid4())
		html_file_name = f"{user_id}.html"
		html_file_location = f"templates/{html_file_name}"

		# Save the user in the database
		user = User(user_id=user_id)
		db.add(user)
		db.commit()
		db.refresh(user)

		# Create an filled HTML file in the templates folder
		fill_html_as_pdf(html_file_location, data['data'])

		# After creation send the email to both user & admin
		send_email(
			["supratimm531@gmail.com"],
			f'Hi, please find the filled pdf at {backend_url}/download-pdf/{user.user_id}'
		)
		send_email(
			[admin_email],
			f'{"supratimm531@gmail.com"} submitted the "MILO Kem Juara 2024 Entry Form". Find the filled pdf at {backend_url}/download-pdf/{user.user_id}'
		)

		return {"user_id": user_id, "message": "HTML file is created and notification email sent"}
	except Exception as e:
		print("error occurred after form submission:", e)
		send_email(
			[admin_email],
			f'Something went wrong when {"supratimm531@gmail.com"} submitted the "MILO Kem Juara 2024 Entry Form"'
		)
		raise HTTPException(status_code=500, detail="Error occurred after form submission")


@app.get("/download-pdf/{user_id}", response_class=HTMLResponse)
async def download_pdf(user_id: str, request: Request):
	html_file_name = f"{user_id}.html"

	if not os.path.exists(f"templates/{html_file_name}"):
		raise HTTPException(status_code=404, detail="File not found")

	# Render the HTML template with Jinja2
	return templates.TemplateResponse(html_file_name, {"request": request})
