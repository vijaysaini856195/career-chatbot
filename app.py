# --- Get AI Response ---
    try:
        # Define a list of common greetings
        greetings = ["hello", "hi", "hey", "hii", "helo"]

        # Check if the user's prompt is a simple greeting
        if prompt.lower().strip() in greetings:
            bot_response = "Hello! How can I help you with your career path today?"
        else:
            # If it's not a greeting, create a prompt for the AI
            ai_prompt = f"Based on these interests and skills: '{prompt}', recommend 3 potential career paths with a brief explanation for each."
            
            # Get the response from the model
            response = model.generate_content(ai_prompt)
            bot_response = response.text

    except Exception as e:
        bot_response = f"Sorry, I couldn't process that. Error: {e}"
