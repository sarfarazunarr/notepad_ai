import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import os
from g4f.client import Client
import asyncio


class Notepad:
    def __init__(self, root):
        self.root = root
        self.root.title("Notepad AI")
        self.root.geometry("800x600")
        self.text_area = tk.Text(self.root, undo=True, font=("Arial", 12), padx=10, pady=10)
        self.text_area.pack(expand=True, fill="both", padx=5, pady=5)
        self.create_menu()
        self.filename = None

        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        self.client = Client()

    def create_menu(self):
        menubar = tk.Menu(self.root)
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="New", command=self.new_file)
        file_menu.add_command(label="Open", command=self.open_file)
        file_menu.add_command(label="Save", command=self.save_file)
        file_menu.add_command(label="Save As", command=self.save_as)

        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.exit_app)
        menubar.add_cascade(label="File", menu=file_menu)

        edit_menu = tk.Menu(menubar, tearoff=0)
        edit_menu.add_command(label="Undo", command=self.text_area.edit_undo)
        edit_menu.add_command(label="Redo", command=self.text_area.edit_redo)
        edit_menu.add_separator()
        edit_menu.add_command(label="Cut", command=self.cut)
        edit_menu.add_command(label="Copy", command=self.copy)
        edit_menu.add_command(label="Paste", command=self.paste)
        menubar.add_cascade(label="Edit", menu=edit_menu)

        ai_menu = tk.Menu(menubar, tearoff=0)
        ai_menu.add_command(label="Use AI", command=self.use_ai)
        menubar.add_cascade(label="AI", menu=ai_menu)
        self.root.config(menu=menubar)

    def new_file(self):
        self.text_area.delete(1.0, tk.END)
        self.filename = None

    def open_file(self):
        self.filename = filedialog.askopenfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if self.filename:
            self.text_area.delete(1.0, tk.END)
            with open(self.filename, "r") as file:
                self.text_area.insert(1.0, file.read())
    def save_file(self):
        if self.filename:
            try:
                content = self.text_area.get(1.0, tk.END)
                with open(self.filename, "w") as file:
                    file.write(content)
            except Exception as e:
                messagebox.showerror("Error", f"Cannot save file: {str(e)}")

        else:
            self.save_as()
    
    def save_as(self):
        try:
            new_file = filedialog.asksaveasfilename(initialfile="Untitled.txt", defaultextension=".txt", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
            content = self.text_area.get(1.0, tk.END)
            with open(new_file, "w") as file:
                file.write(content)
            self.filename = new_file
        except Exception as e:
            messagebox.showerror("Error", f"Cannot save file: {str(e)}")
    
    def exit_app(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.root.destroy()
    

    # Edit section

    def cut(self):
        self.text_area.event_generate("<<Cut>>")
    def copy(self):
        self.text_area.event_generate("<<Copy>>")
    def paste(self):
        self.text_area.event_generate("<<Paste>>")
    
    def use_ai(self):
        prompt_popup = tk.Toplevel(self.root)
        prompt_popup.title("Enter Your Prompt")
        prompt_popup.geometry("300x200")
        prompt_popup.resizable(False, False)
        prompt_popup.config(bg="#222222")
        prompt_popup.attributes("-topmost", True)

        prompt_label = tk.Label(prompt_popup, text="Enter Your Prompt:", bg="#222222", fg="#ffffff", font=("Arial", 12))
        prompt_label.pack(padx=20, pady=20)

        promptEntry = tk.Entry(prompt_popup, width=30, font=("Arial", 12))
        promptEntry.pack(padx=2, pady=10)

        def get_prompt():
            prompt = promptEntry.get()
            if prompt:
                prompt_popup.destroy()
                self.display_ai_message("AI is writing")
                completion = self.get_chat_completion(prompt)
                self.text_area.insert(tk.END, completion)
                self.text_area.see(tk.END)
        ok_button = tk.Button(prompt_popup, text="OK", command=get_prompt, bg="#4CAF50", fg="#fff", font=("Arial", 12), relief=tk.RAISED, borderwidth=3)
        ok_button.pack(pady=30)
        ok_button.bind("<Enter>", lambda e: ok_button.config(bg="#f5a049"))
        ok_button.bind("<Leave>", lambda e: ok_button.config(bg="#4CAF50"))

    def display_ai_message(self, message):
        self.text_area.insert(tk.END, message + "\n")
        self.text_area.see(tk.END)
        self.text_area.update_idletasks()
        self.root.update_idletasks()
    
    def get_chat_completion(self, prompt):
        messages = [{"role": "user", "content": prompt}]
        completion = self.client.chat.completions.create(model="gpt-3.5-turbo", messages=messages)
        self.display_ai_message("")
        return completion.choices[0].message.content
    
if __name__ == "__main__":
    root = tk.Tk()
    notepad = Notepad(root)
    root.mainloop()
