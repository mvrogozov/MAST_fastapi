FROM python:3.10-slim
RUN apt-get update
RUN python3 -m pip install --upgrade pip
WORKDIR /app
COPY requirements.txt /app
RUN pip3 install -r /app/requirements.txt --no-cache-dir
COPY ./ .
LABEL author='mv_rogozov'
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]