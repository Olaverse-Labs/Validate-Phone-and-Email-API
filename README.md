# Phone and Email Validation API

[![Olaverse API](https://img.shields.io/badge/Olaverse-API%20Doc-blue?style=flat-square)](https://www.olaverse.co.uk/validator-api) [![Try on Vibeland](https://img.shields.io/badge/Vibeland-Try%20Live-orange?style=flat-square)](https://www.vibeland.co.uk/tools/validation)

A simple FastAPI-based service to validate phone numbers and email addresses, returning detailed metadata for each.

## Features
- Validate international phone numbers and return metadata (country, formats, timezones, etc.)
- Validate email addresses, check MX records, and return metadata (domain, SMTPUTF8, etc.)

## Requirements
- Python 3.8+
- See `requirements.txt` for dependencies

## Installation
1. Clone this repository or download the code.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the API
Start the FastAPI server with Uvicorn:
```bash
uvicorn main:app --reload
```

The API will be available at [http://127.0.0.1:8000](http://127.0.0.1:8000)

Interactive API docs: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

## API Endpoints

### 1. Validate Phone
- **POST** `/validate-phone`
- **Request Body:**
  ```json
  {
    "phone_number": "+2347056066119"
  }
  ```
- **Response Example:**
  ```json
  {
    "is_valid": true,
    "is_formatted_properly": true,
    "country": "Nigeria",
    "location": "Nigeria",
    "timezones": ["Africa/Lagos"],
    "format_national": "0705 606 6119",
    "format_international": "+234 705 606 6119",
    "format_e164": "+2347056066119",
    "country_code": 234,
    "region_code": "NG",
    "type": 1,
    "possible": true,
    "national_number": 7056066119
  }
  ```

### 2. Validate Email
- **POST** `/validate-email`
- **Request Body:**
  ```json
  {
    "email": "test@example.com"
  }
  ```
- **Response Example:**
  ```json
  {
    "valid": true,
    "metadata": {
      "local_part": "test",
      "domain": "example.com",
      "ascii_email": "test@example.com",
      "smtputf8": false,
      "mx": [[10, "mail.example.com"]],
      "mx_records": true
    }
  }
  ```
  *Note: `display_name`, `mx_fallback_type`, and `spf` will be included if available and not null.*

## Notes
- Phone validation uses the `phonenumbers` library (Google's libphonenumber port).
- Email validation uses `email-validator` and DNS lookups for MX records.
- For production, consider HTTPS and authentication.

## License
MIT 