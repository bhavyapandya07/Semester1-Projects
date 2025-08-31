# 🔒 Secure File Storage with RSA + AES Encryption

This project is a Flask-based web application for securely encrypting and decrypting files using hybrid RSA and AES cryptographic algorithms. It provides a simple web interface allowing users to upload files, select security tiers, and perform encryption or decryption operations entirely in-memory without storing keys on disk.

## ✨ Features

- 🔑 **RSA key pairs** generated and stored in memory for two security tiers: Public and Private
- 🛡️ **Hybrid encryption** using RSA for session key encryption and AES (EAX mode) for file data encryption
- 🖥️ **Web UI** for file upload, tier selection, and operation (encrypt/decrypt) with progress and results display
- 📥 **Download** encrypted (`.enc`) or decrypted (`.txt`) files after processing
- ☁️ **Serverless-friendly** design with no key files written to disk
- 🌐 **Cross-origin support** enabled for flexible deployment

## 📦 Installation

```
pip install Flask==3.0.0 Flask-CORS==4.0.0 pycryptodome==3.19.0
```

## 📋 Usage

1. 🌐 Open the web interface in a browser
2. 🔐 Select a security tier: **Public** or **Private**
3. 📁 Upload a plaintext (`.txt`) file for encryption or an encrypted (`.enc`) file for decryption
4. ⚡ Choose the operation (**Encrypt** or **Decrypt**) and click "Process File"
5. 👀 View the encrypted result (Base64) or the decrypted content in the UI
6. ⬇️ Download the processed file using the provided link

## 📝 Notes

- 🧠 Keys are generated in-memory on first request per tier to simulate a serverless environment
- 🔐 Encryption uses a **2048-bit RSA** key for session key exchange and **AES-128 in EAX mode** for file data
- 📄 The app supports text files and encrypted files but displays binary data as Base64 or shows an appropriate message if not viewable as text

## 🔗 Links

- 🌍 [**Live Demo**](https://cisminiproject.vercel.app/)
- 📊 [**CIS PPT Presentation**](https://www.figma.com/slides/WOD8hk2AhMToP0iGTlwUup/Modern-Futuristic-Technology-Deck?node-id=1-510&t=AuWXOnxGMn4HAaMH-1)

## 🛠️ Tech Stack

- **Backend**: Flask 3.0.0
- **Cryptography**: PyCryptodome 3.19.0
- **Frontend**: HTML5, CSS3, JavaScript
- **Security**: RSA-2048 + AES-128-EAX
