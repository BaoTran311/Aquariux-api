## Prerequisites

* __Python 3.10 or above__ installed
* __NodeJS__ installed
* __Allure CLI__ installed

    ```shell script
    npm i allure-commandline -g
    ```

## Setup

* Create and activate a virtual environment
    ```shell script
    python3 -m venv .venv
    # On Windows
    .venv\Scripts\activate
    # On Unix or MacOS
    source .venv/bin/activate
    ```

* Install necessary libraries

    ```shell script
    pip3 install -r requirements.txt
    ```

## How to run test cases

### Basic Commands

```shell script
# Run all tests
pytest

# Run specific test file
pytest tests/auth/test_login.py

# Run specific test function
pytest tests/auth/test_login.py::test_positive_AUT_TC001_login_with_valid_credentials
```

### Test Filtering
```bash
# Filter by test type
pytest -k "positive"     # Run positive tests only
pytest -k "negative"     # Run negative tests only
pytest -k "integration"    # Run integration tests only

# Filter by test case ID
pytest -k "AUT_TC001"    # Run specific test case
pytest -k "TRD_MRK"      # Run trade market related tests

# Filter by test module
pytest tests/auth/       # Authentication tests
pytest tests/trade/      # Trading tests
pytest tests/market/     # Market data tests
pytest tests/user/       # User management tests
```


### Common Usage Examples
```bash
# Run auth tests on demo account with debug
pytest tests/auth/ --account=demo --debuglog

# Run all positive tests for lirunex MT5
pytest -k "positive" --client=lirunex --server=mt5 --debuglog

# Run integration tests with custom user
pytest -k "integration" --user=testuser --password=testpass --debuglog

# Run specific test case with allure report
pytest -k "AUT_TC001" --alluredir=allure-results --debuglog
```

## Framework Structure

```
Aquariux-api/
├── config/                    # Environment configurations
│   └── sit.yaml               # SIT environment settings
├── src/                       # Source code
│   ├── core/                  # Core framework components
│   │   ├── request.py         # HTTP request handling
│   │   └── response.py        # Response validation methods
│   ├── enums/                 # Enumeration constants
│   │   ├── system.py          # System-related enums
│   │   └── trade.py           # Trading-related enums
│   ├── routes/                # API client implementations
│   │   ├── auth/              # Authentication APIs
│   │   │   ├── auth_client.py
│   │   │   └── login.py
│   │   ├── market/            # Market data APIs
│   │   └── trade/             # Trading APIs
│   │       ├── market.py
│   │       ├── order.py
│   │       ├── pending.py
│   │       └── trade_client.py
│   ├── utils/                 # Utility functions
│   │   ├── allure_utils.py    # Allure reporting helpers
│   │   ├── assert_utils.py    # Custom assertion methods
│   │   ├── datetime_utils.py  # Date/time utilities
│   │   ├── json_utils.py      # JSON processing helpers
│   │   ├── logger_utils.py    # Logging configuration
│   │   └── trading_utils.py   # Trading-specific utilities
│   ├── consts.py              # Framework constants
│   └── data_runtime.py        # Runtime data management
├── tests/                     # Test cases
│   ├── auth/                  # Authentication tests
│   │   ├── conftest.py        # Auth-specific fixtures
│   │   └── test_login.py      # Login test cases
│   ├── chart/                 # Chart-related tests
│   ├── market/                # Market data tests
│   │   ├── symbol/            # Symbol management tests
│   │   └── watchlist/         # Watchlist tests
│   ├── trade/                 # Trading tests
│   │   ├── market/            # Market order tests
│   │   ├── order/             # Order management tests
│   │   └── pending/           # Pending order tests
│   └── user/                  # User management tests
│       ├── account/           # Account settings tests
│       ├── preference/        # User preference tests
│       ├── setting/           # User setting tests
│       └── statistics/        # User statistics tests
├── conftest.py                # Global pytest configuration
├── pytest.ini                 # Pytest settings
├── requirements.txt           # Python dependencies
```

### Key Components

**Core Framework (`src/core/`)**
- `request.py`: HTTP request handling with retry logic
- `response.py`: Response validation methods (status, schema, payload)

**API Clients (`src/routes/`)**
- Organized by functional areas (auth, market, trade)
- Each client handles specific API endpoints
- Includes payload builders and response schemas

**Utilities (`src/utils/`)**
- `allure_utils.py`: Custom Allure reporting and attachments
- `assert_utils.py`: Enhanced assertion methods
- `logger_utils.py`: Structured logging with Allure integration

**Test Organization (`tests/`)**
- Mirrors API structure for easy navigation
- Each module has dedicated `conftest.py` for fixtures
- Test naming follows: `test_{type}_{TC_id}_{scenario}`

## How to generate Allure report

* Run via pytest command with Allure command

    ```shell script
    pytest tests --alluredir=allure-results
    allure serve allure-results
    ```
  
## [How to develop API test case](GUIDANCE.md)
