# Flight Ticket OCR API Documentation

This API allows you to extract structured information from flight ticket images and PDFs using OCR and AI processing.

## Base URL

When running locally, the API is available at:
```
http://localhost:8808
```

## Endpoints

### 1. Extract Information from Flight Ticket

Extracts structured information from a flight ticket image or PDF.

**URL**: `/api/extract`

**Method**: `POST`

**Content-Type**: `multipart/form-data`

**Parameters**:

| Parameter | Type   | Required | Description                                                                                |
|-----------|--------|----------|--------------------------------------------------------------------------------------------|
| file      | File   | Yes      | The flight ticket image or PDF file (supported formats: .jpg, .jpeg, .png, .pdf)           |
| model     | String | No       | AI model to use for processing (default: "deepseek/DeepSeek-V3-0324")            |

**Example Request**:

Using cURL:
```bash
curl -X POST http://localhost:8808/api/extract \
  -F "file=@path/to/ticket.jpg" \
  -F "model=deepseek/DeepSeek-V3-0324"
```

Using Python requests:
```python
import requests

url = "http://localhost:8808/api/extract"
files = {"file": open("path/to/ticket.jpg", "rb")}
data = {"model": "deepseek/DeepSeek-V3-0324"}

response = requests.post(url, files=files, data=data)
print(response.json())
```

**Successful Response**:

```json
{
  "airline": "Air France",
  "flight_number": "AF1234",
  "passenger_name": "JOHN DOE",
  "departure_airport": "CDG",
  "arrival_airport": "JFK",
  "departure_date": "2023-06-15",
  "departure_time": "10:30",
  "arrival_date": "2023-06-15",
  "arrival_time": "13:45",
  "seat_number": "12A",
  "booking_reference": "ABC123",
  "ticket_number": "057-1234567890",
  "fare_class": "Y",
  "baggage_allowance": "2PC"
}
```

**Error Responses**:

- 400 Bad Request: File not provided or invalid file type
```json
{
  "error": "No file part"
}
```
```json
{
  "error": "No file selected"
}
```
```json
{
  "error": "File type not supported"
}
```

- 500 Internal Server Error: Processing error
```json
{
  "error": "Error message details"
}
```

## Available Models

The API supports various AI models through OpenRouter:

- `deepseek/DeepSeek-V3-0324` (default)
- `anthropic/claude-3-haiku:beta`
- `anthropic/claude-3-sonnet:beta`
- `meta-llama/llama-3-8b-instruct:free`

## File Size Limits

Maximum file size: 16MB

## Web Interface

A web interface is available at the root URL (`http://localhost:8808/`) for testing the API through a user-friendly interface.