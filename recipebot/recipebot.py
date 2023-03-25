import os
import openai
import time
from Adafruit_IO import Client, Feed

my_secret = os.environ['OAI KEY']
openai.api_key = my_secret

#prompt = "Give me a short recipe with 10 ingredients or less. Keep response to 30 words or less.No seafood or Shellfish."
prompt_a = ' You are a helpful food expert. Give me an idea of what to cook for breakfast. Make sure it has no more than 10 ingredients and does not include seafood. Keep response to less than 37 words.'

prompt_b = ' You are a helpful food expert. Give me an idea of what to cook for lunch. Make sure it has no more than 12 ingredients and does not include seafood or stir-fry. Keep response to less than 37 words.'

prompt_c = ' You are a helpful food expert. Give me an idea of what to cook for dinner. Make sure it has no more than 10 ingredients and does not include seafood. Keep response to less than 37 words.'

prompt_d = ' You are a wise philospher who is well versed in all schools of philosophy and loves to give rhyming advice. Give me some encouraging words of wisdom for today. Make sure your response has no more than 37 words.'

def chipGPT(prompt):
  completion = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=[
     {"role": "user", "content": prompt},


    ]
  )
  reply = (completion.choices[0].message.content)
  return reply

#print(chipGPT(prompt))


run_count = 0

a_key = os.environ['Adafruit key']
a_username = os.environ['adafruit username']
ADAFRUIT_IO_KEY = a_key
ADAFRUIT_IO_USERNAME = a_username

# Create an instance of the REST client.
aio = Client(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)

feed = Feed(name="recipe")
#response = aio.create_feed(feed)
r = aio.feeds('recipe')

print("recipe bot online")

a = "Breakfast"
b = "Lunch"
c = "Dinner"
d = "Wisdom"

while True:
  data = aio.receive(r.key)

  if data.value == a:
    run_count += 1
    print('sending count: ', run_count)
    aio.send_data('recipe', chipGPT(prompt_a))
  time.sleep(1)
  if data.value == b:
    run_count += 1
    print('sending count: ', run_count)
    aio.send_data('recipe', chipGPT(prompt_b))
  time.sleep(1)
  if data.value == c:
    run_count += 1
    print('sending count: ', run_count)
    aio.send_data('recipe', chipGPT(prompt_c))
  time.sleep(1)
  if data.value == d:
    run_count += 1
    print('sending count: ', run_count)
    aio.send_data('recipe', chipGPT(prompt_d))
  time.sleep(1)


