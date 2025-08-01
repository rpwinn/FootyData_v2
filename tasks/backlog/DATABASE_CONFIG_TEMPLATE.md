# Database Configuration Template for Staging Table Tasks

## 🛠️ Technical Details

### Database Configuration:
- **Database**: PostgreSQL (via `DATABASE_URL` environment variable)
- **Schema**: `staging` (as defined in `config/config.yaml`)
- **Connection**: Using `psycopg2` with environment variables from `.env`
- **Table**: `staging.[table_name]`

### API Endpoint:
- **URL**: `/[endpoint_path]`
- **Method**: GET
- **Required Parameters**: [list required parameters]
- **Response**: [describe response structure]

### Files to Create:
- `src/database/create_[table_name]_staging.sql`
- `src/etl/test_[table_name]_data.py`

### Dependencies:
- PostgreSQL database access via `DATABASE_URL`
- [List any dependent staging tables]
- API documentation from TASK-001
- FBR API client configuration
- Environment variables loaded from `.env` file

## 📚 Resources
- [Endpoint API Documentation](src/api/endpoint_documentation/[endpoint].md)
- [Dependent staging table](src/database/create_[dependent_table]_staging.sql)
- [FBR API Client](src/api/fbr_client.py)

## 💡 Notes
- All staging tables use the `staging` schema as defined in `config/config.yaml`
- Database connection uses `DATABASE_URL` from `.env` file
- Table naming follows pattern: `staging.[table_name]`
- Include standard audit fields: `created_at`, `updated_at`
- Store raw API response in `raw_data JSONB` field for debugging 