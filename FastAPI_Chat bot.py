from fastapi import FastAPI, HTTPException, Form
from fastapi.responses import HTMLResponse
import pandas as pd

# Load the dataset into a Pandas DataFrame
df = pd.read_csv('C:/Dataset/chatbot_data.csv')  # Adjust path as per your actual file location

# Initialize FastAPI
app = FastAPI()

# Define the HTML form content as a string
html_form = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Simple Chatbot API</title>
</head>
<body>
    <h1>Simple Chatbot API</h1>
    <form action="/chatbot/" method="post">
        <label for="query">Enter your query:</label><br>
        <input type="text" id="query" name="query"><br>
        <input type="submit" value="Submit">
    </form>
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
async def main():
    return html_form

@app.post("/chatbot/", response_class=HTMLResponse)
async def chatbot(query: str = Form(...)):
    query = query.strip().lower()  # Convert query to lowercase and strip whitespace

    # Search for matching intent in the dataset
    result = df[df['instruction'].str.lower().str.contains(query, na=False)]

    if result.empty:
        raise HTTPException(status_code=404, detail="No matching intent found.")

    # Get the first response (you can modify this logic based on your dataset structure)
    response = result.iloc[0]['response']

    return f"<h2>Query: {query}</h2><p>Response: {response}</p>"

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)
