from fastapi import FastAPI, HTTPException, Form
from fastapi.responses import HTMLResponse
import pandas as pd
import numpy as np
import asyncio

# Load the dataset into a Pandas DataFrame
df = pd.read_csv('C:/Dataset/chatbot_data.csv')  # Adjust path as per your actual file location

# Initialize FastAPI
app = FastAPI()

# HTML form content as a string
html_form = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Simple Chatbot API</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 20px;
        }
        .chat-container {
            width: 70%;
            margin: auto;
            border: 1px solid #ccc;
            padding: 20px;
            border-radius: 5px;
        }
        .chat-message {
            margin-bottom: 10px;
            padding: 10px;
            background-color: #f2f2f2;
            border-radius: 5px;
        }
    </style>
</head>
<body>
    <div class="chat-container">
        <h1>Simple Chatbot API</h1>
        <div id="chat-log"></div>
        <form id="chat-form">
            <label for="category">Select category:</label><br>
            <select id="category" name="category">
                <option value="card">Card</option>
                <option value="loan">Loan</option>
                <option value="transfer">Transfer</option>
                <option value="others">Others</option>
            </select><br><br>
            <label for="query">Enter your query:</label><br>
            <input type="text" id="query" name="query" list="query-options" autocomplete="off"><br><br>
            <datalist id="query-options"></datalist>
            <button type="submit">Submit</button>
        </form>
    </div>

    <script>
        const autocompleteData = {
            "card": [
                "Can you help me activate a card?",
                "I need to activate a card on mobile",
                "I'd like to activate a Master Card for international usage, can I get some help?"
            ],
            "loan": [
                "I need a loan, can you help me apply?",
                "How can I apply for a loan?",
                "I'm looking folr a loan, where could I find it?"
            ],
            "transfer": [
                "i transferred money to the wrong account help me canceling a bank transfer",
                "How can I cancel a bank transfer?",
                "i have to cancel a bank transfer to a cxontact i need assistance"
            ]
        };

        // Function to update autocomplete options based on category
        function updateAutocompleteOptions(category, input) {
            const datalist = document.getElementById("query-options");
            datalist.innerHTML = ""; // Clear previous options

            if (autocompleteData.hasOwnProperty(category)) {
                const suggestions = autocompleteData[category].filter(item => item.toLowerCase().startsWith(input.toLowerCase()));
                suggestions.forEach(item => {
                    const option = document.createElement("option");
                    option.value = item;
                    datalist.appendChild(option);
                });
            }
        }

        // Event listener for category change
        document.getElementById("category").addEventListener("change", function() {
            const category = this.value;
            const input = document.getElementById("query").value;
            updateAutocompleteOptions(category, input);
        });

        // Event listener for query input
        document.getElementById("query").addEventListener("input", function() {
            const category = document.getElementById("category").value;
            const input = this.value;
            updateAutocompleteOptions(category, input);
        });

        // Event listener for form submission
        document.getElementById("chat-form").addEventListener("submit", async function(event) {
            event.preventDefault();
            let category = document.getElementById("category").value;
            let query = document.getElementById("query").value;
            let formData = new FormData();
            formData.append("category", category);
            formData.append("query", query);

            try {
                let response = await fetch('/chatbot/', {
                    method: 'POST',
                    body: formData
                });

                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }

                let result = await response.text();
                document.getElementById("chat-log").innerHTML += result;
                document.getElementById("query").value = ''; // Clear input field
                updateAutocompleteOptions(category, ''); // Clear autocomplete options after submission
            } catch (error) {
                console.error('Error:', error);
            }
        });
    </script>
</body>
</html>
"""

# Simple linear regression model using TensorFlow for demonstration
def train_model():
    model = tf.keras.models.Sequential([
        tf.keras.layers.Dense(1, input_shape=(1,))
    ])
    model.compile(optimizer='sgd', loss='mean_squared_error')

    for epoch in range(1, 6):  # Train for 5 epochs for demonstration
        model.fit(X, y, epochs=1, verbose=0)  # Training step
        if epoch == 2.5:
            break  # Stop training at epoch 2.5

    return "Training completed up to epoch 2.5"

@app.get("/", response_class=HTMLResponse)
async def main():
    return html_form

@app.post("/chatbot/", response_class=HTMLResponse)
async def chatbot(category: str = Form(...), query: str = Form(...)):
    category = category.lower().strip()
    query = query.strip().lower()

    if category in ["card", "loan", "transfer"]:
        # Search for matching intent in the dataset based on selected category
        result = df[df['category'].str.lower() == category]
        if result.empty:
            fallback_response = "No relevant information found."
        else:
            result = result[result['instruction'].str.lower().str.contains(query, na=False)]
            if result.empty:
                fallback_response = "No relevant information found."
            else:
                response = result.iloc[0]['response']
                fallback_response = f"Chatbot Response: {response}"
    elif category == "others":
        # Directly use the query to find relevant responses in the dataset
        result = df[df['instruction'].str.lower().str.contains(query, na=False)]
        if result.empty:
            fallback_response = "Thank you for using Chatbot. We request you to call our customer care number 1800 123 123 or email us at ourbank@domain.com."
        else:
            response = result.iloc[0]['response']
            fallback_response = f"Chatbot Response: {response}"
    else:
        fallback_response = "Invalid category selected."

    html_response = f'<div class="chat-message"><strong>User:</strong> {query}</div>'
    html_response += f'<div class="chat-message"><strong>Chatbot:</strong> {fallback_response}</div>'

    return HTMLResponse(content=html_response)

@app.post("/train/", response_class=HTMLResponse)
async def start_training():
    # Simulated training process
    result = train_model()
    return result

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8020)
