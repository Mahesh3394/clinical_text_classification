FROM python:3.8

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN useradd -m -u 1000 user

USER user
ENV HOME=/home/user \
	PATH=/home/user/.local/bin:$PATH

WORKDIR $HOME/app

COPY --chown=user . $HOME/app


CMD ["gunicorn", "-w", "1", "-b", "0.0.0.0:7860", "app:app"]

# CMD ["python", "app.py"]