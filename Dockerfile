FROM python:3.8.3-alpine

LABEL maintainer="bujarbakiu"

RUN apk add --no-cache gcc python3-dev libffi-dev musl-dev linux-headers postgresql-dev

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . app
WORKDIR /app

EXPOSE 8000

# runs the app
ENTRYPOINT ["python", "manage.py"]
CMD ["runserver", "0.0.0.0:8000"]
