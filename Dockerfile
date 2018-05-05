FROM mongo:3.6

WORKDIR /usr/src/app

RUN apt-get update && apt-get install -y --no-install-recommends apt-utils && \
 apt-get install -y python3 python3-pip git

COPY requirements.txt ./

RUN pip3 install --upgrade pip
RUN pip3 install --upgrade setuptools
RUN pip3 install --no-cache-dir -r requirements.txt
EXPOSE 5000

RUN git clone https://github.com/silverrainb/data602-assignment2 /usr/src/app/trading

CMD [ "trading/trading/start.sh" ]
