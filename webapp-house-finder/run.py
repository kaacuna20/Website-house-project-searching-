from flask import Flask, request, jsonify, make_response
from app import create_app
from os import environ


app = create_app(settings_module=environ.get('CONFIGURATION_SETUP'))

  
if __name__ == "__main__":
    app.run(debug=environ.get('DEBUG'), host="0.0.0.0", port=5003)