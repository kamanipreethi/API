from flask import Flask, request, jsonify, send_from_directory
from runner.docker_runner import run_code_in_docker

app = Flask(__name__)

MAX_CODE_SIZE = 5000  # Requirement: limit code length to 5000 chars


def clean_message(msg: str) -> str:
    """
    Removes excessive tracebacks and returns a cleaner message.
    """
    if "Traceback" in msg:
        return msg.splitlines()[-1]  # last line only
    return msg


# Serve UI
@app.route("/", methods=["GET"])
def ui():
    return send_from_directory("static", "index.html")


# Main execution endpoint
@app.route("/run", methods=["POST"])
def run_code():
    data = request.get_json(silent=True)

    if not data or "code" not in data:
        return jsonify({"error": "Missing 'code' field"}), 400

    code = data["code"]

    # Section 4 requirement: enforce max length
    if len(code) > MAX_CODE_SIZE:
        return jsonify({
            "error": f"Code too long (max {MAX_CODE_SIZE} characters)"
        }), 400

    # Execute inside Docker
    output, exit_code = run_code_in_docker(code)

    # Clean output
    output = clean_message(output)

    return jsonify({
        "output": output,
        "exit_code": exit_code
    })


# Main entry point
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)