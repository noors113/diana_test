# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set environment variables for Python
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /usr/src/app

# Install Poetry
RUN pip install poetry

# Copy only the dependencies file to the working directory
COPY pyproject.toml poetry.lock ./

# Install project dependencies
RUN poetry config virtualenvs.create false && \
    poetry install --without dev --no-root --all-extras

# Copy the current directory contents into the container at /usr/src/app
COPY . .

# Expose the port that Django will run on
EXPOSE 8000

# Define the default command to run when the container starts
CMD ["gunicorn", "diana_tst.wsgi:application", "--bind", "0.0.0.0:8000"]
