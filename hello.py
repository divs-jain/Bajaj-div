from google import genai

# Replace with your actual Gemini API key
API_KEY = "YOUR_API_KEY"

def main():
    # Initialize the Gemini client
    client = genai.Client(api_key=API_KEY)

    # 1. Upload file - update path as needed
    file_path = "BAJHLIP23020V012223.pdf"
    with open(file_path, "rb") as f:
        uploaded_file = client.files.upload(
            file=f,
            config={"mime_type": "application/pdf"}
        )
    print(f"File uploaded: {uploaded_file.uri}")

    # 2. Initialize conversation with the file message
    conversation = [
        {
            "role": "user",
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

    # 3. Start interactive chat loop
    while True:
        user_input = input("\nYou: ").strip()
        if user_input.lower() == "exit":
            print("Conversation ended.")
            break

        conversation.append({"role": "user", "parts": [{"text": user_input}]})

        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=conversation
            )
        except Exception as e:
            print(f"Error communicating with Gemini API: {e}")
            continue

        print("\nGemini:", response.text)
        conversation.append({"role": "model", "parts": [{"text": response.text}]})

if __name__ == "__main__":
    main()
