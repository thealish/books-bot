FROM python: 3.7.9


WORKDIR /src
COPY requirements.txt /src
RUN pip install -r requirements.txt
COPY . /src