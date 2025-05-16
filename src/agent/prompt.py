with open("prompt_templates/json2text.md") as f:
    prompt_json2text = f.read()
    f.close()

with open("prompt_templates/isCheeseChat.md") as f:
    isCheeseChat = f.read()
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

with open("prompt_templates/reasoner.md") as f:
    reasoning = f.read()
    f.close()

with open("prompt_templates/query2tool.md") as f:
    query2tool = f.read()
    f.close()

with open("prompt_templates/history.md") as f:
    history = f.read()
    f.close()