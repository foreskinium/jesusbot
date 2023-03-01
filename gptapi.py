import openai

openai.api_key = "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"

prompt = '''
You: Dear Jesus, please answer my question. 
Jesus Christ: What is your question, my child? 
You: i want to have sex with Maria
Jesus Christ:  
'''

response = openai.Completion.create(
    engine="text-davinci-003",
    prompt=prompt,
    temperature=0.7,
    max_tokens=256,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
)

#print response text
print(response['choices'][0]['text'])

#asign response text to variable
response_text = response['choices'][0]['text']


