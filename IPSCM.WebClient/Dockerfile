# Primera Etapa: Construir la aplicación Angular
FROM node:latest as node

RUN mkdir -p /app
WORKDIR /app

# Copiar el archivo package.json e instalar dependencias
COPY package.json /app
RUN npm install

# Copiar el resto de los archivos y construir la aplicación Angular
COPY . /app

# Ajustar el presupuesto en el archivo angular.json
RUN sed -i 's/"maximumError": "1mb"/"maximumError": "2mb"/' /app/angular.json

RUN npm run build --prod

# Segunda Etapa: Configurar el servidor NGINX
FROM nginx:latest

# Copiar los archivos de la primera etapa al directorio del servidor NGINX
COPY --from=node /app/dist/ipscm.web-client /usr/share/nginx/html
