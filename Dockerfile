# FROM python:3.8.3-alpine

# LABEL maintainer="bujarbakiu"

# WORKDIR /usr/src/app

# # set environment variables
# ENV PYTHONDONTWRITEBYTECODE 1
# ENV PYTHONUNBUFFERED 1

# # RUN apk add --no-cache gcc python3-dev libffi-dev musl-dev linux-headers postgresql-dev

# # COPY requirements.txt requirements.txt
# # RUN pip install --no-cache-dir -r requirements.txt

# # COPY . app
# # WORKDIR /app

# # EXPOSE 8000



# # install psycopg2 dependencies
# RUN apk update \
#     && apk add postgresql-dev gcc python3-dev musl-dev

# RUN pip install --upgrade pip
# COPY ./requirements.txt .
# RUN pip install -r requirements.txt

# # copy project
# COPY . .

# # runs the app
# ENTRYPOINT ["python", "manage.py"]
# CMD ["runserver", "127.0.0.1:8000"]

FROM python:3.8.3-alpine

LABEL maintainer="bujarbakiu"

RUN mkdir /code

WORKDIR /code

COPY requirements.txt /code/

# install psycopg2 dependencies
RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev
RUN pip install --upgrade pip


# Install the requirements.
RUN pip install -r requirements.txt

# Copy the rest of the code. 
COPY . /code/

ENTRYPOINT ["/code/entrypoint.sh"]