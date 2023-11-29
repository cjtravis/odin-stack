FROM python:3.9

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY data_generator.py /app/

CMD ["python", "data_generator.py"]
