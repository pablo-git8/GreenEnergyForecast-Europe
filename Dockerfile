# Use an official Python runtime as a parent image
FROM python:3.11

# Set the working directory in the container to /entsoe_pipeline
WORKDIR /entsoe_pipeline

# Copy the necessary directories and files into the container
COPY src/ /entsoe_pipeline/src/
COPY data/ /entsoe_pipeline/data/
COPY models/ /entsoe_pipeline/models/
COPY requirements.txt /entsoe_pipeline/
COPY scripts/*.sh /entsoe_pipeline/

# Give execute permission to the scripts
RUN chmod +x /entsoe_pipeline/*.sh

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Set environment variables for sensitive data
# These should be passed when running the container
ENV ENTSOE_API_URL=""
ENV ENTSOE_SECURITY_TOKEN=""

# Command to run the default pipeline script
CMD ["./run_pipeline.sh"]

