FROM python:3.13

WORKDIR /app/

ENV VIRTUAL_ENV=/env
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
RUN apt-get -y update
RUN apt-get install ffmpeg libxml2-dev libxslt-dev  -y
ENV XDG_DATA_HOME=/data
RUN mkdir -p $XDG_DATA_HOME/spotdl/.spotdl/.spotipy
RUN chmod -R 0777 $XDG_DATA_HOME/spotdl

COPY requirements.txt .

RUN pip install -r requirements.txt

ADD start.sh .
RUN chmod +X start.sh
ADD get.sh .
RUN chmod +X get.sh
ADD download.sh .
RUN chmod +X download.sh

CMD ["sleep","infinity"]