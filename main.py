import os

from database import Base, engine, get_db

from fastapi import Depends, FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from models import User

from sqlalchemy.orm import Session

from utils import send_email, fill_html_as_pdf

from uuid import uuid4


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
	# Get the data sent by the Google Form
	data = await request.json()
	print("1st", data)
	print("2nd", dir(data))

	# parent_name = data['data']['Coach/Guardian/Parent Name:'][0]
	# dob = data['data']['Date of Birth:\nMonth/Day/Year\n'][0]
	# print("Debug form data:", parent_name, dob)

	# Generate a unique UUID
	user_id = str(uuid4())
	html_file_name = f"{user_id}.html"
	html_file_location = f"templates/{html_file_name}"

	# Save the user in the database
	user = User(user_id=user_id, html_file_name=html_file_name)
	db.add(user)
	db.commit()
	db.refresh(user)

	# Create an filled HTML file in the templates folder
	fill_html_as_pdf(html_file_location, data['data'])
	send_email("supratimm531@gmail.com", user_id)

	return {"user_id": user_id, "message": "User & HTML created and notification email sent"}


@app.get("/download-pdf/{user_id}", response_class=HTMLResponse)
async def download_pdf(user_id: str, request: Request):
	html_file_name = f"{user_id}.html"

	if not os.path.exists(f"templates/{html_file_name}"):
		raise HTTPException(status_code=404, detail="File not found")

	# Render the HTML template with Jinja2
	return templates.TemplateResponse(html_file_name, {"request": request})
