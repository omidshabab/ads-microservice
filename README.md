# Ads Recommendation Service

## Introduction

The Ads Recommendation Service is a machine learning-powered system designed to provide personalized ad recommendations to users based on their interactions and preferences. Built using FastAPI, SQLAlchemy, and PyTorch, this service leverages user activity data to train a recommendation model that predicts which ads a user is likely to engage with.

## Features

- User registration and management
- Ad creation and management
- User activity tracking
- Machine learning model for ad recommendations
- Background training of the recommendation model
- RESTful API for easy integration

## File and Folder Structure

```
.
├── app
│   ├── api
│   │   ├── v1
│   │   │   ├── endpoints
│   │   │   │   ├── ads.py
│   │   │   │   ├── training.py
│   │   │   │   └── users.py
│   │   │   ├── models.py
│   │   └── __init__.py
│   ├── config.py
│   ├── core
│   │   ├── recommendation
│   │   │   ├── features.py
│   │   │   ├── model.py
│   │   │   └── training.py
│   │   └── __init__.py
│   ├── db
│   │   ├── models
│   │   │   ├── ads.py
│   │   │   ├── users.py
│   │   │   └── user_activities.py
│   │   ├── session.py
│   │   └── __init__.py
│   ├── services
│   │   ├── ads_service.py
│   │   └── user_service.py
│   ├── core
│   │   ├── schemas
│   │   │   ├── ads.py
│   │   │   └── users.py
│   │   └── __init__.py
│   ├── main.py
│   └── __init__.py
├── tests
│   ├── test_api
│   │   ├── test_endpoints
│   │   │   ├── test_ads.py
│   │   │   └── test_users.py
│   │   └── conftest.py
│   └── __init__.py
├── .env.example
├── .gitignore
├── docker-compose.yml
├── Dockerfile
└── requirements.txt
```

## File Descriptions

- **app/**: The main application directory containing all the source code.
  - **api/**: Contains the API endpoints for the application.
    - **v1/**: Version 1 of the API.
      - **endpoints/**: Contains the FastAPI route handlers.
        - **ads.py**: Handles ad-related operations (creation, recommendations).
        - **training.py**: Manages model training operations.
        - **users.py**: Manages user-related operations (registration, preferences).
      - **models.py**: Contains Pydantic models for API responses and requests.
  - **config.py**: Configuration settings for the application, including environment variables.
  - **core/**: Contains core functionalities of the application.
    - **recommendation/**: Contains the recommendation model and training logic.
      - **features.py**: Extracts features from user activities for training.
      - **model.py**: Defines the recommendation model architecture.
      - **training.py**: Contains the logic for training the recommendation model.
  - **db/**: Database-related files.
    - **models/**: Contains SQLAlchemy models for ads, users, and user activities.
    - **session.py**: Manages database sessions and connections.
  - **services/**: Contains service classes that encapsulate business logic.
    - **ads_service.py**: Handles ad-related business logic.
    - **user_service.py**: Handles user-related business logic.
  - **core/schemas/**: Contains Pydantic schemas for data validation and serialization.
  - **main.py**: The entry point of the application, where the FastAPI app is created and configured.

- **tests/**: Contains unit and integration tests for the application.
  - **test_api/**: Contains tests for the API endpoints.
    - **test_endpoints/**: Contains individual test files for ads and users.
    - **conftest.py**: Contains fixtures and setup code for tests.

- **.env.example**: Example environment variables file for configuration.

- **.gitignore**: Specifies files and directories to be ignored by Git.

- **docker-compose.yml**: Docker Compose configuration for running the application and database.

- **Dockerfile**: Dockerfile for building the application image.

- **requirements.txt**: Lists the Python dependencies required for the application.

## Getting Started

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up the environment variables by copying `.env.example` to `.env` and updating the values.

5. Run the application:
   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 8000
   ```

6. Access the API at `http://localhost:8000/api/v1/`.

## Running Tests

To run the tests, use the following command:
```bash
pytest
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
