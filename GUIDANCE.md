### [Link test cases memberSite](https://docs.google.com/spreadsheets/d/1Ck8AvaeEnlfGmuc242Oc1PBm9meh3i2UYOgTk48Jgvg/edit?gid=0#gid=0)

## Agenda
- Naming convention
- Test coverage
- Mandatory checkpoints
- Payload validation
- Json schema


## How to develop test cases
- Test Naming Convention: 
  - **test_type** → indicates the test category  
    (should be one of the values `positive`, `negative`, `integration`)  
  - **TC_id** → unique test case identifier  
    (e.g., `AUT_TC001`, `TRD_MRK_TC002`)  
  - **test_scenario** → short description of what the test does  
    (e.g., `login_using_valid_CRM_credential_with_required_params`)  
  - **test_positive_AUTH_TC001_login_using_valid_CRM_credential_with_required_params**
- Test Coverage
  - Positive: valid payload/params validation
  
    Ex:
    - Required params
    - Full params (required + optional)
    - Redundant params
    - ...
  - Negative: invalid payload/ params
    
    Ex:
    - Missing required params
    - Wrong data type of params
    - Missing authenticate in headers
    - Using another authenticate
    - ...
  - Integration: check multiple APIs combine
  
    Ex: 
    - 1/ GET /symbol
    - 2/ POST /trade/order
    - 3/ GET /trade/order/detail -> to verify create success
    - 4/ UPDATE /trade/order
    - 5/ GET /trade/order/detail -> to verify update success
    - 6/ DELETE /trade/order
    - 7/ GET /trade/order/detail -> to verify delete success
- Mandatory Checkpoints
  - `resp.check_status_code(<expected status code>)` → (e.g., `resp.check_status_code(200)`)
  - `resp.check_response_time(<expected response time>)` → (e.g., `resp.check_response_time(0.5)`)
  - `resp.check_jsonschema(<expected schema>)` → (e.g., `resp.check_jsonschema(schema)`)
- Payload Validation Methods
  
  Example response payload 
    ```json
      {
        "code": "200",
        "result": {
          "token": "eyJhbGciOiJIUzUxMiJ9.eyJyb2xlIjpbIlJPTEVfVVNFUiJdLCJsb2dpblRpbWUiOjE3NTk4NDk2NDAxNjYsIm1ldGF0cmFkZXJJZCI6IjIwOTIwMDk2MzIiLCJ0ZW5hbnRJZCI6ImxpcnVuZXgiLCJvbXNTZXJ2ZXJJZCI6ImxpcnVuZXgiLCJzb3VyY2UiOiJXRUIiLCJ0eXBlIjoiTUVNQkVSIiwidXNlcklkIjoiREVNTy0yMDkyMDA5NjMyIiwic3ViIjoiREVNTy0yMDkyMDA5NjMyIiwiaWF0IjoxNzU5ODQ5NjQwLCJleHAiOjE3NjI0NDE2NDB9.ffaMKSmtdwXZWwH0H1AvgXiPgtJoZCMZ2k9uMQr_9ox3pMAz6HW9R25FeC57CuGL0Manc78l8AqhVMRLJhDy6Q",
             "user": {
               "source": "WEB",
               "metatraderId": "2092009632",
               "metatraderGroup": "demoLxStd",
               "isDemo": true,
               "traderSubcription": "lirunex|DEMO|demoLxStd",
               "marketSubcription": "lirunex|DEMO|2092009632",
               "traderSubscription": "lirunex|DEMO|demoLxStd",
               "marketSubscription": "lirunex|DEMO|2092009632",
               "tenantId": "lirunex",
               "mainProductCode": "METATRADER4",
               "omsServerId": "lirunex"
          }
        }
      }
    ```
  `resp.check_payload_equals('200', key="code")`

  `resp.check_payload_equals('WEB', key="result.token.user.source")`

## What is JSON Schema (Important)
  - JSON Schema that describes the structure of response data — it defines:
    - Which fields the data must include
    - The data type of each field (string, number, boolean, etc.), and
    - The validation rules that apply to those fields.
  - Ex:
    
    Response data json 
      ```json{
      {
          "id": 123,
          "name": "Bao Tran",
          "email": "bao@example.com",
          "is_active": true
      }
      ```
    Json schema
      ```json
        {
          "type": "object",
          "properties": {
            "id": { "type": "integer" },
            "name": { "type": "string" },
            "email": { "type": "string", "format": "email" },
            "is_active": { "type": "boolean" }
          },
          "required": ["id", "name", "email"]
        }
      ```
   - [Link generate json schema](https://transform.tools/json-to-json-schema)
