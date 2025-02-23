import tkinter as tk
import subprocess


def split_song():
    url = entry.get()
    subprocess.run(["python3", "song_splitter.py", url])


root = tk.Tk()
root.title("Song Splitter")
root.configure(bg='#00BFFF')
root.geometry("450x200")

header = tk.Frame(root, bg='#00BFFF', height=100)
header.pack(side="top", fill="x")

title = tk.Label(header, text="Song Splitter", font=("Helvetica", 24, "bold"), bg='#00BFFF', fg='white')
title.pack(side="top", pady=30)

body = tk.Frame(root, bg='#b3f2e8')
body.pack(side="bottom", fill="both", expand=True)

entry = tk.Entry(body, font=("Helvetica", 14), relief="groove")
entry.pack(pady=10)

button = tk.Button(body, text="OK", command=split_song, font=("Console", 14, "bold"))
button.pack()

root.mainloop()
