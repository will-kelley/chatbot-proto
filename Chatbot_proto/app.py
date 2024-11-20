from flask import Flask, render_template, request, jsonify
import json, random
import re
import difflib

app = Flask(__name__)

# Load predefined responses (located in the responses.json file)
with open("data/responses.json", "r") as file:
    responses = json.load(file)

# GLOBAL context variable to track conversation state
context = {"last_question": None}

# Suggestion helper function
def suggest_closest_input(user_input, valid_inputs):
    closest_match = difflib.get_close_matches(user_input, valid_inputs, n=1, cutoff=0.6)
    if closest_match:
        return closest_match[0]
    return None


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/get_response", methods=["POST"])
def get_response():
    global context

    # Retriving user input
    user_input = request.json.get("message", "").lower()

    # Default responses #
    # Determining which default response to use at random
    default_responses = [
    "I'm sorry, I don't understand that.",
    "Can you rephrase your question?",
    "Did you mean one of these: 'agent', 'help', 'math'?"
    ]

    # Check for an exact match
    response = responses.get(user_input, None)

    # Helper function for "yes/no" validation
    def validate_yes_no(user_input):
        yes_variations = {"yes", "yep", "yeah", "ya", "sure", "ok", "okay", "yea"}
        no_variations = {"no", "na", "nope", "not really", "nah"}
        if user_input in yes_variations:
            return "yes"
        elif user_input in no_variations:
            return "no"
        return None
    
    # Context tracker
    if context["last_question"] == "agent":
        validated_response = validate_yes_no(user_input)
        if validated_response == "yes":
            response = "Connecting you to an agent now. We thank you for your patience."
            context["last_question"] = None # Reset after resolution
        elif validated_response == "no":
            response = "Okay, let me know if there is anything else I can help you with!"
            context["last_question"] = None
        else:
            response = "Would you like to speak with an agent? Please response with 'yes' or 'no'."
    elif "agent" in user_input:
        response = "Would you like to speak with an agent? Please response with 'yes' or 'no'."
        context["last_question"] = "agent"

    # Math expression handler
    if re.search(r'\d+(\s*[-+*/x]\s*\d+)+', user_input):
        try:
            # Replace 'x' with '*' for multiplication
            expression = user_input.replace("x", "*")
            # Extract the math expression from the input using regex
            math_expression = re.search(r'(\d+(\s*[-+*/]\s*\d+)+)', expression).group(0)
            # Evaluate the expression
            result = eval(math_expression)
            response = f"The result of {math_expression} is {result}."
        except Exception as e:
            response = "I'm sorry, I couldn't calculate that. If you meant to answer a math expression, please ensure that it is valid."

    if not response:
        valid_inputs  = list(responses.keys())
        closest_match = suggest_closest_input(user_input, valid_inputs)

        if closest_match:
            response = f"I'm sorry did you mean '{closest_match}'?"
        else:
            response = random.choice(default_responses)

    return jsonify({"response": response})        


if __name__ == "__main__":
    app.run(debug=True)