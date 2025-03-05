from flask import Flask, request, jsonify
from app.api.api import app


if __name__ == "__main__":
    app.run(debug=True)
    



