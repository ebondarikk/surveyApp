FROM python:3.8-alpine3.13

ARG workdir=/var/www/survey
ARG user=survey

WORKDIR ${workdir}

COPY requirements.txt .

RUN adduser -D ${user} \
    && chown -R ${user}:${user} ${workdir} \
    && apk add --virtual .build-deps musl-dev gcc postgresql-dev libffi-dev cargo rust \
    && apk add postgresql-libs curl-dev libcurl \
        jpeg-dev \
        zlib-dev \
        wkhtmltopdf-dev \
        freetype-dev \
        lcms2-dev \
        openjpeg-dev \
        tiff-dev \
        tk-dev \
        tcl-dev \
        harfbuzz-dev \
        fribidi-dev \
    && chown -R ${user}:${user} ${workdir} \
    && pip install --upgrade pip \
    && pip install -r requirements.txt

COPY docker-entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/docker-entrypoint.sh
RUN chown ${user}:${user} /usr/local/bin/docker-entrypoint.sh


USER survey

COPY . .

ENTRYPOINT [ "/usr/local/bin/docker-entrypoint.sh" ]
