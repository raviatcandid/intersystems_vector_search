# Vector Search with LLM in InterSystems IRIS

## Overview
This project demonstrates a Vector Search application using Large Language Models (LLMs) integrated with InterSystems IRIS. The application is built using Streamlit and leverages OpenAI's API for natural language processing tasks.

## Project Structure
```
tree .
.
├── app
│   ├── docker-compose.yaml
│   └── streamlit
│       ├── combined_code.py
│       ├── constants.py
│       ├── db_operations.py
│       ├── Dockerfile
│       ├── helper.py
│       ├── main.py
│       ├── openai_llm.py
│       └── requirements.txt
├── jupyter_notebooks
│   ├── intersystems_vector_search.ipynb
│   └── sample_data
│       ├── example_Imatinib_Teva.pdf
│       ├── large_document.txt
│       └── small_data.txt
└── README.md
```

## Prerequisites
Ensure you have the following installed on your local machine:
- Docker
- Docker Compose

## Getting Started
- Clone the Repository
- git clone https://github.com/mychoys-co/intersystems_vector_search
- cd app

## Set Up Environment Variables
Create a .env file in the root directory of your project and add the following environment variables:
```
IRIS_USERNAME=demo
IRIS_PASSWORD=demo
IRIS_HOSTNAME=intersystems
IRIS_PORT=1972
IRIS_TABLE_NAME=intersystems_table
IRIS_NAMESPACE=USER
OPENAI_API_KEY=<your-openai-api-key>
```

## Build and Run the Application
Run the following command to build and start the services:
`
docker compose up --build
`

## This will start two services:
- InterSystems IRIS: Runs on ports 1972 and 52773.
- Streamlit App: Runs on ports 8501 and 8502.

## Access the Application
Once the services are up and running, you can access the Streamlit application by navigating to:
`
http://localhost:8501
`

## Usage

### Uploading Files
You can upload a .pdf or .txt file through the Streamlit interface.
The file content will be processed and inserted into the InterSystems IRIS database.

### Asking Questions
Enter your question in the provided input box and click the Submit button.
The application will generate a response to your question using OpenAI's API and display relevant search results from the InterSystems IRIS database.

## Project Components

### docker-compose.yaml
Defines the services required for the application: intersystems (IRIS) and app (Streamlit application).

### streamlit/Dockerfile
Specifies the Docker image for the Streamlit application, including the installation of necessary dependencies and models.

### streamlit/main.py
Contains the main Streamlit application code, which handles file uploads, data processing, and querying.

### streamlit/db_operations.py
Handles database operations such as verifying table existence, inserting data, and counting records.

### streamlit/combined_code.py
Combines various functionalities such as initializing the database, inserting data, and generating responses to user queries.

### streamlit/openai_llm.py
Handles interactions with OpenAI's API for natural language processing tasks.

### streamlit/requirements.txt
Lists the Python dependencies required for the Streamlit application.

### streamlit/constants.py and streamlit/helper.py
Contain various helper functions and constants used throughout the application.

## Notes
Ensure that the InterSystems IRIS container is fully up and running before attempting to use the Streamlit application.
The sleep 40 command in the Docker configuration ensures that the IRIS service has enough time to start before the application attempts to connect.

## Troubleshooting
If you encounter any issues, check the logs of both containers using the following command:
`
docker-compose logs
`
