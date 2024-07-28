from flask import Flask, jsonify
from __init__ import init_app

app = init_app()

if __name__ == '__main__':
    app.run(debug=True, port=8082, host='0.0.0.0')
