import os
import cohere
import subprocess

# Initialize Cohere API
API_KEY = "vZwXDrGNmlU01We0CQbdejyzCqZiQXds5Tyi3cAa"
co = cohere.Client(API_KEY)

def generate_code(user_input):
    """Generate code using Cohere API and save it to a plain text file, then open it in Notepad."""
    try:
        # Generate code
        response = co.generate(
            model="command-xlarge-nightly",  # Use the appropriate model for your needs
            prompt=user_input,
            max_tokens=1000,
            temperature=0.7,
        )
        code = response.generations[0].text.strip()

        # Prepare file path
        file_name = user_input.lower().replace(" ", "_") + ".txt"
        file_path = os.path.join("Data", "Scripts", file_name)

        # Ensure the directory exists
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        # Save the generated code to the file
        with open(file_path, "w") as file:
            file.write(code)

        print(f"Code saved to: {file_path}")

        # Open the file in Notepad
        try:
            subprocess.run(["notepad", file_path], check=True)
        except Exception as e:
            print(f"Failed to open file in Notepad: {e}")
    except Exception as e:
        print(f"Error generating code: {e}")

def main():
    print("Code Generator Bot")
    print("Enter your request (e.g., 'create a bot using python') or 'exit' to quit:")

    while True:
        user_input = input("Request: ")
        if user_input.lower() == "exit":
            break

        generate_code(user_input)

if __name__ == "__main__":
    main()
