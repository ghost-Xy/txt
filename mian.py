import tkinter as tk
from tkinter import filedialog, ttk
import os

def select_folder():
    folder_path = filedialog.askdirectory()
    folder_label.config(text="已选择的文件夹路径: " + folder_path)

def process_files():
    folder_path = folder_label.cget("text")。split(": ")[1]
    files_list = [file for file in os.listdir(folder_path) if file.endswith(".txt")]

    total_files = len(files_list)
    progress_bar['maximum'] = total_files

    for index, file in enumerate(files_list):
        file_path = os.path。join(folder_path, file)
        output_file_path = file_path + ".temp"

        try:
            with open(file_path, 'r', encoding='utf-8') as input_file, open(output_file_path, 'w', encoding='utf-8') as output_file:
                lines_seen = set()
                for line in input_file:
                    stripped_line = line.rstrip('\n')
                    if stripped_line not in lines_seen:
                        output_file.write(line)
                        lines_seen.add(stripped_line)

                os.remove(file_path)
                os.rename(output_file_path, file_path)

        except Exception as e:
            progress_label.config(text="错误: " + str(e))
            return

        progress_bar['value'] = index + 1
        progress_label.config(text="正在处理文件 {}/{}"。format(index + 1, total_files))

    result_label.config(text="处理完成！")

def update_window_size():
    root.update_idletasks()
    root.geometry("400x" + str(root.winfo_reqheight()))

root = tk.Tk()
root。title("文件夹处理工具")
root。geometry("400x200")

select_button = tk.Button(root, text="选择文件夹", command=select_folder)
select_button.pack(pady=10, padx=10, side=tk.LEFT)

folder_label = tk.Label(root, text="已选择的文件夹路径: ")
folder_label.pack(pady=5, padx=10, anchor=tk.W)

process_button = tk.Button(root, text="开始", command=process_files)
process_button.pack(pady=10, padx=10, side=tk.LEFT)

progress_bar = ttk.Progressbar(root, length=300, mode='determinate')
progress_bar.pack(pady=10, padx=10)

progress_label = tk.Label(root, text="")
progress_label.pack(pady=5, padx=10, anchor=tk.W)

result_label = tk.Label(root, text="")
result_label.pack(pady=5, padx=10, anchor=tk.W)

root。after(100, update_window_size)
root。mainloop()
