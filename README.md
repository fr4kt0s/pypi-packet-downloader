# 🐍 PyPI Package Web Mirror (Bandersnatch GUI)

This project provides a lightweight web interface built with Flask to mirror individual Python packages using [bandersnatch](https://pypi.org/project/bandersnatch/), process the downloaded files, and archive them.

---

## 🚀 Features

* Simple web UI with text input for PyPI package names
* Mirrors packages from PyPI using `bandersnatch`
* Automatically modifies file paths in the generated file list
* Archives selected files as `.tar.gz`
* Displays result directly in the browser
* Logs all activity to console and rotating log file

---

## 📁 Project Structure

```text
project/
├── main.py                    # Flask app entrypoint
├── scripts/
│   ├── webserver.py           # Flask route handler
│   ├── bandersnatch_utils.py  # Package mirroring logic
│   ├── file_utils.py          # File filtering and selection
│   ├── archive_utils.py       # Archive creation
│   └── validation.py          # Input validation
├── templates/
│   └── index.html             # HTML form for web UI
├── config/
│   └── bandersnatch.conf      # Configuration file for bandersnatch
├── requirements.txt           # Python dependencies
├── Dockerfile                 # Docker build file
└── webserver.log              # Rotating log file
```

---

## 🐳 Run with Docker

### 🛠 Build the image:

```bash
docker build -t pypi-webmirror .
```

### ▶️ Run the container:

```bash
docker run -p 5000:5000 pypi-webmirror
```

### 🌍 Access the Web UI

Open [http://localhost:5000](http://localhost:5000) in your browser.

---

## 🔄 Live Development (optional)

To enable live code changes without rebuilding the container each time:

```bash
docker run -p 5000:5000 -v $(pwd):/app pypi-webmirror
```

> This mounts your local source directory into the container at `/app`.

---

## ⚙️ Configuration

Edit the Bandersnatch config file:

```text
config/bandersnatch.conf
```

Example fields to configure:

* `directory = /mnt/python/data/changes/`
* `storage-backend = filesystem`
* `mirror = false` (when using `sync <package>` mode)

---

## 🗃 Output Paths

* Original package files: `/mnt/python/data/changes/`
* Modified file lists & archives: `/mnt/python/data/upload/`

---

## 📋 Logging

All logs are written to:

* Console output (with level: `INFO`)
* Rotating file `webserver.log` (max size 1MB, 5 backups)

---

## 🛡️ Deployment Note

This app uses Flask's development server and is **not suitable for production**.
Use a proper WSGI server like **Gunicorn** for deployment:

```bash
gunicorn -w 4 -b 0.0.0.0:5000 main:app
```

---

## 📄 License

MIT License
(c) Your Name, 2025
