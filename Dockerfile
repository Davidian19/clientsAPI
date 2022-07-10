FROM python

WORKDIR /usr/src/app

COPY clientsJsons.json .

RUN npm install

COPY . .

EXPOSE 5000

CMD ["python", "index.py"]
