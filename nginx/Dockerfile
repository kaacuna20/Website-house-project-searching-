FROM nginx:latest

RUN mkdir -p /etc/nginx/ssl

COPY ./ssl/cert.pem /etc/nginx/ssl/cert.pem
COPY ./ssl/key.pem /etc/nginx/ssl/key.pem


RUN chmod 700 /etc/nginx/ssl/

COPY nginx.conf /etc/nginx/nginx.conf

EXPOSE 80 443