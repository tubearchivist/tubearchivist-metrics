FROM python:3.11.13-slim-bookworm
WORKDIR /app
COPY tubearchivist-metrics/requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "-u", "tubearchivist-metrics/main.py"]
