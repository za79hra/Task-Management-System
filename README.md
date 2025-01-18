# Task-Management-System
# Authentication and User Management API

This project provides an authentication and user management system, including functionalities for OTP generation, user registration, login, and token management. The API allows users to register with their phone number, verify their identity with an OTP, and log in to retrieve authentication tokens for secure access to protected resources.

## Features

- **OTP Generation and Verification:** 
  - Users can request an OTP for registration.
  - OTP is sent to the user's phone and stored for verification within a time window (2 minutes).
  
- **User Registration:**
  - Users can register with their phone number, username, password, and OTP.
  - Verifies the OTP before registering the user.

- **Login and Token Generation:**
  - Users can log in using their username and password.
  - Upon successful login, users receive an access token and a refresh token.

- **Role-Based Access Control (RBAC):**
  - Supports multiple roles (e.g., `admin`, `user`) for secure access control.

## Project Structure

The project is structured into several key modules:

- **`auth.py`**: Contains the routes for sending OTP, user registration, and login.
- **`services.py`**: Handles business logic related to OTP generation, user registration, and login.
- **`utils.py`**: Contains utility functions, such as role validation and token creation.
- **`database.py`**: Manages MongoDB connections and provides database operations like storing OTPs and user data.
- **`task_dao.py`**: Provides functions for interacting with tasks stored in MongoDB.

## Setup and Installation

### Prerequisites

Ensure that you have the following installed:

- Python 3.8+
- MongoDB
- Docker (for optional containerization)

### Installation Steps

1. Clone the repository:

    ```bash
    git clone https://github.com/your-username/Task-Management-System.git
    cd Task-Management-System
    ```

2. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3. Configure your MongoDB connection and secret keys in an `.env` file or environment variables.

4. Start the application:

    ```bash
    uvicorn main:app --reload
    ```

    The API will now be running at `http://127.0.0.1:8000`.

## API Endpoints

### `POST /send-otp`

- **Description**: Sends an OTP to a user's phone for registration.
- **Request Body**: 

    ```json
    {
      "phone": "+989XXXXXXXXX"
    }
    ```

- **Response**:

    ```json
    {
      "message": "OTP sent successfully",
      "otp": "123456",
      "status_code": 200
    }
    ```

### `POST /register`

- **Description**: Registers a new user with phone number, username, password, and OTP.
- **Request Body**:

    ```json
    {
      "phone": "+989XXXXXXXXX",
      "username": "johndoe",
      "password": "password123",
      "otp": "123456",
      "role": "user"
    }
    ```

- **Response**:

    ```json
    {
      "message": "User registered successfully",
      "status_code": 200
    }
    ```

### `POST /token`

- **Description**: Logs in the user and provides an access token and refresh token.
- **Request Body**:

    ```json
    {
      "username": "johndoe",
      "password": "password123"
    }
    ```

- **Response**:

    ```json
    {
      "access_token": "access_token_string",
      "refresh_token": "refresh_token_string",
      "token_type": "bearer"
    }
    ```

## Authentication

Tokens are issued as JWT (JSON Web Tokens). The `access_token` is used for accessing protected resources, and the `refresh_token` can be used to obtain a new access token when the current one expires.

### Token Verification

To verify the token in requests, you can use the `role_required` function that checks whether the user has the necessary role (e.g., `admin`, `user`).

Example of verifying a token in an endpoint:

```python
from fastapi import Depends
from utils import role_required

@app.get("/admin-data")
async def get_admin_data(token: str = Depends(role_required('admin'))):
    return {"message": "Access granted to admin data"}
```
## Database

The project uses MongoDB for storing user information and OTPs. The `MongoConnection` class handles database operations, including:

- Inserting and updating user data.
- Storing OTP data with expiration.

Ensure MongoDB is running locally or configure it for remote access.

## Logging

The project uses Python's built-in `logging` module to log important events like token validation, role access checks, and database operations. Logs can be found in the console or redirected to a file.

## Tests

To ensure the correct functionality of the API, you can write and run tests using `pytest`.

### Example Test

```python
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_send_otp():
    response = client.post("/send-otp", json={"phone": "+989XXXXXXXXX"})
    assert response.status_code == 200
    assert "otp" in response.json()
```

### Contributing
We welcome contributions to improve this project! Please fork the repository and submit a pull request with your changes. Be sure to follow the existing code style and write tests for any new features or bug fixes.


