from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS
from g4f.client import Client

app = Flask(__name__)
CORS(app)  # Enable CORS for cross-origin requests

# Home route to display a simple message
@app.route('/')
def home():
    return jsonify({"message": "Flask server is running!"})

# Function to chunk a long message into smaller parts
def chunk_message(message, chunk_size=5000):
    # Split the message into smaller chunks
    return [message[i:i + chunk_size] for i in range(0, len(message), chunk_size)]

# Define the route to send messages
@app.route('/send_message', methods=['POST'])
def send_message():
    user_message = request.json.get('message')  # Get the message from the POST request body
    if not user_message:
        return jsonify({"error": "Message is empty!"}), 400

    # Chunk the user message
    message_chunks = chunk_message(user_message)

    client = Client()
    full_response = ""

    # Send each chunk to the GPT model and gather responses
    for chunk in message_chunks:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": chunk}],
        )
        gpt_response = response.choices[0].message.content
        full_response += gpt_response + " "  # Combine the responses

    # Return the full GPT response as JSON
    return jsonify({"response": full_response.strip()}), 200

if __name__ == '__main__':
    app.run(debug=True)
