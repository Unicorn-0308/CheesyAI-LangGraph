with open("prompt_templates/json2text.md") as f:
    prompt_json2text = f.read()
    f.close()

with open("prompt_templates/isCheeseChat.md") as f:
    isCheeseChat = f.read()
    f.close()

with open("prompt_templates/query2filter.md") as f:
    query2filter = f.read()
    f.close()

with open("prompt_templates/query2mongo.md") as f:
    query2mongo = f.read()
    f.close()

with open("prompt_templates/system.md") as f:
    system = f.read()
    f.close()

with open("prompt_templates/hello.md") as f:
    hello = f.read()
    f.close()

with open("prompt_templates/general.md") as f:
    general = f.read()
    f.close()