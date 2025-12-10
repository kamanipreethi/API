# Python Code Execution API 🐍

A secure REST API that executes user-submitted Python code inside isolated Docker containers with built-in security measures.

## 🎯 Project Overview

This project demonstrates how to safely run untrusted Python code by leveraging Docker containerization with security constraints. Users can submit Python code via an API endpoint and receive the execution output.

**Example:**
```bash
POST /run
Body: { "code": "print('Hello World')" }
Response: { "output": "Hello World" }
```

## ✨ Features

- ✅ Execute Python code via REST API
- ✅ Docker container isolation
- ✅ Execution timeout (10 seconds)
- ✅ Memory limit (128MB)
- ✅ Network isolation (no internet access)
- ✅ Read-only filesystem
- ✅ Input validation (max 5000 characters)
- ✅ Detailed error messages
- ✅ Simple web UI for testing

## 🛡️ Security Features

### 1. **Execution Timeout**
Prevents infinite loops from consuming resources:
```python
# This code will be terminated after 10 seconds
while True:
    pass
```

### 2. **Memory Limits**
Protects against memory exhaustion attacks:
```python
# This will be stopped before crashing the system
x = "a" * 1000000000
```

### 3. **Network Isolation**
Blocks all network access:
```python
# This will fail - no internet access allowed
import requests
requests.get("http://evil.com")
```

### 4. **Read-Only Filesystem**
Prevents unauthorized file modifications:
```python
# This will fail in read-only mode
with open("/tmp/test.txt", "w") as f:
    f.write("hacked!")
```

### 5. **Input Validation**
- Maximum code length: 5000 characters
- Validates request format
- Sanitizes input

## 📋 Prerequisites

- **Docker** (version 20.10 or higher)
- **Python** 3.8+ (for running the API)
- **pip** (Python package manager)

### Install Docker

**Windows/Mac:**
- Download [Docker Desktop](https://www.docker.com/products/docker-desktop)

**Linux:**
```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
```

Verify installation:
```bash
docker --version
```

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone <repository-url>
cd api
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Pull Python Docker Image
```bash
docker pull python:3.11-slim
```

### 4. Start the API
```bash
python app.py
```

The API will start on `http://localhost:5000`

## 📖 API Documentation

### Endpoint: `POST /run`

Execute Python code in an isolated Docker container.

**Request:**
```json
{
  "code": "print(2 + 2)"
}
```

**Success Response:**
```json
{
  "output": "4",
  "status": "success"
}
```

**Error Response:**
```json
{
  "error": "Execution timed out after 10 seconds",
  "status": "error"
}
```

### Example API Calls

**Using cURL:**
```bash
curl -X POST http://localhost:5000/run \
  -H "Content-Type: application/json" \
  -d '{"code": "print(\"Hello World\")"}'
```

**Using Python requests:**
```python
import requests

response = requests.post('http://localhost:5000/run', json={
    'code': 'print(2 + 2)'
})
print(response.json())
```

**Using JavaScript fetch:**
```javascript
fetch('http://localhost:5000/run', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ code: 'print("Hello World")' })
})
.then(res => res.json())
.then(data => console.log(data));
```

## 🧪 Testing Examples

### Test 1: Basic Execution
```json
{
  "code": "print('Hello')"
}
```
Expected: `{ "output": "Hello" }`

### Test 2: Mathematical Operations
```json
{
  "code": "x = 5 + 3\nprint(x)"
}
```
Expected: `{ "output": "8" }`

### Test 3: Loops
```json
{
  "code": "for i in range(5):\n    print(i)"
}
```
Expected: `{ "output": "0\n1\n2\n3\n4" }`

### Test 4: Timeout Protection
```json
{
  "code": "while True:\n    pass"
}
```
Expected: `{ "error": "Execution timed out after 10 seconds" }`

### Test 5: Memory Protection
```json
{
  "code": "x = 'a' * 1000000000"
}
```
Expected: Error due to memory limit

### Test 6: Network Isolation
```json
{
  "code": "import requests\nrequests.get('http://google.com')"
}
```
Expected: Error (no network access)

## 🌐 Web UI

Access the web interface at `http://localhost:5000` after starting the API.

Features:
- Code editor with syntax highlighting
- Submit button to execute code
- Output display area
- Error handling with clear messages

## 🏗️ Project Structure

```
api/
├── app.py                 # Main Flask API
├── executor.py            # Docker execution logic
├── static/
│   ├── css/
│   │   └── style.css     # Web UI styles
│   └── js/
│       └── app.js        # Web UI logic
├── templates/
│   └── index.html        # Web UI HTML
├── requirements.txt       # Python dependencies
├── README.md             # This file
└── DOCUMENTATION.md      # Detailed project documentation
```

## 🔧 Configuration

Edit the following parameters in `executor.py`:

```python
TIMEOUT = 10              # Execution timeout in seconds
MEMORY_LIMIT = "128m"     # Container memory limit
MAX_CODE_LENGTH = 5000    # Maximum characters allowed
```

## 🐛 Troubleshooting

### Common Issues

**1. "Permission denied" Error**
```bash
# On Linux, add your user to docker group
sudo usermod -aG docker $USER
# Log out and log back in
```

**2. "Cannot connect to Docker daemon"**
```bash
# Start Docker service
sudo systemctl start docker  # Linux
# Or start Docker Desktop on Windows/Mac
```

**3. Container doesn't stop**
- Check Docker version (must be 20.10+)
- Ensure timeout flag is properly set

**4. Code runs too slow**
- Check memory limits
- Verify Docker has sufficient resources allocated

## 📚 What I Learned

### Docker Security Insights

1. **Containers are NOT VMs**: They share the host kernel, so complete isolation isn't guaranteed
2. **Read-only filesystems** prevent many attacks but don't stop memory-based exploits
3. **Resource limits** are essential to prevent DoS attacks
4. **Network isolation** is easy with `--network none` but process isolation requires more
5. **Timeouts** are critical for managing runaway processes

### Limitations Discovered

- Docker can read `/etc/passwd` inside the container (but it's the container's passwd, not the host's)
- Cannot write to filesystem with `--read-only` flag (this is good!)
- Some Python libraries require write access to work properly
- Container startup has overhead (~1-2 seconds per execution)

### Security Best Practices Implemented

✅ Never run containers as root (use `--user`)
✅ Always set resource limits (CPU, memory, PIDs)
✅ Disable network unless absolutely required
✅ Use read-only filesystems when possible
✅ Set execution timeouts
✅ Validate and sanitize all inputs
✅ Log all executions for monitoring

## 🚨 Security Warnings

⚠️ **This is a learning project!** For production use, consider:

- Additional sandboxing (gVisor, Firecracker)
- Rate limiting per user
- Audit logging
- Code analysis before execution
- More sophisticated resource limits
- Proper authentication/authorization
- HTTPS/TLS for API endpoints

## 🤝 Contributing

Feel free to submit issues and enhancement requests!

## 📄 License

This project is for educational purposes.

## 👨‍💻 Author

Created as a learning project to understand Docker security and code execution sandboxing.

---

**⚡ Quick Commands Reference:**

```bash
# Start API
python app.py

# Run tests
python test_api.py

# Pull Docker image
docker pull python:3.11-slim

# Check running containers
docker ps

# Clean up stopped containers
docker container prune
```
