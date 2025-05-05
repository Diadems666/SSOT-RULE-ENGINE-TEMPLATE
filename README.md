# Bottle Shop End of Trade Web Application

A web-based application for Australian bottle shops to manage end-of-trade processes, cash handling, and financial reconciliation.

## Overview

This application streamlines the daily reconciliation of sales, cash handling, and financial reporting for bottle shops. It features an intuitive calendar interface, robust support for all denominations of Australian currency, dedicated modules for managing safe and till floats, and comprehensive end-of-trade reconciliation.

## Features

- **Calendar Interface**: Navigate and select specific dates for financial management
- **Australian Currency Support**: Handle all coin denominations (5c, 10c, 20c, 50c, $1, $2) and banknote denominations ($5, $10, $20, $50, $100)
- **Safe Float Management**: Track and maintain the $1,500 safe float with automatic excess/deficit calculation
- **Till Float Management**: Track, reconcile and calculate optimal denomination breakdown for the $500 till float
- **Daily Trade Variables**: Record and track till readings, EFTPOS transactions, card payments, account charges, cash amounts, and customer counts
- **End-of-Trade Reconciliation**: Automatically calculate variance between recorded sales and payment methods
- **Settlement Process**: Mark daily takings as settled once reconciliation is complete
- **Knowledge Graph Integration**: Comprehensive graph representation of application components and relationships
- **Rule Engine**: Business rules enforcement and documentation

## Technology Stack

- **Backend**: Python 3.13, Flask 2.3.3 framework
- **Frontend**: HTML5, CSS3, JavaScript (with Bootstrap 5)
- **Database**: SQLite with SQLAlchemy 2.0.36
- **Forms**: Flask-WTF 1.2.1 with WTForms 3.0.1
- **Authentication**: Flask-Login 0.6.2
- **Database Migrations**: Flask-Migrate 4.0.4
- **Environment Variables**: python-dotenv 1.0.0
- **Knowledge Graph**: MCP Knowledge Graph server

## Known Compatibility Issues

There are currently compatibility issues between SQLAlchemy 2.0.x and Python 3.13. The error appears related to type annotations in the SQLAlchemy codebase:

```
AssertionError: Class <class 'sqlalchemy.sql.elements.SQLCoreOperations'> directly inherits TypingOnly but has additional attributes {'__firstlineno__', '__static_attributes__'}.
```

Potential solutions include:
- Downgrading to Python 3.11 or 3.12
- Waiting for SQLAlchemy to release a version compatible with Python 3.13
- Manually patching the SQLAlchemy code

## Installation

1. Clone the repository
2. Create a virtual environment:
   ```
   python -m venv venv
   ```
3. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - macOS/Linux: `source venv/bin/activate`
4. Install the required packages:
   ```
   pip install -r requirements.txt
   ```
5. Initialize the database:
   ```
   flask db init
   flask db migrate -m "Initial migration"
   flask db upgrade
   ```
6. Run the application:
   ```
   flask run
   ```

## Usage

After starting the application, navigate to `http://localhost:5000` in your web browser. The application will redirect you to the current day's takings page. From there, you can:

1. Navigate to different dates using the calendar view
2. Enter safe and till float denomination counts
3. Record payment method totals
4. Calculate optimal till float denomination breakdown
5. View the variance between recorded sales and payment methods
6. Save and settle daily takings

## Business Rules

The application enforces several key business rules:

1. Safe float must maintain a target value of $1,500
2. Till float must maintain a target value of $500
3. All Australian currency denominations are supported
4. Till float makeup prioritizes smaller denominations for the float
5. Once a day is settled, its records cannot be modified without special permissions
6. All financial values are stored as floating-point to two decimal places
7. Customer count must be a non-negative integer

## Database Schema

The application uses a SQLite database with the following structure:

- **daily_takings**: Records daily financial data
  - `date` (PRIMARY KEY): Date of the record
  - `till_read`: Total sales from the POS
  - `eftpos_total`: Fixed EFTPOS terminal transactions
  - `portable_eftpos_total`: Portable EFTPOS transactions
  - `amex`: American Express transactions
  - `diners`: Diners Club transactions
  - `account_charges`: Account charge transactions
  - `total_cash`: Total cash transactions
  - `points_redeemed`: Loyalty points redeemed
  - `customer_count`: Number of customers
  - `safe_float_open`: JSON string of opening safe float denominations
  - `safe_float_close`: JSON string of closing safe float denominations
  - `till_float_open`: JSON string of opening till float denominations
  - `till_float_close_before_makeup`: JSON string of closing till float denominations before makeup
  - `till_float_makeup`: JSON string of till float makeup denominations
  - `variance`: Calculated variance between till read and payment methods
  - `settled`: Boolean indicating if the day's takings are settled

## Knowledge Graph

The application integrates with MCP Knowledge Graph to maintain a comprehensive representation of the system's architecture, components, and relationships. This graph provides:

- Detailed mapping of code structure and relationships
- Documentation of business rules and logic
- Visualization of component interactions
- Support for developer onboarding and maintenance

To interact with the Knowledge Graph:
1. Ensure MCP servers are installed and running
2. Use the MCP Knowledge Graph API to query the application structure
3. Visualize relationships between components

## Development

### Project Structure

```
bottle_shop/
├── __init__.py           # Application factory and extensions
├── controllers/          # Route controllers
│   ├── __init__.py
│   ├── main.py           # Main routes
│   └── takings.py        # Takings-related routes
├── models/               # Database models
│   ├── __init__.py
│   └── daily_takings.py  # DailyTakings model
├── services/             # Business logic services
│   ├── __init__.py
│   └── currency_service.py  # Currency handling service
├── static/               # Static assets
│   ├── css/              # Stylesheets
│   └── js/               # JavaScript files
└── templates/            # Jinja2 templates
    ├── layout.html       # Base template
    ├── about.html        # About page
    ├── calendar.html     # Calendar view
    └── takings.html      # Daily takings form
```

### Rule Engine Configuration

The application uses a Rule Engine system to maintain and enforce business rules:

```
.cursor/CORE/RULE-ENGINE/
├── MDC-BOTTLE-SHOP.rules  # Main domain context rules
└── WORKFLOW.rules         # Development workflow rules
```

## Future Enhancements

Planned enhancements include:
1. User authentication for manager access
2. Data export functionality for reporting
3. Dashboard for historical variance tracking
4. Backup/restore functionality for the database
5. Cash flow trend visualization

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Authors

- Developed for Australian bottle shops to streamline end-of-trade processes