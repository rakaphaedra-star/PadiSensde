from google import genai

client = genai.Client(
    api_key="AIzaSyBsFZF6UtgNqMLh9XPC5SdPhTYAl7iDN8w"
)

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Halo bro, apa kabar?"
)

print(response.text)