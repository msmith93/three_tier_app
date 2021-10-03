from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello_world():
    return 'Hello, World!'

@app.route("/health")
def health():
    # If DB connectivity succeeds
    return 'OK'

@app.route("/diag")
def diag():
    diagnostics_data = {}
    return diagnostics_data

if __name__ == "__main__":
    # Only for debugging while developing
    app.run(host='0.0.0.0', debug=True, port=80)
