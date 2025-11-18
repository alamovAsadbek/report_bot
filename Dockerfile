FROM python:3.11

# Set working directory
WORKDIR /bot

# Copy project files
COPY . .

# Install dependencies
RUN pip install -r requirements.txt

# Expose necessary ports (optional)
EXPOSE 5000

# Run the bot
CMD ["python", "main.py"]
