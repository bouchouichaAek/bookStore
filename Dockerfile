# Dockerfile

# Use the official Python image from the Docker Hub
FROM python:3.11-alpine

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt /app/

# Install the dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the Django project into the container
COPY . /app

# Expose the port on which the Django app runs
EXPOSE 8000

# Run the Django development server
CMD ["python","manage.py" ,"migrate", "&&","python", "manage.py", "runserver", "0.0.0.0:8000"]
