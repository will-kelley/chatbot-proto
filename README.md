# Chatbot Prototype
This is a Flask-based chatbot prototype designed to handle user queries, provide predefined responses, perform basic math calculations, and suggest corrections for close matches when user input is unclear. This project serves as a foundation for developing a more advanced bot, including future machine-learning-based solutions.
## Features
### 1. Predefined Responses
- The chatbot uses a JSON file (responses.json) to store predefined key-value pairs for user queries and responses.
Example: If the user inputs "hello", the bot responds with "Hi there!".
### 2. Context-Aware Conversations
- Tracks the state of the conversation with a context object.
Example: If the user asks for an "agent," the bot will ask for confirmation and handle follow-up inputs like "yes" or "no".
### 3. Math Expression Handling
Detects and evaluates mathematical expressions entered by the user.
Example: Inputting "5 + 3" will return "The result of 5 + 3 is 8.".
### 4. Fallback Responses
- Provides fallback responses for unrecognized inputs.
- Randomly selects one of several preconfigured fallback messages to improve the user experience.
### 5. Suggestion Engine
- Uses Python's difflib library to suggest corrections for typos or close matches to valid inputs.
- Example: If the user types "helo", the bot responds with "I'm sorry, did you mean 'hello'?".
