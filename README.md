████████████████████████████████████████████████████████████████████████

# 💻 Optimization Algorithms Comparative Project - AOA

## ✨ Features

- 🚀 Implements four major optimization algorithms:
  - 🔺 **Gradient Descent (GD)**
  - ❄️ **Simulated Annealing (SA)**
  - 🧬 **Genetic Algorithm (GA)**
  - 🦅 **Particle Swarm Optimization (PSO)**
- ⚡ Applies these algorithms to:
  - 📈 Hyperparameter tuning for logistic regression (Machine Learning)
  - 🌍 Solving the Traveling Salesman Problem (TSP)
- 📊 Visualizes algorithm convergence and optimal paths for TSP
- ⏱️ Benchmarks algorithm speed and output quality for each task

## 📦 Installation

1. **Dependencies:**
   - 🐍 Python
   - 🔢 numpy
   - 📊 pandas
   - 🤖 scikit-learn
   - 📉 matplotlib
2. **Setup:**  
   Install required packages with pip:  
```
pip install numpy pandas scikit-learn matplotlib
```
3. **Data:**  
📂 Place `Student_Performance.csv` in your working directory for ML optimization.

## 📋 Usage

- 🧠 **Machine Learning Optimization:**  
- ▶️ Run `Logistic_Regression_Optimization.py` to optimize the regularization parameter `C` for logistic regression using all four algorithms.
- 🏆 Outputs: Best C values, model accuracy for each method, and the winning algorithm.
- 🌐 **Traveling Salesman Problem (TSP) Optimization:**  
- ▶️ Run `TSP.py` to compare SA, GA, and PSO for finding the shortest route among randomly generated cities.
- 📉 Outputs: Shortest routes, distances, timing stats, and graphs visualizing paths and convergence curves.
- 🛠️ **Parameter Customization:**  
- ⚙️ Tweak script parameters as desired, such as city count or iteration numbers, for comparison experiments.

## 📝 Notes

- 🔀 **Cross-validation** is used in ML optimization to avoid biased accuracy estimates.
- 🎯 Results highlight that different algorithms excel at different problem types (convex vs non-convex).
- 🌈 TSP experiments visually demonstrate solution and convergence differences between metaheuristics.
- 🗂️ Machine learning and TSP tasks are handled in separate scripts for clarity.
- 👍 For best results, run scripts individually and examine plots for insights into performance.

## 🔗 Links

- 👩‍🎓 **Student Performance Dataset:**  
[Kaggle - Student Performance (Multiple Linear Regression)](https://www.kaggle.com/datasets/nikhil7280/student-performance-multiple-linear-regression)
- 📁 **Project Documents:**  
- 🖥️ `OPTIMIZATION ALGORITHM.pptx` (presentation)
- 📄 `AOA_PROJECT(final).pdf` (detailed report)

## 🛠️ Tech Stack

- 🛡️ **Programming Language:** Python
- 🧮 **Core Libraries:** numpy, pandas
- 🤖 **Machine Learning:** scikit-learn
- 📈 **Visualization:** matplotlib
- 🗃️ **Dataset:** Student Performance (CSV format)

████████████████████████████████████████████████████████████████████████

# 🔒 Secure File Storage with RSA + AES Encryption - CIS

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
