#Primera Etapa
FROM node:latest as node

RUN mkdir -p /app

WORKDIR /app

COPY package.json /app

RUN npm install

COPY . /app

RUN npm run build --prod

#Segunda Etapa
FROM nginx:latest

COPY --from=node /app/dist/ipscm.web-client /usr/share/nginx/html