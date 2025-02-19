# Python image to use.
FROM python:3.12.8-slim-bullseye

# Set the working directory to /app
WORKDIR /app

ENV INSTANCE_NAME="aidemy"
#ENV REGION="us-central1"
ENV SQL_FILE="setup/curriculums.sql"
#ENV DB_USER="postgres"
#ENV DB_PASS="1234qwer"
#ENV DB_NAME="aidemy-db"


# copy the requirements file used for dependencies
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Copy the rest of the working directory contents into the container at /app
COPY . .

EXPOSE 8080

# Run app.py when the container launches
ENTRYPOINT ["python", "app.py"]