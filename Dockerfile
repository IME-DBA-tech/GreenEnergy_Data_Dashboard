FROM my-devops-tools:latest AS builder

WORKDIR /app

COPY  app/requirements.txt .

RUN mkdir -p /install && \
    pip install --prefix=/install --no-cache-dir -r requirements.txt

FROM my-devops-tools:latest

RUN useradd -m myuser

WORKDIR /home/myuser/app

COPY --from=builder /install /usr/local


COPY  --chown=myuser:myuser app/ .

USER myuser

HEALTHCHECK --interval=30s --timeout=3s \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000'); exit(0)"

EXPOSE 5000

CMD ["python","app.py"]
