FROM python:3.10.0-bullseye
WORKDIR /usr/local/
ENV TZ="Europe/Amsterdam"
COPY ./ /usr/local/
RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt
CMD python app.py