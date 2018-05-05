FROM continuumio/anaconda

WORKDIR /usr/src/app

RUN pip install --upgrade pip
RUN pip install --upgrade setuptools
RUN pip install websocket-client argparse
RUN conda update -n base conda
RUN conda install plotly pymongo
EXPOSE 5000

RUN git clone https://github.com/silverrainb/data602-assignment3 /usr/src/app/trading

CMD [ "trading/trading/start.sh" ]