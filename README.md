# Setup Guide

Follow these steps to set up the project:

## Installation Steps

### 1. Clone the Repository
```bash
git clone https://github.com/klinucsd/wenokn
```

### 2. Download and Setup Vector Databases

#### Data Commons Vector DB
Download and unzip the Data Commons vector database:
```bash
# Download from: https://hubbub.sdsc.edu/.test/data_commons.zip
# Extract the downloaded file to your project directory
```

#### WENOKN Vector DB
Download and extract the WENOKN vector database:
```bash
# Download from: https://hubbub.sdsc.edu/.test/wenokn.zip
# Extract the downloaded file to your project directory
```

### 3. Install Dependencies
Install the required Python libraries:
```bash
pip install -r requirements.txt
```

### 4. Configure Environment
Edit the `.env` file to configure your environment settings. Make sure to include:
```env
OPENAI_KEY=your_openai_api_key_here
```

### 5. Test Installation
Run the test to verify everything is working correctly:
```bash
python -m smart_query.test.data_system_test.py
```

## Running as FastAPI (Optional)

You can optionally run the system as a web API using FastAPI:

### Prerequisites
Ensure you have completed all the installation steps above, particularly:
- Vector databases are downloaded and extracted
- Dependencies are installed
- Environment variables are configured

### Starting the FastAPI Server

#### Option 1: Direct Python execution
```bash
python main.py
```

#### Option 2: Using uvicorn directly
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### Accessing the API

Once the server is running, you can:

- **Interactive API Documentation**: Visit `http://localhost:8000/docs` for Swagger UI
- **Query Endpoint**: `http://localhost:8000/api/v1/query?query=your_question_here`

### Example API Usage

#### Using curl:
```bash
# Example query
curl "http://localhost:8000/api/v1/query?query=What is the population of California?"
```

#### Using Python requests:
```python
import requests

# Make a query
response = requests.get(
    "http://localhost:8000/api/v1/query",
    params={"query": "What is the population of California?"}
)
print(response.json())
```

### API Response Format
The API returns JSON responses in the following format:
```json
{
  "query": "Your original query",
  "result": "JSON formatted data result",
  "status": "success"
}
```

### Production Deployment
For production deployment, consider:
- Using a production ASGI server like Gunicorn with Uvicorn workers
- Setting up proper logging and monitoring
- Configuring SSL/TLS certificates
- Setting up load balancing if needed

## Notes
- Make sure you have Python and pip installed on your system
- Ensure you have sufficient storage space for the vector databases
- Check that all file paths are correctly configured in your `.env` file
- For FastAPI deployment, ensure your OpenAI API key is properly configured in the environment