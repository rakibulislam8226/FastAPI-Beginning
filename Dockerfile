FROM        python:3

ENV         PYTHONUNBUFFERED=1

WORKDIR     /home

COPY        ./requirements.txt .

# COPY        * .

RUN         pip install -r requirements.txt


EXPOSE      8001

CMD         ["uvicorn", "--reload", "auth.main:app"]