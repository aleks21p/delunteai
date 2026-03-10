from flask import Flask, request, jsonify
from flask_cors import CORS
import ollama
import base64

app = Flask(__name__)
CORS(app)

system_prompt = "respond in between 1-50 words"

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_message = data.get("message", "")
    file_data = data.get("file")
    file_name = data.get("fileName", "")
    history = data.get("history", [])
    
    # Build messages list with history
    messages = []
    
    # Add previous messages from history
    for hist_msg in history:
        if hist_msg.get("role") == "user":
            messages.append({"role": "user", "content": hist_msg.get("content", "")})
        elif hist_msg.get("role") == "ai":
            messages.append({"role": "assistant", "content": hist_msg.get("content", "")})
    
    # If there's a file, process it
    if file_data:
        # Remove the data URL prefix if present
        if file_data.startswith("data:"):
            file_data = file_data.split(",")[1]
        
        # Decode base64
        file_bytes = base64.b64decode(file_data)
        
        # Check if it's an image file
        if file_name.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp')):
            # Use llava model for image analysis
            prompt = user_message if user_message else "What is in this image?"
            
            response = ollama.chat(
                model="llava",
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                        "images": [file_data.split(",")[-1] if "," in file_data else file_data]
                    }
                ]
            )
        else:
            # For other files, try to read as text
            try:
                file_content = file_bytes.decode('utf-8', errors='ignore')
                prompt = f"Here's a file ({file_name}):\n\n{file_content}\n\n{user_message}" if user_message else f"Analyze this file ({file_name}):\n\n{file_content}"
            except:
                prompt = f"User uploaded file: {file_name}. {user_message}" if user_message else f"User uploaded: {file_name}"
            
            messages.append({"role": "user", "content": prompt})
            
            response = ollama.chat(
                model="llama3",
                messages=messages
            )
    else:
        # Add current user message to messages
        messages.append({"role": "user", "content": user_message})
        
        # Use text model with history
        response = ollama.chat(
            model="llama3",
            messages=[
                {"role": "system", "content": system_prompt}
            ] + messages
        )

    return jsonify({"reply": response["message"]["content"]})

app.run(port=5050)