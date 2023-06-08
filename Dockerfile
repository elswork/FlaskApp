FROM python:3-alpine3.18 

ARG BUILD_DATE
ARG VCS_REF
ARG VERSION
LABEL mantainer="Eloy Lopez <elswork@gmail.com>" \
    org.label-schema.build-date=$BUILD_DATE \
    org.label-schema.name="FlaskApp" \
    org.label-schema.description="Python3 and Flask App" \
    org.label-schema.url="https://deft.work" \
    org.label-schema.vcs-ref=$VCS_REF \
    org.label-schema.vcs-url="https://github.com/DeftWork/FlaskApp" \
    org.label-schema.vendor="Deft Work" \
    org.label-schema.version=$VERSION \
    org.label-schema.schema-version="1.0"

COPY src /src/

RUN pip install -r /src/requirements.txt

EXPOSE 5000

ENTRYPOINT [ "/bin/sh", "/src/start.sh" ]