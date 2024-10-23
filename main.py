import subprocess

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
origins = ['*']

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
	print("3rd", data.__dict__)

	# Trigger your Python script or perform some action
	subprocess.run(["python3", "script.py"])
	return {"message": "Success"}
