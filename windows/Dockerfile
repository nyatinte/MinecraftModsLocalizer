FROM mcr.microsoft.com/windows/servercore:ltsc2019
ENV chocolateyVersion=1.4.0

# Chocolateyのインストール
RUN powershell -Command "Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))"

# Pythonのインストール
RUN powershell -Command "choco install -y python --version 3.12.0"

RUN powershell -Command "choco install -y vcredist140"

# ホストマシンのコードをコンテナにコピー
COPY ./src /app/src
WORKDIR /app/src

# 依存関係のインストール
RUN pip install --no-cache-dir pyzipper requests pyinstaller TkEasyGUI litellm

# tkinterのインストール確認（pipで明示的にインストール）
RUN pip install tk || echo "tkinter already included in python distribution"

# PyInstallerでビルドする場合の例（コメントアウト）
# RUN pyinstaller main.py --onefile --clean --console --distpath /app/dist --workpath /app/build --specpath /app