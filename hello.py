from google import genai

# Initialize Gemini client
client = genai.Client(api_key="AIzaSyBIpp_V4UXlggz7LPgNrapcl-gmiJbsmW0")

# 1. Upload file
file_path = "BAJHLIP23020V012223.pdf"  # replace with your file
uploaded_file = client.files.upload(
    file=open(file_path, "rb"),
    config={"mime_type": "application/pdf"}
)
print(f"File uploaded: {uploaded_file.uri}")

# 2. Initialize conversation history
conversation = [
    {
        "role": "user",  # first message includes file
        "parts": [
            {
                "file_data": {
                    "file_uri": uploaded_file.uri,
                    "mime_type": uploaded_file.mime_type
                }
            },
            {"text": "This is the document for our chat."}
        ]
    }
]

# 3. Continuous chat loop
while True:
    user_input = input("\nYou: ")

    if user_input.lower() == "exit":
        print("Conversation ended.")
        break

    # Append user message
    conversation.append({"role": "user", "parts": [{"text": user_input}]})

    # Send conversation to Gemini
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=conversation
    )

    # Print response
    print("\nGemini:", response.text)

    # Append model response
    conversation.append({"role": "model", "parts": [{"text": response.text}]})
