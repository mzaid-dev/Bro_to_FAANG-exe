from model import client

chat_history = []

while True:
    print("Bot: ", end="", flush=True)
    
    user_prompt = input()

    output = ""

    print("Ai: ", end="", flush=True)
    for chuck in client.stream(user_prompt):
        if chuck.content:
            output += chuck.content
            print(chuck.content,end="",flush=True)

    chat_history.append(output)
    print()


    # print(chat_history)

    