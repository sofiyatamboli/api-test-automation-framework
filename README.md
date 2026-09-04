# API Test Automation Framework

A small REST API (Task Manager) built with **Flask**, paired with a full **automated test suite** using **Pytest** and a **Postman/Newman** collection — with **CI/CD via GitHub Actions** running the tests on every push.

Built to demonstrate end-to-end skills across API development, automated testing, and CI pipelines.

## Tech Stack

- **Python 3 / Flask** — REST API
- **Pytest** — automated test suite
- **Postman + Newman** — collection-based API testing
- **GitHub Actions** — CI pipeline that runs tests automatically
- **pytest-html** — HTML test reports

## Project Structure

```
api-test-automation-framework/
├── app.py                          # Flask REST API
├── requirements.txt
├── tests/
│   └── test_api.py                 # Pytest automated test suite
├── postman/
│   └── TaskManagerAPI.postman_collection.json
└── .github/workflows/tests.yml     # CI pipeline
```

## API Endpoints

| Method | Endpoint         | Description             |
|--------|------------------|--------------------------|
| GET    | /health          | Health check             |
| GET    | /tasks           | Get all tasks            |
| GET    | /tasks/\<id\>      | Get a single task        |
| POST   | /tasks           | Create a new task        |
| PUT    | /tasks/\<id\>      | Update an existing task  |
| DELETE | /tasks/\<id\>      | Delete a task            |

## Running Locally

```bash
# 1. Clone the repo
git clone https://github.com/<your-username>/api-test-automation-framework.git
cd api-test-automation-framework

# 2. Create a virtual environment
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the API
python app.py
# API now running at http://127.0.0.1:5000
```

## Running the Automated Tests

```bash
# Run the full pytest suite
pytest -v

# Run with an HTML report
pytest -v --html=report.html --self-contained-html
```

## Running the Postman Collection via Newman

```bash
npm install -g newman
newman run postman/TaskManagerAPI.postman_collection.json
```

## Continuous Integration

Every push and pull request to `main` automatically triggers the GitHub Actions workflow in [`.github/workflows/tests.yml`](.github/workflows/tests.yml), which installs dependencies, runs the full Pytest suite, and uploads an HTML test report as a build artifact.

## What This Project Demonstrates

- Designing and implementing a REST API from scratch
- Writing automated API tests covering success paths, error handling, and edge cases
- Using both code-based (Pytest) and GUI-based (Postman) testing approaches
- Setting up a CI/CD pipeline so tests run automatically on every code change
- Structuring a testable, maintainable Python project
