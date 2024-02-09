FROM python:latest

RUN python3 -m venv venv
RUN python -m ensurepip
RUN python3 -m pip install discord.py asyncio pyprobs typing enum34 requests googletrans==3.1.0a0 babel

WORKDIR /data

COPY main.py /
COPY tool.py /
COPY private.json /
COPY base.py /
RUN chmod a+x /main.py
RUN chmod a+x /tool.py

CMD python3 /main.py & python3 /tool.py