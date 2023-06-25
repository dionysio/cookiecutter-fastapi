# Use the Python 3.11 base image
FROM python:3.11-slim-buster

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Set the working directory in the container
WORKDIR /app

# Copy the project files into the container
COPY . .

# Install the project dependencies using Poetry
RUN poetry install --no-root --no-interaction --no-ansi

# Set the environment variables
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# Expose the port on which the application will run
EXPOSE 8000

# Use gunicorn as the web server to handle requests
CMD ["poetry", "run", "gunicorn", "main:app", "--bind", "0.0.0.0:8000", "--workers", "4", "--worker-class", "uvicorn.workers.UvicornWorker"]
