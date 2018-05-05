FROM continuumio/anaconda3

WORKDIR /usr/src/app

RUN apt-get update && apt-get install -y apt-utils build-essential
RUN pip install --upgrade pip
RUN pip install --upgrade setuptools
RUN pip install websocket-client argparse
RUN conda update -n base conda
RUN conda install plotly pymongo
RUN conda remove -y statsmodels
RUN git clone git://github.com/statsmodels/statsmodels.git
RUN cd statsmodels ; python3 setup.py build ; python3 setup.py install
EXPOSE 5000

RUN git clone https://github.com/silverrainb/data602-assignment3 /usr/src/app/trading

CMD [ "trading/trading/start.sh" ]