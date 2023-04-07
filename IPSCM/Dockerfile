# start by pulling the python image
FROM python:3.11-alpine

# copy the requirements file into the image

WORKDIR /app
COPY . /app

# switch working directory

#ENV FLASK_APP=app.py
#ENV FLASK_RUN_HOST=0.0.0.0
RUN apk add --no-cache gcc musl-dev linux-headers
# install the dependencies and packages in the requirements file
RUN pip install -U pip && pip install -r requirements.txt


EXPOSE 5000
CMD ["python", "app.py"]