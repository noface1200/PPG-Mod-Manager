import os, json, tkinter as tk, tkinter.filedialog as filedialog
from PIL import Image, ImageTk

class ModManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Noface's People Playground Mod viewer")
        self.root.geometry("600x600")
        self.root.config(bg="#121212")

        self.icons = {}

        self.path_label = tk.Label(root, text="Mod Folder Path:", bg="#121212", fg="white")
        self.path_label.pack(pady=5)

        self.path_entry = tk.Entry(root, width=50, bg="#1e1e1e", fg="white", insertbackground='white')
        self.path_entry.pack(pady=5)

        self.browse_button = tk.Button(root, text="Browse", command=self.browse_folder, bg="#1e1e1e", fg="white")
        self.browse_button.pack(pady=5)

        self.load_button = tk.Button(root, text="Load Mods", command=self.load_mods, bg="#1e1e1e", fg="white")
        self.load_button.pack(pady=5)

        self.frame = tk.Frame(root, bg="#121212")
        self.frame.pack(fill=tk.BOTH, expand=True)

        self.mod_canvas = tk.Canvas(self.frame, bg="#121212")
        self.mod_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.scrollbar = tk.Scrollbar(self.frame, orient=tk.VERTICAL, command=self.mod_canvas.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.mod_canvas.config(yscrollcommand=self.scrollbar.set)

        self.mod_frame = tk.Frame(self.mod_canvas, bg="#121212")
        self.mod_canvas.create_window((0, 0), window=self.mod_frame, anchor="nw")

        self.mod_frame.bind("<Configure>", lambda e: self.mod_canvas.configure(scrollregion=self.mod_canvas.bbox("all")))

    def browse_folder(self):
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.path_entry.delete(0, tk.END)
            self.path_entry.insert(0, folder_selected)

    def load_mods(self):
        folder_path = self.path_entry.get()
        if os.path.isdir(folder_path):
            for mod_folder in os.listdir(folder_path):
                mod_path = os.path.join(folder_path, mod_folder, "mod.json")
                if os.path.isfile(mod_path):
                    with open(mod_path, 'r') as f:
                        mod_data = json.load(f)
                        self.display_mod(
                            mod_data.get("Name", "Unknown Mod"),
                            os.path.join(folder_path, mod_folder, mod_data.get("ThumbnailPath", "")),
                            mod_data.get("Author", "Unknown Author"),
                            mod_data.get("Description", "No description available."),
                            mod_data.get("ModVersion", "N/A"),
                            mod_data.get("GameVersion", "N/A")
                        )

    def display_mod(self, mod_name, thumbnail_path, author, description, mod_version, game_version):
        mod_entry_frame = tk.Frame(self.mod_frame, bg="#1e1e1e")
        mod_entry_frame.pack(fill=tk.X, pady=10)

        if thumbnail_path and os.path.isfile(thumbnail_path):
            image = Image.open(thumbnail_path)
            image = image.resize((50, 50))
            photo = ImageTk.PhotoImage(image)
            self.icons[mod_name] = photo
            image_label = tk.Label(mod_entry_frame, image=photo, bg="#1e1e1e")
            image_label.image = photo
            image_label.pack(side=tk.LEFT, padx=5)
        else:
            placeholder = tk.Label(mod_entry_frame, text="[No Image]", width=10, height=5, bg="#1e1e1e", fg="white")
            placeholder.pack(side=tk.LEFT, padx=5)

        mod_info_frame = tk.Frame(mod_entry_frame, bg="#1e1e1e")
        mod_info_frame.pack(side=tk.LEFT, fill=tk.X, padx=10, expand=True)

        mod_name_label = tk.Label(mod_info_frame, text=mod_name, anchor="w", font=("Arial", 14, "bold"), bg="#1e1e1e", fg="white")
        mod_name_label.pack(anchor="w")

        mod_info_label = tk.Label(mod_info_frame, text=f"Author: {author}\nDescription: {description}\nMod Version: {mod_version}\nGame Version: {game_version}", anchor="w", justify=tk.LEFT, bg="#1e1e1e", fg="white")
        mod_info_label.pack(anchor="w")

root = tk.Tk()
mod_manager = ModManager(root)
root.mainloop()
