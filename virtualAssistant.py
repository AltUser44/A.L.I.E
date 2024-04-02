import tkinter as tk
from tkinter import messagebox
import random
import requests


class VirtualAssistant:
    def __init__(self, master):
        self.master = master
        self.master.title("ALLIE - Virtual Assistant")
        self.master.geometry("400x400")

        # Define fonts and colors
        question_font = ("Helvetica", 14, "bold")
        response_font = ("Helvetica", 12)
        background_color = "#FFE4E1"  # MistyRose

        self.greetings = ["Hello User!", "Hi there User!", "Greetings User!", "Hey User!",]

        self.greeting_label = tk.Label(master, text="", font=response_font, bg=background_color)
        self.greeting_label.pack(pady=30)

        self.user_input_entry = tk.Entry(master, width=20, font=question_font)
        self.user_input_entry.pack(pady=10)

        self.response_label = tk.Label(master, text="", font=response_font, wraplength=380, justify="left",
                                       bg=background_color)
        self.response_label.pack(pady=10)

        self.respond_button = tk.Button(master, text="Ask ALLIE", command=self.respond, font=response_font,
                                        bg="#FFA07A")  # LightSalmon
        self.respond_button.pack(pady=10)

        # Initialize the virtual assistant with a random greeting
        self.greet_user()

    def greet_user(self):
        greeting = random.choice(self.greetings)
        self.greeting_label.config(text=greeting)

    def respond(self):
        user_input = self.user_input_entry.get().strip().lower()

        if user_input in ["exit", "quit", "bye"]:
            self.master.destroy()
        else:
            response = self.virtual_assistant(user_input)
            self.response_label.config(text=response)

    def virtual_assistant(self, user_input):
        # Maximum number of characters to display in the text box
        max_chars = 280  # You can adjust this value as needed

        url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{user_input}"
        headers = {'User-Agent': 'Mozilla/5.0'}
        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                data = response.json()
                if 'extract' in data:
                    summary = data['extract']
                    # End the summary at the last complete sentence within max_chars
                    if len(summary) > max_chars:
                        truncated_summary = summary[:max_chars]
                        last_period = truncated_summary.rfind('.')
                        if last_period == -1:
                            # No period found, so we have to cut off without ending a sentence
                            return truncated_summary + "..."
                        else:
                            # End after the last complete sentence
                            return truncated_summary[:last_period + 1]
                    else:
                        return summary
                else:
                    return "Sorry, I couldn't find any information on that topic."
            else:
                return "Sorry, there was an error fetching the information."
        except requests.RequestException:
            return "An error occurred while trying to fetch data."


if __name__ == "__main__":
    root = tk.Tk()
    root.configure(bg="#FFE4E1")  # MistyRose
    app = VirtualAssistant(root)
    root.mainloop()
