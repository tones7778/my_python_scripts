from fastapi import FastAPI
import uvicorn

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

if __name__ == "__main__": # python main.py
    uvicorn.run("main:app", host="0.0.0.0", port=9002, log_level="info")


# gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:9001 --reload


myapp.service

[Unit]
Description=Gunicorn instance to serve Fastapi on port 9002
After=network.target

[Service]
User=root
Group=root
WorkingDirectory=/home/tones/Downloads/code/fastapi-poc-to-prd
Environment="PATH=/home/tones/Downloads/code/fastapi-poc-to-prd/venv/bin"
ExecStart=/home/tones/Downloads/code/fastapi-poc-to-prd/venv/bin/gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:9002

[Install]
WantedBy=multi-user.target
