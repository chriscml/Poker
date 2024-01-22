def envoyerGPT4(my_api_key):
  client = OpenAI(api_key=my_api_key)
  
  # Path to your image
  image_path = "capture.png"
  
  response = client.chat.completions.create(
    model="gpt-4-turbo",
    messages=[
      {
        "role": "user",
        "content": [
          {"type": "text", "text": "What’s in this image?"},
          {
            "type": "image_url",
            "image_url": {
              "url": f"../assets/{image_path}",
            },
          },
        ],
      }
    ],
    max_tokens=300,
  )

  print(response.choices[0])
  
def envoyerGPT(my_api_key):
  client = OpenAI(api_key=my_api_key)
  response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
      {"role": "system", "content": "You are a helpful assistant."},
      {"role": "user", "content": "Who won the world series in 2020?"},
      {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
      {"role": "user", "content": "Where was it played?"}
    ]
  )

  print(response.choices[0].text)
  
  
#envoyerGPT4("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")
#envoyerGPT("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")