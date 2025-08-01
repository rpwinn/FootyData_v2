# /generate_api_key Endpoint Documentation

## Overview
Endpoint to generate a new API key for accessing the FBR API. This is a utility endpoint for obtaining authentication credentials.

## Endpoint Details
- **URL**: `/generate_api_key`
- **Method**: POST
- **Base URL**: https://fbrapi.com

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| None | - | - | This endpoint does not accept any parameters |

## Response Structure

### Success Response (200)
```json
{
    "api_key": "j7zDTA9GnmmUgCxZQ0bF4cMLi9RTWQg_9BbtBgOw9hM"
}
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
| `api_key` | string | Generated API key for authentication | "j7zDTA9GnmmUgCxZQ0bF4cMLi9RTWQg_9BbtBgOw9hM" |

## Usage Examples

### Generate New API Key
```bash
POST /generate_api_key
```

### Using curl
```bash
curl -X POST \
     -H "Content-Type: application/json" \
     -H "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36" \
     "https://fbrapi.com/generate_api_key/"
```

### Using Python
```python
import requests

headers = {
    'Content-Type': 'application/json',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
}

response = requests.post('https://fbrapi.com/generate_api_key/', headers=headers)
api_key_data = response.json()
new_api_key = api_key_data['api_key']
```

### Using JavaScript/Fetch
```javascript
fetch('https://fbrapi.com/generate_api_key/', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
    }
})
.then(response => response.json())
.then(data => {
    console.log('New API Key:', data.api_key);
});
```

## Data Volume
- **Response Size**: Small (few bytes)
- **Update Frequency**: On-demand (generated when requested)
- **Data Availability**: Always available

## Dependencies
- **Requires**: No authentication (this endpoint generates authentication)
- **Used by**: New users and applications to obtain API access

## Notes

This endpoint provides:

- **API Key Generation**: Creates new authentication credentials
- **No Authentication Required**: Can be called without existing API key
- **Immediate Access**: Generated key can be used immediately
- **Unique Keys**: Each call generates a unique API key

### Additional Notes
- Generated API keys are immediately valid
- No authentication required to generate new keys
- Keys are unique and should be kept secure
- Can be called multiple times to generate multiple keys
- Generated keys follow the format: 64-character alphanumeric string

## Common Use Cases

1. **Initial Setup**: Generate first API key for new applications
2. **Key Rotation**: Generate new keys for security purposes
3. **Development**: Create keys for testing and development
4. **Backup Keys**: Generate additional keys as backups

## Error Handling

| Status Code | Description | Resolution |
|-------------|-------------|------------|
| 200 | Success | API key generated successfully |
| 400 | Bad Request | Check request format |
| 429 | Too Many Requests | Respect rate limiting |
| 500 | Internal Server Error | Server issue, try again later |

## Security Considerations

- **Key Storage**: Store generated keys securely
- **Key Sharing**: Never share API keys publicly
- **Key Rotation**: Regularly generate new keys
- **Environment Variables**: Store keys in environment variables, not in code

## Integration with Other Endpoints

After generating an API key, it can be used with all other endpoints:

```bash
# Example: Use generated key with countries endpoint
curl -H "X-API-Key: YOUR_GENERATED_KEY" \
     -H "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36" \
     "https://fbrapi.com/countries/"
``` 