from flask import Flask, render_template_string, request, jsonify
import os, pickle, sys, random
import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F

app = Flask(__name__)

# --- Tic-Tac-Toe Utilities ---
def check_winner(board):
    wins = [(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)]
    for a,b,c in wins:
        if board[a]==board[b]==board[c]!=0:
            return board[a], (a,b,c)
    if 0 not in board:
        return 0, ()
    return None, ()

# --- Minimax AI ---
def minimax(board, player):
    winner, _ = check_winner(board)
    if winner is not None:
        return winner * player, None
    best_score = -float('inf')
    best_move = None
    for i in range(9):
        if board[i]==0:
            board[i] = player
            score, _ = minimax(board, -player)
            score = -score
            board[i] = 0
            if score > best_score:
                best_score = score
                best_move = i
    return best_score, best_move

# --- Q-Learning ---
Q_FILE = 'qtable.pkl'
if os.path.exists(Q_FILE):
    with open(Q_FILE,'rb') as f:
        Q = pickle.load(f)
else:
    Q = {}
EPSILON = 0.1
ALPHA = 0.5
GAMMA = 0.9

def board_to_str(board):
    return ''.join([str(c) for c in board])

def qtrain_episode():
    board = [0]*9
    player = 1
    history = []
    while True:
        state = board_to_str(board)
        moves = [i for i,v in enumerate(board) if v==0]
        if random.random() < EPSILON or state not in Q:
            action = random.choice(moves)
        else:
            qs = Q.get(state,[0]*9)
            qs_valid = [qs[i] for i in moves]
            max_q = max(qs_valid)
            best_moves = [i for i in moves if qs[i]==max_q]
            action = random.choice(best_moves)
        history.append((state, action))
        board[action] = player
        winner, _ = check_winner(board)
        if winner is not None:
            reward = 1 if winner==1 else -1 if winner==-1 else 0
            for s,a in history:
                Q.setdefault(s,[0]*9)
                Q[s][a] += ALPHA*(reward - Q[s][a])
            break
        player *= -1

def qtrain(n=50000):
    print("Training Q-Learning AI...")
    for i in range(1,n+1):
        qtrain_episode()
        if i%500==0:
            print(f"Progress: {i}/{n}", end='\r')
            sys.stdout.flush()
    with open(Q_FILE,'wb') as f:
        pickle.dump(Q,f)
    print("\nQ-Learning training completed.")

def q_move(board):
    state = board_to_str(board)
    moves = [i for i,v in enumerate(board) if v==0]
    if state not in Q or random.random()<EPSILON:
        return random.choice(moves)
    qs = Q.get(state,[0]*9)
    qs_valid = [qs[i] for i in moves]
    max_q = max(qs_valid)
    best_moves = [i for i in moves if qs[i]==max_q]
    return random.choice(best_moves)

# --- Policy Gradient AI ---
class PolicyNet(nn.Module):
    def __init__(self):
        super().__init__()
        self.fc1 = nn.Linear(9,128)
        self.fc2 = nn.Linear(128,9)
    def forward(self,x):
        x = F.relu(self.fc1(x))
        x = self.fc2(x)
        return F.softmax(x,dim=-1)

policy = PolicyNet()
optimizer = optim.Adam(policy.parameters(), lr=0.01)
POLICY_FILE = 'policy.pth'

def board_to_tensor(board, player=1):
    return torch.tensor([player*c for c in board],dtype=torch.float32)

def policy_select(state, mask):
    probs = policy(state)
    mask_t = torch.tensor(mask, dtype=torch.float32)
    probs = probs * mask_t                 # mask illegal moves
    if probs.sum().item() == 0:            # fallback if all probs zero
        probs = mask_t
    probs = probs / probs.sum()            # normalize
    if torch.isnan(probs).any():           # extra safeguard
        probs = mask_t / mask_t.sum()
    m = torch.distributions.Categorical(probs)
    action = m.sample()
    return action.item(), m.log_prob(action)

def policy_episode():
    board = [0]*9
    player = 1
    log_probs = []
    rewards = []
    while True:
        mask = [1 if b==0 else 0 for b in board]
        state = board_to_tensor(board, player)
        action, log_prob = policy_select(state, mask)
        board[action]=player
        log_probs.append(log_prob)
        winner, _ = check_winner(board)
        if winner is not None:
            r = 1 if winner==1 else -1 if winner==-1 else 0
            rewards = [r]*len(log_probs)
            break
        player *= -1
    discounted = []
    R=0
    for r in reversed(rewards):
        R = r + 0.99*R
        discounted.insert(0,R)
    discounted = torch.tensor(discounted)
    discounted = (discounted-discounted.mean())/(discounted.std()+1e-8)
    loss=[]
    for lp,R in zip(log_probs, discounted):
        loss.append(-lp*R)
    optimizer.zero_grad()
    torch.stack(loss).sum().backward()
    optimizer.step()

def policy_train(n=50000):
    print("Training Policy Gradient AI...")
    for i in range(1,n+1):
        policy_episode()
        if i%500==0:
            print(f"Progress: {i}/{n}", end='\r')
            sys.stdout.flush()
    torch.save(policy.state_dict(), POLICY_FILE)
    print("\nPolicy Gradient training completed.")

def policy_move(board):
    mask = [1 if b==0 else 0 for b in board]
    state = board_to_tensor(board)
    action,_ = policy_select(state, mask)
    return action

# --- Load or train models ---
if not os.path.exists(Q_FILE):
    qtrain()
if not os.path.exists(POLICY_FILE):
    policy_train()
else:
    policy.load_state_dict(torch.load(POLICY_FILE))

# --- HTML UI ---
HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
<title>Tic-Tac-Toe AI Selector</title>
<style>
body { font-family: Arial,sans-serif; background:#f5f5f5; display:flex; flex-direction:column; align-items:center; margin:0; padding:0; }
h1{margin-top:40px; font-weight:600; font-size:2.2em;}
.board{display:grid; grid-template-columns:repeat(3,100px); grid-gap:10px; margin-top:20px;}
.cell{width:100px;height:100px;background:#fff; border-radius:12px; display:flex; justify-content:center; align-items:center; font-size:64px; cursor:pointer; box-shadow:0 2px 6px rgba(0,0,0,0.1); transition:0.2s;}
.cell:hover{background:#e0e0e0; transform:scale(1.05);}
.cell.winner{background:#4b6cb7;color:white;}
#message{margin-top:20px; font-size:1.5em; min-height:30px; text-align:center;}
button{margin-top:20px;padding:12px 25px;font-size:16px;border:none;border-radius:8px;background:#4b6cb7;color:white; cursor:pointer;}
button:hover{background:#182848;}
select{margin-top:20px;padding:8px 12px;font-size:16px;border-radius:6px;}
</style>
</head>
<body>
<h1>Tic-Tac-Toe AI Selector</h1>
<select id="ai_select">
<option value="qlearning">Q-Learning</option>
<option value="policy">Policy Gradient</option>
<option value="minimax">Minimax</option>
</select>
<div class="board" id="board">
{% for i in range(9) %}
<div class="cell" id="cell{{i}}" onclick="makeMove({{i}})"></div>
{% endfor %}
</div>
<div id="message"></div>
<button onclick="resetGame()">Reset Game</button>
<script>
let board=['','','','','','','','',''];
let waiting=false;

function makeMove(pos){
    if(board[pos]!=''||waiting) return;
    board[pos]='X';
    updateBoard();
    waiting=true;
    document.getElementById('message').innerText="AI is thinking...";
    setTimeout(()=>{
        fetch('/move',{
            method:'POST',
            headers:{'Content-Type':'application/json'},
            body: JSON.stringify({board:board, ai:document.getElementById('ai_select').value})
        }).then(res=>res.json()).then(data=>{
            board=data.board;
            highlightWinning(data.winner_line);
            updateBoard();
            document.getElementById('message').innerText = data.message || "Your turn!";
            waiting=false;
        });
    },300);
}

function updateBoard(){
    for(let i=0;i<9;i++){
        document.getElementById('cell'+i).innerText=board[i];
        document.getElementById('cell'+i).classList.remove('winner');
    }
}

function resetGame(){
    board=['','','','','','','','',''];
    updateBoard();
    document.getElementById('message').innerText='';
}

function highlightWinning(line){
    if(line && line.length==3){
        line.forEach(i=>{document.getElementById('cell'+i).classList.add('winner');});
    }
}
</script>
</body>
</html>
"""

# --- Flask Routes ---
@app.route("/")
def index():
    return render_template_string(HTML_PAGE)

@app.route("/move", methods=["POST"])
def move():
    data = request.get_json()
    board = data["board"]
    ai = data["ai"]
    int_board = [1 if x=="X" else -1 if x=="O" else 0 for x in board]

    # Check if game already over
    winner, line = check_winner(int_board)
    if winner is not None:
        msg = "Draw!" if winner==0 else ("You win!" if winner==1 else "AI wins!")
        return jsonify({"board": board, "message": msg, "winner_line": list(line)})

    # AI move
    if ai=="minimax":
        _, move = minimax(int_board, -1)
    elif ai=="qlearning":
        move = q_move(int_board)
    else:  # policy gradient
        move = policy_move(int_board)

    if move is not None and int_board[move]==0:
        int_board[move] = -1

    # Convert back to symbols
    board = ["X" if v==1 else "O" if v==-1 else "" for v in int_board]
    winner, line = check_winner(int_board)
    if winner is not None:
        msg = "Draw!" if winner==0 else ("You win!" if winner==1 else "AI wins!")
    else:
        msg = ""
    return jsonify({"board": board, "message": msg, "winner_line": list(line)})

# --- Run ---
if __name__ == "__main__":
    app.run(debug=True)
