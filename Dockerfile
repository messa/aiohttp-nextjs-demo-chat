FROM node:10-alpine as build_frontend
WORKDIR /frontend
COPY frontend/package.json frontend/package-lock.json ./
RUN npm install
COPY frontend ./
RUN npm run build
RUN ls -lah /frontend

FROM python:3.7-alpine as build_backend
RUN apk add --update libffi openssl
RUN apk add alpine-sdk libffi-dev openssl-dev
RUN python3 -m venv /venv
RUN /venv/bin/pip install -U pip wheel
RUN /venv/bin/pip install aiohttp aiohttp_session requests_oauthlib
RUN /venv/bin/pip install cryptography cchardet aiodns
COPY setup.py MANIFEST.in /app-src/
COPY chat_web /app-src/chat_web
COPY --from=build_frontend /frontend/out /app-src/chat_web/frontend_static
RUN test -d /app-src/chat_web/frontend_static/_next
RUN /venv/bin/pip install /app-src

FROM python:3.7-alpine
RUN apk add --update libffi openssl
COPY --from=build_backend /venv /venv
ENV ALLOW_DEV_LOGIN=1
EXPOSE 5000
CMD ["/venv/bin/chat-web"]
