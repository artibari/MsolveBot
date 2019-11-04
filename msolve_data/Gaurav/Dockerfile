FROM python:3.5
RUN pip install requests
WORKDIR /app
copy send_mail_trail.py .
expose 5000
cmd ["python", "app.py"]