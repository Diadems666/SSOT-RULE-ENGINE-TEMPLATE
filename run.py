#!/usr/bin/env python
"""
Run script for the Bottle Shop End of Trade Web Application
"""
from bottle_shop import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) 