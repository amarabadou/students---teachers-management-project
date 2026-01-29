import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import os
import shutil
import subprocess
from connect import create_connection 


LOGO_FILENAME = "img/dd.png" 
WINDOW_TITLE = "Lesson Uploader"
UPLOAD_BUTTON_TEXT = "Upload PDF"
LIST_BUTTON_TEXT = "View Lessons"
UPLOADS_DIRECTORY = "Uploaded_Lessons"
DATABASE_NAME = "ingbba" 


BG_DARK = "#34495E"      
FG_LIGHT = "white"       
ACCENT_GREEN = "#E67E22" 
ACCENT_RED = "lightblue"   
FONT_TITLE = ('Helvetica', 12, 'bold')
FONT_BODY = ('Helvetica', 10)


class PDFUploaderApp:
    def __init__(self, master):
        self.master = master
        master.title(WINDOW_TITLE)
        
        
        master.config(bg=BG_DARK)

        
        try:
            global logo_img
            logo_img = tk.PhotoImage(file=LOGO_FILENAME) 
            self.logo_label = tk.Label(master, image=logo_img, bg=BG_DARK)
            self.logo_label.pack(pady=15, padx=20)
        except:
            self.logo_error_label = tk.Label(master, 
                                             text=f"Logo not found: {LOGO_FILENAME}", 
                                             fg=ACCENT_RED, 
                                             bg=BG_DARK, 
                                             font=FONT_BODY)
            self.logo_error_label.pack(pady=10)

        
        tk.Label(master, text="Lesson Title:", bg=BG_DARK, fg=FG_LIGHT, font=FONT_BODY).pack(pady=(10, 0))
        self.title_entry = tk.Entry(master, width=40, font=FONT_BODY, relief=tk.FLAT, bd=2)
        self.title_entry.pack(pady=(0, 5))
        
        
        id_frame = tk.Frame(master, bg=BG_DARK)
        id_frame.pack(pady=(5, 10))

        
        teacher_frame = tk.Frame(id_frame, bg=BG_DARK)
        teacher_frame.pack(side=tk.LEFT, padx=10)
        
        tk.Label(teacher_frame, text="Teacher ID:", bg=BG_DARK, fg=FG_LIGHT, font=FONT_BODY).pack()
        self.teacher_id_entry = tk.Entry(teacher_frame, width=8, font=FONT_BODY, relief=tk.FLAT, bd=2, justify=tk.CENTER)
        self.teacher_id_entry.pack()
        
        
        level_frame = tk.Frame(id_frame, bg=BG_DARK)
        level_frame.pack(side=tk.LEFT, padx=10)
        
        tk.Label(level_frame, text="Level ID:", bg=BG_DARK, fg=FG_LIGHT, font=FONT_BODY).pack()
        self.level_id_entry = tk.Entry(level_frame, width=8, font=FONT_BODY, relief=tk.FLAT, bd=2, justify=tk.CENTER)
        self.level_id_entry.pack()
        
        
        self.path_var = tk.StringVar()
        self.path_var.set("No file selected.")
        self.path_label = tk.Label(master, 
                                   textvariable=self.path_var, 
                                   wraplength=350, 
                                   justify=tk.CENTER,
                                   bg="#ECF0F1", 
                                   fg="#2C3E50", 
                                   relief=tk.FLAT,
                                   font=FONT_BODY,
                                   padx=10, pady=5)
        self.path_label.pack(pady=10, padx=20, fill=tk.X)
        
        
        button_frame = tk.Frame(master, bg=BG_DARK)
        button_frame.pack(pady=(15, 20), padx=20)
        
        
        self.upload_button = tk.Button(button_frame, 
                                       text=UPLOAD_BUTTON_TEXT, 
                                       command=self.upload_file,
                                       font=FONT_TITLE,
                                       bg=ACCENT_RED, 
                                       fg="black", 
                                       height=2, 
                                       width=15, 
                                       relief=tk.GROOVE)
        self.upload_button.pack(side=tk.LEFT, padx=10) 
        
        
        self.list_button = tk.Button(button_frame, 
                                     text=LIST_BUTTON_TEXT,
                                     command=self.list_and_open_lessons,
                                     font=FONT_TITLE,
                                     bg=ACCENT_GREEN, 
                                     fg=FG_LIGHT, 
                                     height=2, 
                                     width=15, 
                                     relief=tk.GROOVE)
        self.list_button.pack(side=tk.LEFT, padx=10) 
        
        
        self.status_var = tk.StringVar()
        self.status_var.set("")
        self.status_label = tk.Label(master, 
                                     textvariable=self.status_var, 
                                     fg="#F1C40F", 
                                     bg=BG_DARK,
                                     font=FONT_BODY)
        self.status_label.pack(pady=10)

    
    def upload_file(self):
        lesson_title = self.title_entry.get().strip()
        teacher_id_str = self.teacher_id_entry.get().strip()
        level_id_str = self.level_id_entry.get().strip()
        
        if not lesson_title or not teacher_id_str or not level_id_str:
            messagebox.showerror("Input Error", "Please fill in the Lesson Title, Teacher ID, and Level ID.")
            return
            
        try:
            teacher_id = int(teacher_id_str)
            level_id = int(level_id_str)
        except ValueError:
            messagebox.showerror("Input Error", "Teacher ID and Level ID must be integers.")
            return

        filepath = filedialog.askopenfilename(
            defaultextension=".pdf",
            filetypes=[("PDF Documents", "*.pdf")],
            title="Choose a PDF Lesson to Upload"
        )
        
        if not filepath:
            self.path_var.set("No file selected.")
            self.status_var.set("Selection cancelled.")
            return

        self.path_var.set(f"Selected file: {filepath}")
        self.status_var.set("Processing...")
        
        connection = None
        try:
            if not os.path.exists(UPLOADS_DIRECTORY):
                os.makedirs(UPLOADS_DIRECTORY)
            
            filename = os.path.basename(filepath)
            destination_path = os.path.join(UPLOADS_DIRECTORY, filename)
            shutil.copy(filepath, destination_path)
            
            db_file_path = os.path.join(UPLOADS_DIRECTORY, filename)
            
            connection = create_connection(DATABASE_NAME)
            if connection is None:
                raise Exception("Could not establish a database connection.")
            
            cursor = connection.cursor()
            
            insert_query = """
                INSERT INTO lessons (title, file_path, teacher_id, level_id)
                VALUES (%s, %s, %s, %s)
            """
            
            cursor.execute(insert_query, (lesson_title, db_file_path, teacher_id, level_id))
            connection.commit()
            
            self.status_var.set(f"SUCCESS: Lesson '{lesson_title}' saved and DB updated.")
            messagebox.showinfo("Upload Complete", 
                                f"Lesson '{lesson_title}' uploaded successfully! Saved to DB and folder.")
            
        except Exception as e:
            if connection:
                connection.rollback()
                
            error_msg = f"ERROR: Failed to save file or database entry. ({e})"
            self.status_var.set(error_msg)
            messagebox.showerror("Upload Error", error_msg)
            
        finally:
            if connection:
                cursor.close()
                connection.close()
    
    
    def list_and_open_lessons(self):
        self.status_var.set("Listing uploaded files...")
        
        if not os.path.exists(UPLOADS_DIRECTORY) or not os.listdir(UPLOADS_DIRECTORY):
            messagebox.showinfo("No Lessons", f"The '{UPLOADS_DIRECTORY}' folder is empty or does not exist.")
            self.status_var.set("Ready to upload.")
            return
            
        all_files = os.listdir(UPLOADS_DIRECTORY)
        pdf_files = [f for f in all_files if f.lower().endswith('.pdf')]
        
        if not pdf_files:
            messagebox.showinfo("No PDF Lessons", f"No PDF files found in the '{UPLOADS_DIRECTORY}' folder.")
            self.status_var.set("Ready to upload.")
            return
        
        self.open_selection_window(pdf_files)
        self.status_var.set("File selection complete.")

    
    def open_selection_window(self, pdf_files):
        selection_window = tk.Toplevel(self.master)
        selection_window.title("Open Uploaded Lesson")
        selection_window.geometry("400x300")
        selection_window.config(bg=BG_DARK) 

        tk.Label(selection_window, 
                 text="Select a Lesson to Open:", 
                 bg=BG_DARK, 
                 fg=FG_LIGHT, 
                 font=FONT_TITLE).pack(pady=10) 

        listbox = tk.Listbox(selection_window, width=50, height=10, font=FONT_BODY, selectbackground=ACCENT_GREEN)
        listbox.pack(padx=20, pady=5, fill=tk.BOTH, expand=True)
        
        for file in pdf_files:
            listbox.insert(tk.END, file)

        def open_selected_file():
            try:
                selected_index = listbox.curselection()
                if not selected_index:
                    messagebox.showwarning("Selection Error", "Please select a file first.")
                    return
                    
                filename = listbox.get(selected_index[0])
                full_path = os.path.join(UPLOADS_DIRECTORY, filename)

                if os.name == 'nt': 
                    os.startfile(full_path)
                elif os.uname().sysname == 'Darwin': 
                    subprocess.call(('open', full_path))
                else: 
                    subprocess.call(('xdg-open', full_path))
                    
                self.status_var.set(f"Opened file: {filename}")
                selection_window.destroy()

            except Exception as e:
                messagebox.showerror("File Error", f"Could not open file.\nError: {e}")
                self.status_var.set(f"Error opening file: {filename}")

        open_button = tk.Button(selection_window, 
                                text="Open Selected File", 
                                command=open_selected_file, 
                                bg=ACCENT_GREEN, 
                                fg=FG_LIGHT,
                                font=FONT_BODY,
                                relief=tk.FLAT)
        open_button.pack(pady=10)
        
        close_button = tk.Button(selection_window, 
                                 text="Close", 
                                 command=selection_window.destroy,
                                 bg=BG_DARK,
                                 fg=FG_LIGHT,
                                 font=FONT_BODY,
                                 relief=tk.FLAT)
        close_button.pack(pady=5)


if __name__ == '__main__':
    root = tk.Tk()
    app = PDFUploaderApp(root)
    root.mainloop()