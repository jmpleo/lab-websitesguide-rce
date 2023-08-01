FROM python:3.6.10-alpine3.11

COPY websiteguide.ini /etc/supervisor.d/websiteguide.ini
COPY default.conf /etc/nginx/conf.d/default.conf

RUN mkdir /WebsiteGuide
WORKDIR /WebsiteGuide
COPY . .

RUN apk update && \
    apk add --no-cache --virtual .build-deps \
        openssl-dev \
        gcc \
        musl-dev \
        python3-dev \
        libffi-dev \
        openssh-client \
        make && \
    apk add --no-cache \
        openssh \
        nginx \
        mariadb \
        build-base \
        supervisor \
        bash && \
    pip install --upgrade pip && \
    pip install gunicorn

RUN pip install --no-index --no-cache-dir --find-links=wheelhouse -r requirements.txt && \
    apk del .build-deps

RUN adduser -S -s /bin/sh websiteguide && \
    addgroup -S websiteguide && \
    adduser websiteguide websiteguide && \
    \
    touch /var/log/supervisord.log && \
    mkdir -p /etc/supervisor.d /run/nginx /var/log/nginx && \
    chown -R nginx:nginx /run/nginx /var/log/nginx && \
    chmod -R 770 /var/log/nginx && \
    chown -R websiteguide:websiteguide /var/log/supervisord.log && \
    chown -R websiteguide:websiteguide /WebsiteGuide && \
    chown websiteguide:websiteguide /etc/supervisord.conf

RUN su -c "python3 manage.py updatedb && \
           python3 manage.py useradd -u admin -p 4HfWNI4bLJzyr9ocSGGD9rlK19Dw -s -n admin" websiteguide

RUN chmod ug+s /usr/bin/scp

EXPOSE 80
CMD nginx && supervisord -c /etc/supervisor.d/websiteguide.ini
