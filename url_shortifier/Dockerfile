FROM python:3.8

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYHONUNBUFFERED 1

WORKDIR /usr/src/dev_proj

RUN pip install --upgrade pip

COPY ./requirements.txt /usr/src/requirements.txt

RUN pip install -r /usr/src/requirements.txt

COPY . /usr/src/dev_proj

EXPOSE 8000


ENTRYPOINT ["/usr/src/dev_proj/entrypoint.sh"]

#CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]