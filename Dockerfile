FROM python:3.11.3

RUN mkdir /fastapi_ylab
WORKDIR /fastapi_ylab

COPY ./requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt --no-cache-dir

COPY . .

#WORKDIR src
#
#CMD ["uvicorn", "main:app", "--host", "0.0.0.0"]