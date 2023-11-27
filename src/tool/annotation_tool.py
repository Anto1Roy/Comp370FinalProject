import json
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox

import pandas as pd

class FileOutputApp:
    def __init__(self, root, articles, url_list, start_index, end_index):
        self.root = root
        self.root.title("Annotation Tool")

        self.url_list = url_list

        # Set the size of the window
        self.root.geometry("400x400")  # Change the width and height as needed
        
        self.input_label = tk.Label(root, text="Content:")
        self.input_label.pack()

        self.input_content = tk.StringVar() 

        self.input_label_display = tk.Label(root, textvariable=self.input_content, wraplength=300,  width=150, height=15, anchor='n')
        self.input_label_display.pack()
        

        # Create the buttons
        self.next_button = tk.Button(root, text="Next", command=lambda: self.next_content(), state=tk.NORMAL)
        self.next_button.pack(side=tk.RIGHT, padx=20)

        # Create a frame to hold the buttons
        button_frame = tk.Frame(root)
        button_frame.pack(side=tk.TOP, anchor=tk.CENTER)

        self.save_button1 = tk.Button(button_frame, text="Positive", command=lambda: self.save_to_button("Positive"), state=tk.NORMAL)
        self.save_button1.pack(side=tk.LEFT, padx=20)

        self.save_button2 = tk.Button(button_frame, text="Negative", command=lambda: self.save_to_button("Negative"), state=tk.NORMAL)
        self.save_button2.pack(side=tk.LEFT, padx=20)

        self.save_button3 = tk.Button(button_frame, text="Neutral", command=lambda: self.save_to_button("Neutral"), state=tk.NORMAL)
        self.save_button3.pack(side=tk.LEFT, padx=20)

        self.initialize(articles, start_index, end_index)


    def initialize(self, articles, start_index, end_index):
        self.current_index = 0
        self.current_article = start_index
        self.end_index = end_index
        self.articles = articles
        self.results = []  # List of tuples (currentNumber, buttonNumber)

        self.display_current_item()

    def next_article(self):
        self.current_index = 0
        self.current_article += 1
        self.input_content.set("")
        self.input_label_display.config(text="")
        if self.articles[self.current_article] != None:
            if self.current_index == len(self.articles[self.current_article]) - 1:
                self.next_button.config(state=tk.DISABLED)
            else:
                self.next_button.config(state=tk.NORMAL)
        else:
            self.next_button.config(state=tk.DISABLED)
        

        self.display_current_item()

    def next_content(self):
        self.current_index = self.current_index + 1
        self.input_content.set("")
        self.input_label_display.config(text="")

        # if last cotnent
        if self.current_index == len(self.articles[self.current_article]) - 1:
            self.next_button.config(state=tk.DISABLED)

        self.display_current_item()
        

    def save_to_button(self, button_number):
        try:
            self.results.append((self.url_list[self.current_article], button_number))

            if self.current_article < len(self.articles) - 1 and self.current_index < self.end_index:
                self.next_article()
            else:
                # Close the window if all elements are processed
                self.root.destroy()     
        except ValueError:
            self.show_error("Entered text not found in the list.")


    def display_current_item(self):
        # Display the content of the current item in the label
        if self.articles[self.current_article] == None or len(self.articles[self.current_article]) == 0:
             current_item = f"open url : {url_list[self.current_article]}"
        else :
            if len(self.articles[self.current_article][self.current_index]) < 10:
                self.next_content()
            current_item = self.articles[self.current_article][self.current_index]
        self.input_content.set(current_item)

    def show_message(self, message):
        messagebox.showinfo("Message", message)

    def show_error(self, message):
        messagebox.showerror("Error", message)

    def map_results_with_csv(self, user, csv_file_path):
        # Read the existing CSV file
        df = pd.read_csv(csv_file_path)

        # Check if the user column already exists
        if user not in df.columns:
            # If it doesn't exist, add a new column for the user
            df[user] = None

        print(self.results)

        # Fill in the answers for the new user
        for result in self.results:
            index = df.index[df['url'] == result[0]].tolist()[0]
            df.at[index, user] = result[1]

        # Save the updated DataFrame back to the CSV file
        df.to_csv(csv_file_path, index=False)

if __name__ == "__main__":

    import sys

    if len(sys.argv) != 4:
        print("Usage: python script.py <user> <start_index> <end_index>")
        sys.exit(1)


    root = tk.Tk()

    user = sys.argv[1]
    start_index = int(sys.argv[2])
    end_index = int(sys.argv[3])

    csv_file_path = Path(__file__).parent.parent.parent / 'data/articles/results.csv'

    # receive json and transform into list of lists

    json_content = json.load(open(Path(__file__).parent.parent.parent / 'data/articles/content_swift.json', 'r'))
    # Example list of lists
    url_list = list(json_content.keys())
    input_content = []
    for url in url_list:
        input_content.append(json_content[url]['paragraphs'])

    app = FileOutputApp(root, input_content, url_list, start_index, end_index)

    root.mainloop()

    app.map_results_with_csv(user, csv_file_path)
