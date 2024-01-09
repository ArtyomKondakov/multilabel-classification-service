FROM ubuntu:20.04


RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    python3-pip \
    make \
    wget \
    ffmpeg \
    libsm6 \
    libxext6


WORKDIR /planets_service

COPY requirements.txt requirements.txt

RUN pip --no-cache-dir install -r  requirements.txt -f https://download.pytorch.org/whl/torch_stable.html

COPY . /planets_service/

CMD make run_app
