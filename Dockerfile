FROM node:lts-alpine as build

WORKDIR /opt/build
COPY package*.json .
RUN npm ci

COPY rollup.config.js .
COPY public public
COPY src src
RUN npm run build


FROM python:3.9-slim

WORKDIR /opt/app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY --from=build /opt/build/public public
COPY server server

EXPOSE 5050
CMD ["python", "-m", "server", "public"]
