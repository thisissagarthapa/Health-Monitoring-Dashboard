FROM python:3.12.6-bullseye

ENV PYTHONUNBUFFERED=1

# Set WORKDIR to the parent directory
WORKDIR /django/HealthMonitoringProject

# Copy the requirements.txt file first and install dependencies
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

# Copy all project files to the container
COPY . .

# Set the WORKDIR to where the manage.py file is located
WORKDIR /django/HealthMonitoringProject/HealthMonitoringProject

# Command to run the Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]