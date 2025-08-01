# TASK-004: Investigate and Track Broken Endpoints

## Task Overview
- **Task ID**: TASK-004
- **Created**: 2025-07-31
- **Status**: TODO
- **Priority**: MEDIUM
- **Type**: INVESTIGATION
- **Dependencies**: TASK-003 (Cascading Data Collection Framework)

## 🎯 Objective
Investigate and implement a system to track broken endpoints to avoid re-running them on every collection run. Currently, endpoints that return 500 errors (like league 602 - FA Community Shield) are retried on every run, which is inefficient and wastes API calls.

## 📋 Acceptance Criteria
- [ ] Identify all endpoints that consistently return 500 errors
- [ ] Create a mechanism to track and store failed endpoint attempts
- [ ] Implement logic to skip known broken endpoints in future runs
- [ ] Add configuration options for endpoint blacklisting
- [ ] Create reporting system to show which endpoints are being skipped
- [ ] Provide manual override to retry blacklisted endpoints

## 🔍 Context
During the European majors collection, we encountered several endpoints that consistently return 500 errors:
- League 602 (FA Community Shield) - 500 Server Error
- League 604 - 500 Server Error  
- League 606 - 500 Server Error
- League 612 - 500 Server Error
- League 646 - 500 Server Error

These are likely competitions that don't support the `/league-seasons` endpoint (like one-off matches, international competitions, etc.).

## 📝 Implementation Steps

### Phase 1: Investigation
1. **Identify Broken Endpoints**
   - [ ] Run collection scripts and log all 500 errors
   - [ ] Categorize errors by endpoint type and league type
   - [ ] Determine if errors are consistent or intermittent
   - [ ] Document which competition types don't support certain endpoints

2. **Analyze Error Patterns**
   - [ ] Check if errors correlate with specific league types
   - [ ] Identify if errors are related to competition format (one-off vs. season-based)
   - [ ] Determine if errors are API limitations or temporary issues

### Phase 2: Tracking System
3. **Create Endpoint Blacklist**
   - [ ] Design database table to store failed endpoint attempts
   - [ ] Track endpoint, league_id, error type, and timestamp
   - [ ] Implement logic to mark endpoints as "permanently broken" vs "temporarily failed"

4. **Implement Skip Logic**
   - [ ] Modify collection scripts to check blacklist before making API calls
   - [ ] Add configuration option to enable/disable blacklist checking
   - [ ] Create logging to show when endpoints are being skipped

### Phase 3: Configuration and Reporting
5. **Configuration System**
   - [ ] Add blacklist configuration to `collection_config.yaml`
   - [ ] Create manual override options for testing
   - [ ] Add retry logic for endpoints that were temporarily down

6. **Reporting and Monitoring**
   - [ ] Create reports showing skipped endpoints
   - [ ] Add metrics for API call efficiency
   - [ ] Implement periodic retry of blacklisted endpoints

## 🛠️ Technical Details

### Database Schema for Tracking
```sql
CREATE TABLE staging.failed_endpoints (
    id SERIAL PRIMARY KEY,
    endpoint VARCHAR(50) NOT NULL,
    league_id INTEGER,
    error_type VARCHAR(20) NOT NULL,
    error_message TEXT,
    failure_count INTEGER DEFAULT 1,
    last_failure TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_permanent BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Configuration Options
```yaml
# Add to collection_config.yaml
endpoint_blacklist:
  enabled: true
  permanent_failures:
    - endpoint: "league-seasons"
      league_ids: [602, 604, 606, 612, 646]
      reason: "One-off competitions don't support seasons endpoint"
  retry_after_days: 30  # Retry blacklisted endpoints after 30 days
```

### Implementation Approach
1. **Pre-flight Check**: Before making API calls, check if endpoint/league_id combination is blacklisted
2. **Failure Tracking**: Log all 500 errors to database with failure count
3. **Permanent vs Temporary**: Mark endpoints as permanently broken after N consecutive failures
4. **Manual Override**: Allow force-retry of blacklisted endpoints for testing

## 📊 Expected Benefits
- **Reduced API Calls**: Skip known broken endpoints
- **Faster Collection**: Avoid waiting for failed requests
- **Better Error Handling**: Distinguish between temporary and permanent failures
- **Improved Monitoring**: Track API health over time

## 🚧 Potential Challenges
- **False Positives**: Endpoints might be temporarily down
- **API Changes**: Endpoints might be fixed in future
- **Configuration Management**: Keeping blacklist up to date
- **Testing**: Ensuring blacklist doesn't hide real issues

## 💡 Future Enhancements
- **Automatic Retry**: Periodically retry blacklisted endpoints
- **API Health Dashboard**: Monitor endpoint success rates
- **Smart Blacklisting**: Use machine learning to predict endpoint failures
- **Endpoint Documentation**: Document which competition types support which endpoints

## 📚 Resources
- [Current API Documentation](src/api/endpoint_documentation/)
- [Collection Configuration](config/collection_config.yaml)
- [FBR Client Implementation](src/api/fbr_client.py)

---
*Created: 2025-07-31*
*Last Updated: 2025-07-31*
*Status: TODO* 