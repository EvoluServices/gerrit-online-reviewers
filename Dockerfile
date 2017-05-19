# Use an official Python runtime as a base image
FROM python:2.7-slim

# install nmap
RUN apt-get update \
  && DEBIAN_FRONTEND=noninteractive apt-get install -y nmap \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
ADD . /app

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Run app.py when the container launches
CMD ["python", "-u", "update_online_reviewers.py"]
