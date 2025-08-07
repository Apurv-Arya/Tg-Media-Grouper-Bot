FROM python:3.10-slim-bullseye

# Set the working directory in the container.
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application's code into the container at /app
COPY . .

ENV TELEGRAM_BOT_TOKEN=""

CMD ["python", "main.py"]
