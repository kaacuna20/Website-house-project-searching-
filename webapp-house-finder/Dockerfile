FROM python:3.8-slim

RUN apt-get update && \
    apt-get install -y locales && \
    echo "en_US.UTF-8 UTF-8" > /etc/locale.gen && \
    locale-gen en_US.UTF-8

ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8

WORKDIR /app

COPY requirements.txt ./

RUN pip install -r requirements.txt

RUN pip install pytest

COPY . .

EXPOSE 5003

CMD ["gunicorn", "run:app", "-w", "4", "--bind", "0.0.0.0:5003"]



