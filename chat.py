import openai
import sys
import threading
import time

# Change api key and base url for your own use.
client = openai.OpenAI(
    api_key="API_KEY",
    # Example: https://generativelanguage.googleapis.com/v1beta/openai/
    base_url="BASE_URL"
)

def loading_spinner(stop_event):
    """Function to display a simple spinner in the CLI."""
    chars = ["|", "/", "-", "\\"]
    while not stop_event.is_set():
        for char in chars:
            if stop_event.is_set():
                break
            sys.stdout.write(f"\rGemini is thinking... {char}")
            sys.stdout.flush()
            time.sleep(0.1)
    sys.stdout.write("\r" + " " * 30 + "\r")
    sys.stdout.flush()

def chat_with_gemini():
    # Since we're using terminal to display the chat, we don't need use Markdown formatting.
    messages = [
        {
            "role": "system", 
            "content": "You are a helpful AI. IMPORTANT: Do not use Markdown formatting. No bolding (**), no italics, no bullet points, and no headers. Return only plain text."
        }
    ]

    print("--- Gemini Flash Chat (Plain Text Mode) ---")
    print("Type 'exit' or 'quit' to stop.\n")

    while True:
        try:
            user_input = input("You: ")
            
            if user_input.lower() in ["exit", "quit"]:
                print("Goodbye!")
                break

            messages.append({"role": "user", "content": user_input})
            stop_loading = threading.Event()
            spinner_thread = threading.Thread(target=loading_spinner, args=(stop_loading,))
            spinner_thread.start()

            try:
                response = client.chat.completions.create(
                    model="gemini-3-flash-preview",
                    messages=messages,
                )
                assistant_reply = response.choices[0].message.content
            finally:
                stop_loading.set()
                spinner_thread.join()

            print(f"\nGemini: {assistant_reply}\n")
            messages.append({"role": "assistant", "content": assistant_reply})

        except KeyboardInterrupt:
            print("\nSession ended.")
            sys.exit()
        except Exception as e:
            print(f"\nAn error occurred: {e}")
            break

if __name__ == "__main__":
    chat_with_gemini()