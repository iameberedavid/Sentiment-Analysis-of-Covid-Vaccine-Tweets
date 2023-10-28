
# Use an official Python runtime as a parent image
FROM python:3.11.4-slim

# Create and set the working directory
WORKDIR /app

# Copy the requirements.txt file into the container at /app
COPY requirements.txt /app/

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Copy the Gradio app files into the container at /app
COPY src/ /app/

# Expose the port that Gradio will use
EXPOSE 7860

# Define the command to run your Gradio app
CMD ["python", "app.py"]