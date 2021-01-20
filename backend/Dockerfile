FROM python:alpine

ENV FLASK_APP annotation.py

WORKDIR /opt/labeling-tool

COPY requirements.txt ./requirements/
RUN pip install --no-cache-dir -r ./requirements/requirements.txt

COPY app app
COPY annotation.py config.py wsgi.py gunicorn.py ./

EXPOSE 5000

CMD ["gunicorn", "-c", "gunicorn.py", "annotation:app"]
