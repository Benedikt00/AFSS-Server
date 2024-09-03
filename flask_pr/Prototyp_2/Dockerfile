FROM python:3.12.2

# Set environment variables
# Set the working directory in the container
WORKDIR /

# Copy the dependencies file to the working directory
COPY requirements.txt .

# Install any needed dependencies specified in requirements.txt
RUN pip install -r requirements.txt

# Copy the rest of the application code to the working directory
COPY . ./app
#COPY Templates Templates

ENTRYPOINT [ "python" ]


# Run the Flask application
CMD ["app/__init__.py", "run", "--debug"]