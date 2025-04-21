from flask import Flask, render_template, request, send_file, redirect
import os, json

app = Flask(__name__)
UPLOAD_FOLDER = "payloads"
OUTPUT_FOLDER = "output"
DEVICE_COUNTER_FILE = "device_count.json"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def xor_encrypt(data, key=0xAA):
    return bytes([b ^ key for b in data])

def update_device_count():
    if os.path.exists(DEVICE_COUNTER_FILE):
        with open(DEVICE_COUNTER_FILE, "r") as f:
            count = json.load(f).get("count", 0) + 1
    else:
        count = 1
    with open(DEVICE_COUNTER_FILE, "w") as f:
        json.dump({"count": count}, f)
    return count

@app.route("/", methods=["GET", "POST"])
def index():
    count = 0
    if os.path.exists(DEVICE_COUNTER_FILE):
        with open(DEVICE_COUNTER_FILE, "r") as f:
            count = json.load(f).get("count", 0)
    return render_template("index.html", device_count=count)

@app.route("/upload", methods=["POST"])
def upload():
    file = request.files["payload"]
    if file:
        path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(path)
    return redirect("/")

@app.route("/inject", methods=["POST"])
def inject():
    filename = request.form["filename"]
    path = os.path.join(UPLOAD_FOLDER, filename)
    if os.path.exists(path):
        with open(path, "rb") as f:
            data = f.read()
        # Inject fake hook (NOPs for simulation)
        hook = b"\x90" * 10
        injected = hook + data
        out_path = os.path.join(OUTPUT_FOLDER, "hook_payload.bin")
        with open(out_path, "wb") as f:
            f.write(injected)
    return redirect("/")

@app.route("/encrypt", methods=["POST"])
def encrypt():
    in_path = os.path.join(OUTPUT_FOLDER, "hook_payload.bin")
    out_path = os.path.join(OUTPUT_FOLDER, "hook_payload_encrypted.bin")
    if os.path.exists(in_path):
        with open(in_path, "rb") as f:
            data = f.read()
        encrypted = xor_encrypt(data)
        with open(out_path, "wb") as f:
            f.write(encrypted)
    return redirect("/")

@app.route("/download/<filename>")
def download(filename):
    return send_file(os.path.join(OUTPUT_FOLDER, filename), as_attachment=True)

@app.route("/simulate_execution", methods=["POST"])
def simulate_execution():
    update_device_count()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
