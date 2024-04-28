# Use the official Python image as a base
FROM python:3.11

# Set environment variable to prevent buffering issues
ENV PYTHONUNBUFFERED 1

# Set the working directory inside the container
WORKDIR /code

# Copy the requirements file into the container at /code/
COPY requirements.txt /code/

# Install project dependencies
RUN pip install -r requirements.txt

# Copy the current directory contents into the container at /code/
COPY . /code/

# Run Django migrations
# RUN python manage.py migrate

# Expose port 8000 to access the Django development server
EXPOSE 8000

# Command to run the Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]