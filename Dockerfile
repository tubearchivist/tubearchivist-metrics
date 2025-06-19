FROM python:3.11.8-slim-bookworm
WORKDIR /app
COPY tubearchivist-metrics/requirements.txt .
RUN pip3 install -r requirements.txt
COPY . .
CMD ["python3", "-u", "tubearchivist-metrics/main.py"]
