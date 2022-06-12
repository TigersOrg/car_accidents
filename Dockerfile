FROM python:3

ENV FLASK_ENV=development
ENV JWT_SECRET_KEY=somekeyyouneverguess

ADD . /app
COPY . /app
WORKDIR /app

COPY requirements.txt ./
RUN pip install -r requirements.txt


CMD ["flask", "run", "--host", "0.0.0.0"]
