# BoxAudit

**BoxAudit** is a Python utility that scans and counts files (images, videos, and others) across large folder structures stored on Box.com using the Box API.

Built to handle 50,000+ folders efficiently, it uses your API key to authenticate and provides a breakdown of file types, making large data audits fast and automated.

---

## 🚀 Features

- 🔍 Count total files in Box folders recursively
- 🖼️ Classify files (images, videos, others) based on extension
- 📦 Supports massive folder structures (50k+ folders)
- 🔐 API Key-based secure access to Box
- 📊 Generates simple count reports

---

## 🧰 Requirements

- Python 3.8+
- `requests`
- `boxsdk`

Install them via:

```bash
pip install -r requirements.txt
