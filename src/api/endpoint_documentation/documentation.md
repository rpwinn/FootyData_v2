# /documentation Endpoint Documentation

## Overview
Endpoint to view FBR API documentation. This is a utility endpoint that provides access to the complete API documentation.

## Endpoint Details
- **URL**: `/documentation`
- **Method**: GET
- **Base URL**: https://fbrapi.com

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| None | - | - | This endpoint does not accept any parameters |

## Response Structure

### Success Response (200)
```html
<!doctype html>
<html lang=en>
<head>
    <title>FBR API Documentation</title>
    <!-- HTML documentation content -->
</head>
<body>
    <!-- Complete API documentation in HTML format -->
</body>
</html>
```

### Error Response (4xx/5xx)
```json
{
    "error": "Error message description"
}
```

## Field Descriptions

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| HTML Content | string | Complete API documentation in HTML format | Full documentation page |

## Usage Examples

### Get API Documentation
```bash
GET /documentation
```

### Using curl
```bash
curl -H "X-API-Key: YOUR_API_KEY" \
     -H "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36" \
     "https://fbrapi.com/documentation/"
```

### Using Python
```python
import requests

headers = {
    'X-API-Key': 'YOUR_API_KEY',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
}

response = requests.get('https://fbrapi.com/documentation/', headers=headers)
documentation_html = response.text
```

## Data Volume
- **Response Size**: Large (full HTML documentation page)
- **Update Frequency**: Static (documentation doesn't change frequently)
- **Data Availability**: Always available

## Dependencies
- **Requires**: Valid API key for authentication
- **Used by**: Developers and users to understand API capabilities

## Notes

This endpoint provides:

- **Complete API Documentation**: Full HTML documentation for all endpoints
- **Authentication Requirements**: Details about API key requirements
- **Rate Limiting Information**: Guidelines for API usage
- **Endpoint Descriptions**: Detailed information about each endpoint
- **Example Requests**: Sample API calls and responses
- **Error Handling**: Information about error codes and responses

### Additional Notes
- Returns HTML content, not JSON
- Requires valid API key authentication
- Useful for programmatic access to documentation
- Can be parsed to extract endpoint information automatically

## Common Use Cases

1. **Development Reference**: Access documentation during development
2. **API Discovery**: Learn about available endpoints and capabilities
3. **Automated Documentation**: Parse documentation for code generation
4. **Troubleshooting**: Reference documentation for API issues

## Error Handling

| Status Code | Description | Resolution |
|-------------|-------------|------------|
| 200 | Success | Documentation retrieved successfully |
| 401 | Unauthorized | Check API key validity |
| 404 | Not Found | Endpoint may be temporarily unavailable |
| 500 | Internal Server Error | Server issue, try again later | 