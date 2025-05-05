# Bottle Shop End of Trade API Documentation

This document describes the API endpoints available in the Bottle Shop End of Trade application.

## API Endpoints

### 1. Calculate Optimal Float

Calculates the optimal denomination breakdown for a till float based on available denominations.

- **URL**: `/api/calculate-optimal-float`
- **Method**: `POST`
- **Content-Type**: `application/json`

#### Request Body

```json
{
  "available_denominations": {
    "5c": 20.00,
    "10c": 30.00,
    "20c": 40.00,
    "50c": 50.00,
    "$1": 200.00,
    "$2": 300.00,
    "$5": 500.00,
    "$10": 1000.00,
    "$20": 2000.00,
    "$50": 5000.00,
    "$100": 10000.00
  },
  "target_value": 500.00
}
```

Parameters:
- `available_denominations` (required): Dictionary mapping denomination names to monetary values or counts
- `target_value` (optional): The target float value (default: 500.00)

#### Successful Response

Status code: 200 OK

```json
{
  "optimal_float": {
    "5c": 0.50,
    "10c": 1.50,
    "20c": 2.00,
    "50c": 10.00,
    "$1": 50.00,
    "$2": 80.00,
    "$5": 100.00,
    "$10": 100.00,
    "$20": 100.00,
    "$50": 50.00,
    "$100": 0.00
  },
  "total_value": 500.00
}
```

Returns:
- `optimal_float`: Dictionary of denominations and their monetary values
- `total_value`: Total monetary value of the optimal float

#### Error Response

Status code: 400 Bad Request

```json
{
  "error": "Unable to create exact float with available denominations",
  "message": "Cannot create a float of exactly $500.00 with the provided denominations."
}
```

Other possible error messages:
- `"Missing request data"`
- `"Missing required field: available_denominations"`
- `"Available denominations must be a dictionary"`
- `"Invalid denomination: [denomination]"`
- `"Denomination value cannot be negative: [denomination]"`
- `"Target value must be a positive number"`

### 2. Safe Float Transfer

Calculates the transfer needed between the safe and the till float to reach a target value.

- **URL**: `/api/safe-float-transfer`
- **Method**: `POST`
- **Content-Type**: `application/json`

#### Request Body

```json
{
  "safe_float": {
    "5c": 0.50,
    "10c": 1.00,
    "20c": 2.00,
    "50c": 10.00,
    "$1": 50.00,
    "$2": 100.00,
    "$5": 100.00,
    "$10": 200.00,
    "$20": 400.00,
    "$50": 500.00,
    "$100": 100.00
  },
  "target_value": 1500.00
}
```

Parameters:
- `safe_float` (required): Dictionary mapping denomination names to monetary values
- `target_value` (optional): The target safe float value (default: 1500.00)

#### Successful Response

Status code: 200 OK

```json
{
  "current_total": 1463.50,
  "target_value": 1500.00,
  "difference": -36.50,
  "action": "withdraw",
  "amount": 36.50
}
```

Returns:
- `current_total`: Current total value of the safe float
- `target_value`: Target value for the safe float
- `difference`: Difference between current total and target value
- `action`: Action to take ('deposit' or 'withdraw')
- `amount`: Absolute amount to deposit or withdraw

#### Error Response

Status code: 400 Bad Request

```json
{
  "error": "Missing required field: safe_float"
}
```

Other possible error messages:
- `"Missing request data"`
- `"Safe float must be a dictionary"`
- `"Invalid denomination: [denomination]"`
- `"Value for [denomination] must be a number"`
- `"Value for [denomination] cannot be negative"`
- `"Target value must be a positive number"`

### 3. Optimize Float Distribution

Optimizes the distribution of denominations between the safe float and till float.

- **URL**: `/api/optimize-float-distribution`
- **Method**: `POST`
- **Content-Type**: `application/json`

#### Request Body

```json
{
  "safe_float": {
    "5c": 10.00,
    "10c": 15.00,
    "20c": 10.00,
    "50c": 20.00,
    "$1": 100.00,
    "$2": 200.00,
    "$5": 200.00,
    "$10": 500.00,
    "$20": 400.00,
    "$50": 500.00,
    "$100": 0.00
  },
  "till_float": {
    "5c": 0.50,
    "10c": 1.00,
    "20c": 2.00,
    "50c": 10.00,
    "$1": 50.00,
    "$2": 40.00,
    "$5": 0.00,
    "$10": 0.00,
    "$20": 0.00,
    "$50": 0.00,
    "$100": 0.00
  },
  "safe_target": 1500.00,
  "till_target": 500.00
}
```

Parameters:
- `safe_float` (required): Dictionary mapping denomination names to monetary values
- `till_float` (required): Dictionary mapping denomination names to monetary values
- `safe_target` (optional): The target safe float value (default: 1500.00)
- `till_target` (optional): The target till float value (default: 500.00)

#### Successful Response

Status code: 200 OK

```json
{
  "safe_adjusted": {
    "5c": 0.50,
    "10c": 10.00,
    "20c": 5.00,
    "50c": 10.00,
    "$1": 100.00,
    "$2": 170.00,
    "$5": 150.00,
    "$10": 450.00,
    "$20": 300.00,
    "$50": 500.00,
    "$100": 0.00
  },
  "till_adjusted": {
    "5c": 10.00,
    "10c": 6.00,
    "20c": 7.00,
    "50c": 20.00,
    "$1": 50.00,
    "$2": 70.00,
    "$5": 50.00,
    "$10": 50.00,
    "$20": 100.00,
    "$50": 0.00,
    "$100": 0.00
  },
  "movements": {
    "5c": 9.50,
    "10c": 5.00,
    "20c": 5.00,
    "50c": 10.00,
    "$1": 0.00,
    "$2": 30.00,
    "$5": 50.00,
    "$10": 50.00,
    "$20": 100.00,
    "$50": 0.00,
    "$100": 0.00
  },
  "safe_total": 1695.50,
  "till_total": 500.00,
  "safe_variance": 195.50,
  "till_variance": 0.00
}
```

Returns:
- `safe_adjusted`: Updated safe float with denomination values
- `till_adjusted`: Updated till float with denomination values
- `movements`: Denomination movements (positive = safe to till, negative = till to safe)
- `safe_total`: Total value of the adjusted safe float
- `till_total`: Total value of the adjusted till float
- `safe_variance`: Difference between safe total and target value
- `till_variance`: Difference between till total and target value

#### Error Response

Status code: 400 Bad Request

```json
{
  "error": "Insufficient total funds",
  "message": "Insufficient total funds. Available: $1800.50, Required: $2000.00"
}
```

Other possible error messages:
- `"Missing request data"`
- `"Missing required field: safe_float"`
- `"Missing required field: till_float"`
- `"Safe float must be a dictionary"`
- `"Till float must be a dictionary"`
- `"Safe target must be a positive number"`
- `"Till target must be a positive number"`
- `"Invalid denomination in safe_float: [denomination]"`
- `"Value for [denomination] in safe_float must be a number"`
- `"Value for [denomination] in safe_float cannot be negative"`

## Error Handling

All API endpoints follow a consistent error response format:

```json
{
  "error": "Brief error description",
  "message": "Detailed error message"
}
```

Error types:
- Value errors (status code 400): Problems with the values provided
- Type errors (status code 400): Problems with the data types
- Unexpected errors (status code 500): Server-side issues 