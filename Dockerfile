# Python 3.11-slim イメージをベースに使用
FROM python:3.11-slim

# 作業ディレクトリを設定
WORKDIR /src

# 必要なシステムパッケージをインストール
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        libpq-dev \
        curl && \
    rm -rf /var/lib/apt/lists/*

# Poetry のインストール
ENV PATH="/root/.local/bin:${PATH}"
RUN curl -sSL https://install.python-poetry.org | python3 - && \
    poetry config virtualenvs.create false

# Poetry の設定と依存関係のインストール
COPY pyproject.toml poetry.lock ./
RUN poetry install

# アプリケーションコードをコピー
COPY . .

# 環境変数の設定
ENV PYTHONUNBUFFERED 1

# ポートを公開
EXPOSE 8000

# 開発サーバーを起動
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
