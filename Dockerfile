# Define build arguments
ARG APP_PATH="/src"
ARG PYTHON_IMAGE="python:3.12-slim"

# Build stage
FROM ${PYTHON_IMAGE} AS build

ARG APP_PATH
WORKDIR ${APP_PATH}

# Install system dependencies for build
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        libpq-dev \
        curl \
        git \
        pkg-config \
    && pip install --upgrade pip \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Configure Poetry
ENV POETRY_HOME="/opt/poetry" \
    POETRY_VERSION=1.8.4 \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_NO_INTERACTION=1 \
    PATH="/opt/poetry/bin:$PATH"

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Install dependencies
COPY pyproject.toml poetry.lock ./
RUN poetry install --no-interaction --no-ansi && rm -rf /root/.cache/pypoetry/*

# Production stage
FROM ${PYTHON_IMAGE}

ARG APP_PATH
WORKDIR ${APP_PATH}

# Configure Python environment
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH=${APP_PATH}

# Copy necessary files from build stage
COPY --from=build /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=build /usr/lib/x86_64-linux-gnu/libpq.so.5 /usr/lib/x86_64-linux-gnu/

# Copy application code
COPY . .

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
