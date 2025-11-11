# GPA API

This project is a GPA calculator API that extracts course information from PDF transcripts and calculates GPA statistics. It is built using FastAPI and provides endpoints for processing transcript files.

## Features

- Upload a PDF transcript file.
- Extract course information including course codes, names, credits attempted, credits earned, and grades.
- Calculate GPA statistics such as total courses, total credits, weighted average, highest grade, and lowest grade.

## Project Structure

```
gpa-api
├── app
│   ├── main.py                # Entry point of the API application
│   ├── api
│   │   └── v1
│   │       ├── endpoints
│   │       │   └── transcripts.py  # API endpoints for transcript processing
│   │       └── __init__.py
│   ├── core
│   │   └── config.py          # Configuration settings for the application
│   ├── services
│   │   ├── extractor.py        # Functions for extracting text from PDFs and parsing course info
│   │   └── statistics.py       # Functions for calculating GPA and statistics
│   ├── models
│   │   └── schemas.py         # Data models and schemas for request/response validation
│   └── utils
│       └── pdf_utils.py       # Utility functions for handling PDF files
├── tests
│   ├── test_extractor.py       # Unit tests for extractor functions
│   └── test_api.py             # Tests for API endpoints
├── requirements.txt            # Project dependencies
├── pyproject.toml              # Project configuration and dependency management
├── .gitignore                  # Files and directories to ignore in version control
└── README.md                   # Project documentation
```

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd gpa-api
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

1. Start the FastAPI application:
   ```
   uvicorn app.main:app --reload
   ```

2. Access the API documentation at `http://127.0.0.1:8000/docs`.

3. Use the `/api/v1/transcripts` endpoint to upload a PDF file and retrieve GPA statistics.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for details.