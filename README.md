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

- 📊 [**CIS PPT Presentation**](https://www.figma.com/deck/WOD8hk2AhMToP0iGTlwUup)

## 🛠️ Tech Stack

- **Backend**: Flask 3.0.0
- **Cryptography**: PyCryptodome 3.19.0

<img width="858" height="706" alt="image" src="https://github.com/user-attachments/assets/17349ba3-0fc7-49c1-a96c-54a09e204b1a" />


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
- 🛠️ **Parameter Customization:** Tweak script parameters as desired, such as city count or iteration numbers, for comparison experiments.

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
- **Frontend**: HTML5, CSS3, JavaScript
- **Security**: RSA-2048 + AES-128-EAX

<img width="1248" height="698" alt="image" src="https://github.com/user-attachments/assets/83d26916-ce2b-49b7-85f4-2c1630ee91eb" />


████████████████████████████████████████████████████████████████████████

# 🛍️ AMT Recommendation System in Data Mining

A hands-on machine learning project implementing **fashion recommendation systems** on the Myntra dataset. Includes both content-based and collaborative filtering methods to suggest relevant clothing and accessories, with clear and modular notebooks for each approach.

## ✨ Features
- 🧩 **Multiple Methods:** Content-based, item-to-item collaborative, and user-to-user collaborative recommendations
- 📝 **Robust Data Handling:** Missing values are smartly filled for smooth operation
- 🔎 **Feature Engineering:** Uses TF-IDF on text and label encoding/normalization for categorical and numerical features
- 💡 **Simple Recommendation Functions:** Clean code for generating and displaying top-N recommended products
- 📊 **Real Product Data:** Demonstrates on the Myntra fashion dataset with diverse clothing categories

## 📦 Installation
```
pip install pandas scikit-learn
```
Run with [Jupyter Notebook](https://jupyter.org/) or [Google Colab](https://colab.research.google.com/).

## 📋 Usage

1. Open `Content.ipynb` for content-based logic, or `Collab.ipynb` for collaborative filtering
2. Place `myntradataset.csv` in the notebook directory
3. Run all notebook cells to preprocess and initialize functions
4. Call the example functions with a product index (`recommend_content_based(0, top_n=5)` or `recommend_collaborative(0, top_n=5)`)
5. View printed recommendations (product name, brand, color, price, rating) in notebook output

## 📝 Notes

- The implementation auto-handles missing `brand`, `colour`, or `description` fields for seamless operation[^1]
- Categorical values (brand, color) are label encoded; all numerical features are min-max normalized[^1]
- Designed for any product in the Myntra dataset – pick any row index for personalized recommendations[^3][^4]
- Example outputs are shown in the notebook's print statements[^3][^4]

## 🔗 Links

- 📑 [**AMT Project PPT**](https://www.figma.com/deck/ndkUt2LJmqVzVYpUQtDong/AMT-PPT?node-id=1-303&viewport=699%2C369%2C0.02&t=gOMcl5fMVoX516to-1&scaling=min-zoom&content-scaling=fixed&page-id=0%3A1)

## 🛠️ Tech Stack

- **Analysis & Code:** Python (pandas, scikit-learn)
- **Data:** Myntra product CSV
- **Notebooks:** Jupyter (.ipynb)
- **ML Techniques:** TF-IDF, Label Encoding, MinMax Scaling, Cosine Similarity

<img width="682" height="441" alt="image" src="https://github.com/user-attachments/assets/490ec213-1eaa-4fa0-a7c3-13fd0f62ca38" />

████████████████████████████████████████████████████████████████████████

# 🎮 Tic-Tac-Toe AI Selector - Multi-Algorithm Comparison

This project is a Flask-based web application that implements three different AI algorithms for playing Tic-Tac-Toe: **Q-Learning**, **Policy Gradient Neural Network**, and **Minimax**. It provides an interactive web interface where users can play against any of the three AI opponents and compare their performance in real-time.

## ✨ Features

- 🧠 **Three AI Algorithms**: Q-Learning (reinforcement learning), Policy Gradient (deep reinforcement learning), and Minimax (classical game theory)
- 🎯 **Interactive Web UI** with responsive grid-based game board and smooth animations  
- 🔄 **Real-time AI Selection** - switch between different AI opponents mid-game
- 💾 **Persistent Learning** - Q-Learning and Policy Gradient models save/load their training progress
- 🎨 **Modern Design** with hover effects, winner highlighting, and visual feedback
- ⚡ **Auto-training** - models train automatically if no saved state exists
- 🎲 **Smart Move Selection** with exploration strategies for learning-based AIs

### Q-Learning
- **Type**: Tabular reinforcement learning
- **Strategy**: Learns optimal moves through trial-and-error gameplay
- **Storage**: State-action values saved in `qtable.pkl`
- **Parameters**: ε=0.1 (exploration), α=0.5 (learning rate), γ=0.9 (discount)

### Policy Gradient
- **Type**: Deep reinforcement learning with neural network
- **Architecture**: 9→128→9 fully connected layers with ReLU activation
- **Strategy**: Learns probability distribution over moves
- **Storage**: Model weights saved in `policy.pth`

### Minimax  
- **Type**: Classical game theory algorithm
- **Strategy**: Explores all possible game states to find optimal moves
- **Performance**: Unbeatable when playing optimally
- **Computation**: Real-time tree search with perfect information

## 📦 Installation
```
pip install Flask==2.3.3 torch==2.0.1 torchvision==0.15.2
```

## 🚀 Usage

1. 🌐 **Start the server**: Run `python app.py` and open `http://localhost:5000`
2. 🎯 **Select AI opponent** from the dropdown menu (Q-Learning, Policy Gradient, or Minimax)
3. 🎮 **Click any cell** to make your move as 'X' - AI plays as 'O'  
4. 🏆 **Game results** are displayed with winner highlighting and victory animations
5. 🔄 **Reset anytime** using the reset button to start a fresh game
6. 🔀 **Switch AIs** mid-game to compare different strategies

## 🎯 Training Details

- **Q-Learning**: 50,000 episodes of self-play with ε-greedy exploration
- **Policy Gradient**: 50,000 episodes using REINFORCE algorithm with baseline normalization
- **Auto-initialization**: Models train automatically on first run if no saved files exist
- **Progress tracking**: Real-time training progress displayed in console

## 📝 Notes

- 🧠 **Learning AIs** improve over time and may make suboptimal moves during exploration
- 🎯 **Minimax** provides the strongest challenge as it never makes mistakes
- 💾 **Training data** persists between sessions for continuous learning
- ⚡ **Model loading** is automatic - no manual training required after initial setup

## 🛠️ Tech Stack

- **Backend**: Flask 2.3.3
- **AI/ML**: PyTorch 2.0.1, NumPy
- **Frontend**: Vanilla JavaScript, CSS Grid, HTML5
- **Storage**: Pickle (Q-table), PyTorch state dict (neural network)

## 📊 Algorithm Comparison

| Algorithm | Strength | Learning | Speed | Memory |
|-----------|----------|----------|-------|---------|
| **Minimax** | Perfect | None | Fast | Low |
| **Q-Learning** | High | Tabular | Medium | Medium |
| **Policy Gradient** | Variable | Neural | Slow | High |

## 🔗 Links

- 📊 [**Project Presentation**:](https://www.figma.com/deck/sRf3uZnt4csFStkcyE1Ov4/ML-PPT?node-id=1-305&t=zvKJH64xZKbRC9ST-1&scaling=min-zoom&content-scaling=fixed&page-id=0%3A1)

<img width="476" height="688" alt="image" src="https://github.com/user-attachments/assets/57600c87-b5fb-4b39-9905-088c2a33c200" />



