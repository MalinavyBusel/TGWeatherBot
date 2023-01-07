FROM python:3 as base

ADD . .

RUN pip install -r requirements.txt

CMD ["python", "main.py"]
