from flask import Flask, request, send_file, jsonify, render_template_string
from flask_cors import CORS
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES, PKCS1_OAEP
import os
import io
import base64

app = Flask(__name__)
CORS(app)

# Store keys in memory for serverless environment
RSA_KEYS = {}

def generate_rsa_keys():
    """Generate RSA keys and store them in memory"""
    global RSA_KEYS
    
    # Generate public tier keys
    if 'public_public' not in RSA_KEYS:
        key_public = RSA.generate(2048)
        RSA_KEYS['public_public'] = key_public.publickey().export_key()
        RSA_KEYS['private_public'] = key_public.export_key()
        print("Public tier RSA keys generated in memory.")

    # Generate private tier keys  
    if 'public_private' not in RSA_KEYS:
        key_private = RSA.generate(2048)
        RSA_KEYS['public_private'] = key_private.publickey().export_key()
        RSA_KEYS['private_private'] = key_private.export_key()
        print("Private tier RSA keys generated in memory.")

def encrypt_file_data(file_data, tier_public_key):
    try:
        recipient_key = RSA.import_key(tier_public_key)
        session_key = get_random_bytes(16)
        
        cipher_rsa = PKCS1_OAEP.new(recipient_key)
        enc_session_key = cipher_rsa.encrypt(session_key)
        
        cipher_aes = AES.new(session_key, AES.MODE_EAX)
        ciphertext, tag = cipher_aes.encrypt_and_digest(file_data)
        
        result = bytearray()
        result.extend(len(enc_session_key).to_bytes(2, byteorder='big'))
        result.extend(enc_session_key)
        result.extend(cipher_aes.nonce)
        result.extend(tag)
        result.extend(ciphertext)
        
        return bytes(result)
    except Exception as e:
        raise Exception(f"Encryption failed: {e}")

def decrypt_file_data(enc_file_data, tier_private_key):
    try:
        private_key = RSA.import_key(tier_private_key)
        
        data_stream = io.BytesIO(enc_file_data)
        len_enc_key = int.from_bytes(data_stream.read(2), byteorder='big')
        enc_session_key = data_stream.read(len_enc_key)
        nonce = data_stream.read(16)
        tag = data_stream.read(16)
        ciphertext = data_stream.read()
        
        cipher_rsa = PKCS1_OAEP.new(private_key)
        session_key = cipher_rsa.decrypt(enc_session_key)
        
        cipher_aes = AES.new(session_key, AES.MODE_EAX, nonce)
        data = cipher_aes.decrypt_and_verify(ciphertext, tag)
        
        return data
    except Exception as e:
        raise Exception(f"Decryption failed: {e}")

# Your existing HTML template (keep exactly as is)
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>Secure File Storage</title>
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap" rel="stylesheet">
<style>
  * {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
  }

  body {
    font-family: 'Poppins', -apple-system, BlinkMacSystemFont, sans-serif;
    background-color: #f7f7f5;
    color: #37352f;
    line-height: 1.5;
    min-height: 100vh;
    padding: 20px;
  }

  .container {
    max-width: 800px;
    margin: 0 auto;
    background: white;
    border-radius: 8px;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
    overflow: hidden;
  }

  .header {
    padding: 32px 40px;
    border-bottom: 1px solid #e9e9e7;
    background: white;
  }

  .header h1 {
    font-size: 32px;
    font-weight: 700;
    color: #2f1b14;
    margin-bottom: 8px;
  }

  .header p {
    color: #9b9a97;
    font-size: 16px;
    font-weight: 400;
  }

  .content {
    padding: 40px;
  }

  .form-section {
    margin-bottom: 32px;
  }

  .form-group {
    margin-bottom: 24px;
  }

  .form-group label {
    display: block;
    font-weight: 500;
    color: #37352f;
    margin-bottom: 8px;
    font-size: 14px;
  }

  select {
    width: 100%;
    padding: 12px 14px;
    border: 1px solid #e9e9e7;
    border-radius: 6px;
    font-size: 14px;
    font-family: 'Poppins', sans-serif;
    background: white;
    color: #37352f;
    transition: all 0.2s ease;
  }

  select:focus {
    outline: none;
    border-color: #2383e2;
    box-shadow: 0 0 0 2px rgba(35, 131, 226, 0.2);
  }

  .file-input-wrapper {
    position: relative;
    display: block;
    width: 100%;
  }

  .file-input {
    width: 100%;
    height: 100px;
    border: 2px dashed #e9e9e7;
    border-radius: 6px;
    background: #fbfbfa;
    cursor: pointer;
    transition: all 0.2s ease;
    position: relative;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-direction: column;
  }

  .file-input:hover {
    border-color: #2383e2;
    background: #f8f9ff;
  }

  .file-input input {
    position: absolute;
    width: 100%;
    height: 100%;
    opacity: 0;
    cursor: pointer;
  }

  .file-input-text {
    font-size: 14px;
    color: #9b9a97;
    font-weight: 400;
  }

  .file-input.has-file {
    border-color: #2383e2;
    background: #f8f9ff;
  }

  .file-input.has-file .file-input-text {
    color: #2383e2;
    font-weight: 500;
  }

  .action-toggle {
    display: flex;
    gap: 12px;
    padding: 4px;
    background: #f7f7f5;
    border-radius: 6px;
    border: 1px solid #e9e9e7;
  }

  .action-option {
    flex: 1;
    padding: 10px 16px;
    text-align: center;
    border-radius: 4px;
    cursor: pointer;
    font-weight: 500;
    font-size: 14px;
    transition: all 0.2s ease;
    background: transparent;
    color: #9b9a97;
  }

  .action-option:hover {
    color: #37352f;
  }

  .action-option.active {
    background: white;
    color: #37352f;
    box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
  }

  .action-option input {
    display: none;
  }

  .process-btn {
    width: 100%;
    padding: 14px 24px;
    background: #2383e2;
    color: white;
    border: none;
    border-radius: 6px;
    font-size: 14px;
    font-weight: 500;
    font-family: 'Poppins', sans-serif;
    cursor: pointer;
    transition: all 0.2s ease;
  }

  .process-btn:hover:not(:disabled) {
    background: #1a6bc7;
  }

  .process-btn:disabled {
    background: #e9e9e7;
    color: #9b9a97;
    cursor: not-allowed;
  }

  .result-section {
    margin-top: 32px;
    padding-top: 32px;
    border-top: 1px solid #e9e9e7;
  }

  .result-block {
    background: #f7f7f5;
    border: 1px solid #e9e9e7;
    border-radius: 6px;
    margin-bottom: 16px;
  }

  .result-header {
    padding: 16px 20px;
    border-bottom: 1px solid #e9e9e7;
    background: #fbfbfa;
    font-weight: 500;
    font-size: 14px;
    color: #37352f;
  }

  .result-content {
    padding: 20px;
    font-family: 'SF Mono', Monaco, Inconsolata, monospace;
    font-size: 12px;
    line-height: 1.6;
    color: #37352f;
    word-break: break-all;
    max-height: 300px;
    overflow-y: auto;
    background: white;
  }

  .download-section {
    margin-top: 16px;
    padding: 20px;
    background: #f8f9ff;
    border: 1px solid #e3f2fd;
    border-radius: 6px;
    text-align: center;
  }

  .download-btn {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 12px 20px;
    background: #2383e2;
    color: white;
    text-decoration: none;
    border-radius: 6px;
    font-weight: 500;
    font-size: 14px;
    transition: all 0.2s ease;
  }

  .download-btn:hover {
    background: #1a6bc7;
    text-decoration: none;
  }

  .status-message {
    padding: 16px 20px;
    border-radius: 6px;
    font-size: 14px;
    font-weight: 500;
    margin-bottom: 16px;
  }

  .status-success {
    background: #f0f9ff;
    color: #1e40af;
    border: 1px solid #bfdbfe;
  }

  .status-error {
    background: #fef2f2;
    color: #dc2626;
    border: 1px solid #fecaca;
  }

  .status-loading {
    background: #fffbeb;
    color: #d97706;
    border: 1px solid #fed7aa;
  }

  @media (max-width: 768px) {
    .container {
      margin: 10px;
      border-radius: 0;
    }
    
    .header {
      padding: 24px 20px;
    }
    
    .content {
      padding: 20px;
    }
    
    .header h1 {
      font-size: 24px;
    }
  }
</style>
</head>
<body>
  <div class="container">
    <div class="header">
      <h1>Secure File Storage</h1>
      <p>Encrypt and decrypt your files with RSA + AES encryption</p>
    </div>

    <div class="content">
      <div class="form-section">
        <div class="form-group">
          <label for="tierSelect">Security Tier</label>
          <select id="tierSelect">
            <option value="public">Public Tier</option>
            <option value="private">Private Tier</option>
          </select>
        </div>

        <div class="form-group">
          <label for="fileInput">File Upload</label>
          <div class="file-input-wrapper">
            <div class="file-input" id="fileInputArea">
              <input type="file" id="fileInput" accept=".txt,.enc" />
              <div class="file-input-text">
                Click to select a file or drag and drop
              </div>
            </div>
          </div>
        </div>

        <div class="form-group">
          <label>Operation</label>
          <div class="action-toggle">
            <div class="action-option active" data-action="encrypt">
              <input type="radio" name="action" value="encrypt" checked />
              Encrypt
            </div>
            <div class="action-option" data-action="decrypt">
              <input type="radio" name="action" value="decrypt" />
              Decrypt
            </div>
          </div>
        </div>

        <button class="process-btn" id="processBtn">Process File</button>
      </div>

      <div id="resultSection" class="result-section" style="display: none;">
        <div id="statusMessage"></div>
        <div id="outputBlock" class="result-block" style="display: none;">
          <div class="result-header" id="outputHeader">Output</div>
          <div class="result-content" id="outputContent"></div>
        </div>
        <div id="downloadSection" class="download-section" style="display: none;">
          <p style="margin-bottom: 12px; color: #6b7280;">File processed successfully</p>
          <a href="#" id="downloadBtn" class="download-btn">
            Download File
          </a>
        </div>
      </div>
    </div>
  </div>

<script>
  document.addEventListener('DOMContentLoaded', function() {
    const fileInput = document.getElementById('fileInput');
    const fileInputArea = document.getElementById('fileInputArea');
    const fileInputText = fileInputArea.querySelector('.file-input-text');
    const actionOptions = document.querySelectorAll('.action-option');
    const processBtn = document.getElementById('processBtn');
    const resultSection = document.getElementById('resultSection');
    const statusMessage = document.getElementById('statusMessage');
    const outputBlock = document.getElementById('outputBlock');
    const outputHeader = document.getElementById('outputHeader');
    const outputContent = document.getElementById('outputContent');
    const downloadSection = document.getElementById('downloadSection');
    const downloadBtn = document.getElementById('downloadBtn');

    fileInput.addEventListener('change', function() {
      if (this.files.length > 0) {
        const fileName = this.files[0].name;
        fileInputText.textContent = fileName;
        fileInputArea.classList.add('has-file');
      } else {
        fileInputText.textContent = 'Click to select a file or drag and drop';
        fileInputArea.classList.remove('has-file');
      }
    });

    actionOptions.forEach(option => {
      option.addEventListener('click', function() {
        actionOptions.forEach(opt => opt.classList.remove('active'));
        this.classList.add('active');
        this.querySelector('input').checked = true;
      });
    });

    processBtn.addEventListener('click', async function() {
      if (!fileInput.files.length) {
        showStatus('Please select a file to process.', 'error');
        return;
      }

      const file = fileInput.files[0];
      const tier = document.getElementById('tierSelect').value;
      const action = document.querySelector('input[name="action"]:checked').value;

      processBtn.disabled = true;
      processBtn.textContent = 'Processing...';
      
      resultSection.style.display = 'block';
      outputBlock.style.display = 'none';
      downloadSection.style.display = 'none';
      showStatus('Processing your file, please wait...', 'loading');

      const formData = new FormData();
      formData.append('file', file);
      formData.append('tier', tier);
      formData.append('action', action);

      try {
        const response = await fetch('/api/encrypt-decrypt', {
          method: 'POST',
          body: formData
        });

        if (!response.ok) {
          const errorData = await response.json();
          throw new Error(errorData.error || 'Server error');
        }

        const blob = await response.blob();
        const arrayBuffer = await blob.arrayBuffer();
        const uint8Array = new Uint8Array(arrayBuffer);
        
        let displayContent;
        let headerText;
        
        if (action === 'encrypt') {
          displayContent = btoa(String.fromCharCode.apply(null, uint8Array));
          headerText = 'Encrypted Content (Base64)';
        } else {
          try {
            displayContent = new TextDecoder('utf-8').decode(uint8Array);
            headerText = 'Decrypted Content';
          } catch (e) {
            displayContent = 'Binary content (cannot display as text)';
            headerText = 'Decrypted Content';
          }
        }

        outputHeader.textContent = headerText;
        outputContent.textContent = displayContent;
        outputBlock.style.display = 'block';

        const url = URL.createObjectURL(blob);
        const extension = action === 'encrypt' ? 'enc' : 'txt';
        downloadBtn.href = url;
        downloadBtn.download = `${action}_result.${extension}`;
        downloadSection.style.display = 'block';

        showStatus('File processed successfully!', 'success');

      } catch (error) {
        showStatus(`Error: ${error.message}`, 'error');
      } finally {
        processBtn.disabled = false;
        processBtn.textContent = 'Process File';
      }
    });

    function showStatus(message, type) {
      statusMessage.textContent = message;
      statusMessage.className = `status-message status-${type}`;
    }
  });
</script>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/encrypt-decrypt', methods=['POST'])
def encrypt_decrypt_api():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
        
        file = request.files['file']
        tier = request.form.get('tier')
        action = request.form.get('action')
        
        if not file or not tier or not action:
            return jsonify({'error': 'Missing required parameters'}), 400
        
        # Generate keys in memory (no file operations!)
        generate_rsa_keys()
        
        # Get keys from memory dictionary
        if tier == 'public':
            pub_key = RSA_KEYS.get('public_public')
            priv_key = RSA_KEYS.get('private_public')
        else:
            pub_key = RSA_KEYS.get('public_private')
            priv_key = RSA_KEYS.get('private_private')
        
        file_data = file.read()
        
        if action == 'encrypt':
            result_data = encrypt_file_data(file_data, pub_key)
            filename = f'encrypted_{file.filename}.enc'
            mimetype = 'application/octet-stream'
        else:
            result_data = decrypt_file_data(file_data, priv_key)
            filename = f'decrypted_{file.filename.replace(".enc", "")}.txt'
            mimetype = 'text/plain'
        
        return send_file(
            io.BytesIO(result_data),
            as_attachment=True,
            download_name=filename,
            mimetype=mimetype
        )
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Export for Vercel
app = app

if __name__ == '__main__':
    app.run(debug=True)
