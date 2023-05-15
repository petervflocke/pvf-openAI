import openai

openai.api_key = 'YOUR_API_KEY'

response = openai.ChatCompletion.create(
  model="gpt-3.5-turbo",
  messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Who won the world series in 2020?"},
        {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
        {"role": "user", "content": "Where was it played?"}
    ]
)

# Get the list of messages in the response
messages = response['choices'][0]['message']['content']

# Concatenate the contents of all the messages into a single string
full_answer = ''.join([message['content'] for message in messages])

print(full_answer)
