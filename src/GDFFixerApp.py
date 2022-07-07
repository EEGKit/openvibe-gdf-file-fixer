import tkinter.filedialog
import tkinter as tk
import os

from GDFFixer import GDFFixer


class GDFFixerApp:
    """
    The class GDFFixer is an GUI application allowing to open GDF files in order to
    check whether they are corrupted and attempt to fix them

    This
    """
    def __init__(self):
        self.window_width = 400
        self.window_length = 400

        self.root = tk.Tk()
        self.root.title("OpenViBE GDF file Fixer")
        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=1)
        self.root.rowconfigure(2, weight=1)
        intro = tk.Label(self.root,
                         text="This tools is designed to fix GDF files that were written with OpenViBE from version 3.0.0 to 3.3.0.\n\n "
                              "Files are first checked for corruption and then fixed it if needed.",
                         wraplength=self.window_width * 0.8)
        intro.grid(row=0, columnspan=2, padx=(20, 20), pady=(20, 20))

        file_select_btn = tk.Button(self.root, text="Select file(s) to check", command=self.select_files)
        file_select_btn.grid(row=1, column=0, pady=(0, 20))
        dir_select_btn = tk.Button(self.root, text="Select directory to check", command=self.select_directory)
        dir_select_btn.grid(row=1, column=1, pady=(0, 20))

        self.feedback_box = tk.Text(self.root, height=5, spacing1=6)
        self.feedback_box.grid(row=2, columnspan=2, sticky=tk.NSEW)
        self.scrollbar = tk.Scrollbar(self.root, orient=tk.VERTICAL)
        self.scrollbar.grid(row=2, column=3, sticky=tk.NSEW)
        self.feedback_box.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.feedback_box.yview)

        self.feedback_box.tag_configure('file_name', font=('Arial', 14, 'italic'))
        self.feedback_box.tag_configure('fixed', foreground='green', font=('Arial', 12, 'bold'))
        self.feedback_box.tag_configure('not_corrupted', foreground='blue', font=('Arial', 12, 'bold'))

        self.gdf_fixer = GDFFixer()

    def check_file(self, file_name):
        self.feedback_box.config(state=tk.NORMAL)
        self.feedback_box.insert(tk.END, " -- {} :".format(os.path.split(file_name)[1]), 'file_name')
        if self.gdf_fixer.process_file(file_name):
            self.feedback_box.insert(tk.END, " Fixed\n".format(os.path.split(file_name)[1]), 'fixed')
        else:
            self.feedback_box.insert(tk.END, " Not corrupted\n".format(os.path.split(file_name)[1]), 'not_corrupted')

        self.feedback_box.config(state=tk.DISABLED)

    def select_directory(self):
        selected_dir = tk.filedialog.askdirectory()
        if selected_dir is not None:
            gdf_files = os.listdir(selected_dir)
            for f in gdf_files:
                if f.endswith(".gdf"):
                    self.check_file(os.path.join(selected_dir, f))

    def select_files(self):
        selected_files = tk.filedialog.askopenfilenames(filetypes=(("GDF Files", "*.gdf"), ("all files", "*.*")))
        for f in selected_files:
            self.check_file(f)

    def run(self):
        self.root.mainloop()