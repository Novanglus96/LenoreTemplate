###########
# STAGE 1 #
# Vue build
###########
# Pinned to a major rather than the floating `lts` tag on purpose: `lts` silently
# jumps majors, so rebuilding an old release tag could produce a different
# frontend bundle under the same version. If a project needs byte-reproducible
# rebuilds, pin this by digest (`node:22-alpine@sha256:...`) and accept the
# maintenance.
FROM node:22-alpine AS frontend-build

WORKDIR /app
COPY frontend/package*.json ./
RUN npm ci
COPY frontend/ .
RUN npm run build

###########
# STAGE 2 #
# Python wheels + lint
###########
FROM python:3.11.4-slim-bookworm AS backend-builder

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y --no-install-recommends gcc

RUN pip install --upgrade pip setuptools wheel
RUN pip install flake8==6.0.0
COPY backend/ /usr/src/app/
RUN flake8 --ignore=E501,F401,E203,E701,W503 ./backend

COPY backend/requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/app/wheels -r requirements.txt

###########
# STAGE 3 #
# Final single-container image
###########
FROM python:3.11.4-slim-bookworm

LABEL maintainer="John Adams"
LABEL version="0.0.0"

# nginx serves the built SPA and proxies the API; supervisord runs nginx,
# gunicorn and the django-q cluster in one container. django-q2 is configured
# with the ORM broker (see Q_CLUSTER in backend/settings.py), so no redis is
# needed — if a project switches the broker to redis, add redis-server here and
# a [program:redis] block to supervisord.conf.
RUN apt-get update && apt-get install -y --no-install-recommends \
    nginx \
    supervisor \
    netcat-openbsd \
    postgresql-client \
    curl \
    && rm -rf /var/lib/apt/lists/*

ENV HOME=/home/app
ENV APP_HOME=/home/app/web
RUN mkdir -p $APP_HOME/staticfiles $APP_HOME/mediafiles
WORKDIR $APP_HOME

# Python dependencies
COPY --from=backend-builder /usr/src/app/wheels /wheels
COPY --from=backend-builder /usr/src/app/requirements.txt .
RUN pip install --upgrade pip setuptools wheel && pip install --no-cache /wheels/*

# Vue static files
COPY --from=frontend-build /app/dist /usr/share/nginx/html

# Backend app
COPY backend/ $APP_HOME/

# Scripts
RUN sed -i 's/\r$//g' $APP_HOME/entrypoint.sh && chmod +x $APP_HOME/entrypoint.sh
RUN sed -i 's/\r$//g' $APP_HOME/start.app.sh && chmod +x $APP_HOME/start.app.sh

# Nginx config
COPY nginx/app.conf /etc/nginx/conf.d/default.conf
RUN rm -f /etc/nginx/sites-enabled/default

# Supervisord config
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

EXPOSE 80

HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost/api/v1/options/health/ || exit 1

ENTRYPOINT ["/home/app/web/entrypoint.sh"]
CMD ["/home/app/web/start.app.sh"]
