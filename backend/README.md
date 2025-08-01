# Quiz Master V2 - Backend

This is the backend for the Quiz Master V2 application. It is a multi-user application that acts as an exam preparation site for multiple courses.

## Features

-   **User Management:** Registration and login for users, with a pre-existing admin account.
-   **Role-Based Access Control:** Admin and user roles, with specific permissions for each.
-   **Quiz Management:** Admins can create, edit, and delete subjects, chapters, quizzes, and questions.
-   **Quiz Taking:** Users can attempt quizzes, and their scores are recorded.
-   **Analytics:** The application provides analytics for both admins and users, including leaderboards and summary charts.
-   **Background Jobs:** The application uses Celery for background jobs, including daily reminders, monthly reports, and CSV exports.
-   **Caching:** The application uses Redis for caching to improve performance.
-   **PDF Reports:** Monthly activity reports are generated as PDFs.

## Getting Started

### Prerequisites

-   Python 3.11+
-   Redis

### Installation

1.  Clone the repository:
    ```bash
    git clone https://github.com/your-username/quiz-master-v2.git
    cd quiz-master-v2/backend
    ```
2.  Install the dependencies:
    ```bash
    pip install -e .
    ```
3.  Initialize the database:
    ```bash
    flask db init
    flask db migrate -m "Initial migration"
    flask db upgrade
    ```
4.  Seed the database with initial data:
    ```bash
    flask seed
    ```

### Running the Application

The following steps should be followed in the correct order to run the application.

1.  **Start Redis Server**

    Before starting the application, ensure your Redis server is running. Open a terminal and start the Redis server (the command may vary based on your OS and installation):
    ```bash
    redis-server
    ```
    Keep this terminal open.

2.  **Initialize and Seed the Database**

    In a new terminal, navigate to the `backend` directory. Run the following commands to set up and populate the database. This only needs to be done once.
    ```bash
    # Initialize the database (only for the first time)
    flask db init

    # Create the database migration script
    flask db migrate -m "Initial migration"

    # Apply the migration to create tables
    flask db upgrade

    # Seed the database with initial data
    flask seed
    ```

3.  **Start the Celery Worker**

    In a third terminal, start the Celery worker to handle asynchronous tasks.
    ```bash
    celery -A main.celery worker -l info
    ```
    Keep this terminal open.

4.  **Start the Flask Application**

    Finally, in a fourth terminal, start the Flask application server.
    ```bash
    flask run
    ```

The application will now be running and accessible at `http://127.0.0.1:5000`.

## API Endpoints

A full list of API endpoints can be found in the `api/` directory.
