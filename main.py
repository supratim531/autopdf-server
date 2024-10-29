import os

from database import Base, engine, get_db

from fastapi import Depends, FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from models import User

from sqlalchemy.orm import Session

from utils import send_email, setup_logger, fill_html_as_pdf

from uuid import uuid4


logger = setup_logger()

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
		logger.info(f"user-data: {data}")
		logger.info(f"metadata of user-data: {dir(data)}")

		email_address = data['data']['Email Address'][0]
		logger.info(f"Check user's email: {email_address}")

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
		logger.info(f"The filled pdf will be at {backend_url}/download-pdf/{user.user_id}")

		# After creation send the email to both user & admin
		send_email(
			[email_address],
			f'Hi, please find the filled pdf at {backend_url}/download-pdf/{user.user_id}'
		)
		send_email(
			[admin_email],
			f'{email_address} submitted the "MILO Kem Juara 2024 Entry Form". Find the filled pdf at {backend_url}/download-pdf/{user.user_id}'
		)

		return {"user_id": user_id, "message": "HTML file is created and notification email sent"}
	except Exception as e:
		logger.info(f"error occurred after form submission: {e}")
		send_email(
			[admin_email, email_address],
			f'Something went wrong when "MILO Kem Juara 2024 Entry Form" submitted from {email_address}'
		)
		raise HTTPException(status_code=500, detail="Error occurred after form submission")


@app.get("/download-pdf/{user_id}", response_class=HTMLResponse)
async def download_pdf(user_id: str, request: Request):
	html_file_name = f"{user_id}.html"

	if not os.path.exists(f"templates/{html_file_name}"):
		logger.info(f"File not found at requested path: {backend_url}/download-pdf/{user_id}")
		raise HTTPException(status_code=404, detail="File not found")

	logger.info(f"File found at requested path: {backend_url}/download-pdf/{user_id}")
	return templates.TemplateResponse(html_file_name, {"request": request})
