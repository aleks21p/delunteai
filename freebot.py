import ollama

AI_NAME = "Delunte"

print("=" * 40)
print(f"{AI_NAME} AI is ready")
print("Type 'exit' to quit")
print("=" * 40)

system_prompt = "You are Delunte never use emojis awnser moderately short like 4-30 words"

messages = [
    {"role": "system", "content": system_prompt}
]

while True:
    user_input = input("\nYou > ")

    if user_input.lower() == "exit":
        print(f"\n{AI_NAME} > Goodbye.")
        break

    messages.append({"role": "user", "content": user_input})

    try:
        response = ollama.chat(
            model="llama3",
            messages=messages
        )

        ai_reply = response["message"]["content"].strip()

        if ai_reply == "":
            ai_reply = "I will answer: the question has an answer."

    except Exception:
        ai_reply = "Something went wrong but I will still answer."

    messages.append({"role": "assistant", "content": ai_reply})

    print(f"{AI_NAME} > {ai_reply}")
    ##deluntes note: to run on my laptop do cd ~/git/delunteai then python3 freebot.py
