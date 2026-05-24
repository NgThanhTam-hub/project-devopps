from flask import Flask, jsonify
import os
import time

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({
        "message"  : "CI/CD + Kubernetes Project",
        "author"   : "Nguyen Thanh Tam",
        "school"   : "Cao Dang Kinh Te TPHCM",
        "version"  : "1.0.0",
        "status"   : "running",
        "hostname" : os.getenv("HOSTNAME", "unknown")
    })

@app.route('/health')
def health():
    return jsonify({
        "status"    : "healthy",
        "timestamp" : time.strftime('%Y-%m-%d %H:%M:%S')
    }), 200

@app.route('/api/version')
def version():
    return jsonify({
        "version"    : "1.0.0",
        "build"      : os.getenv("BUILD_NUMBER", "local"),
        "environment": os.getenv("APP_ENV", "development")
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
