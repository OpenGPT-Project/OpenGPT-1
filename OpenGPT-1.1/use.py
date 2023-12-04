import json
import re
import time

def use(json_file_path, user_input, token_limit=3):
    with open(json_file_path, 'r') as file:
        data = json.load(file)

    all_text = ' '.join(data['text'])
    words = re.findall(r'\b\w+\b', all_text.lower())

    try:
        input_index = words.index(user_input.lower())
    except ValueError:
        similar_words = [word for word in words if user_input.lower() in word]
        
        if not similar_words:
            return f'Sorry, I couldn\'t find "{user_input}" or any similar words in the text.'
        
        user_input = similar_words[0]
        input_index = words.index(user_input)

    tokens_after_input = words[input_index + 1:input_index + 1 + token_limit]
    
    unique_tokens = []
    token_count = 0
    for token in tokens_after_input:
        if token not in unique_tokens:
            unique_tokens.append(token)
            token_count += 1

        if token_count >= token_limit:
            break
    
    text_after_input = ' '.join(unique_tokens)

    slow_output(text_after_input)

def slow_output(text):
    for word in text.split():
        print(word, end=' ', flush=True)
        time.sleep(0.0425)
    print()

json_file_path = 'data.json'
user_input = input('You can tell me a word or a few words: ')
token_limit = int(input('Enter the token limit: '))
time.sleep(0.0425)
print(user_input, end=' ', flush=True)
result = use(json_file_path, user_input, token_limit)
