FROM python:3.8.1-slim-buster

ENV WORKDIR=/usr/src/app
ENV USER=app
ENV APP_HOME=/home/app/web
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
ENV GOOGLE_APPLICATION_CREDENTIALS="./core/googleAccount.json"

WORKDIR $WORKDIR

RUN pip install --upgrade pip 
RUN apt-get update && apt-get install -y gnupg2 && apt-get install -y curl

RUN echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] http://packages.cloud.google.com/apt cloud-sdk main" | tee -a /etc/apt/sources.list.d/google-cloud-sdk.list && curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key --keyring /usr/share/keyrings/cloud.google.gpg  add - && apt-get update -y && apt-get install google-cloud-sdk -y
RUN gcloud auth activate-service-account --key-file ${GOOGLE_APPLICATION_CREDENTIALS}
RUN gcloud config set project snap-n-paste

COPY ./requirements.txt $WORKDIR/requirements.txt
RUN pip install -r requirements.txt
RUN adduser --system --group $USER
RUN mkdir $APP_HOME
WORKDIR $APP_HOME

COPY . $APP_HOME
RUN chown -R $USER:$USER $APP_HOME
USER $USER

EXPOSE 80
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]


