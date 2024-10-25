import subprocess

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from fastapi.responses import HTMLResponse

from fastapi.templating import Jinja2Templates

from fastapi.staticfiles import StaticFiles

from utils import send_email, fill_html_as_pdf

app = FastAPI()
origins = ['*']
templates = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory="static"), name="static")

app.add_middleware(
	CORSMiddleware,
	allow_origins=origins,
  allow_credentials=True,
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
async def form_submit(request: Request):
	data = await request.json()  # Get the data sent by the Google Form
	print("1st", data)
	print("2nd", dir(data))

	parent_name = data['data']['Coach/Guardian/Parent Name:'][0]
	dob = data['data']['Date of Birth:\nMonth/Day/Year\n'][0]
	print("Debug form data:", parent_name, dob)
	# fill_html_as_pdf(name, email)
	# send_email(email)

	# Trigger your Python script or perform some action
	subprocess.run(["python3", "script.py"])
	return {"message": "Success"}

@app.get("/download-pdf", response_class=HTMLResponse)
async def download_pdf(request: Request):
	return templates.TemplateResponse("download_pdf.html", {"request": request})
