from tkinter import filedialog

class FileHandler:
    def __init__(self):
        self.selected_files = []

    def select_files(self):
        #选择日志文件
        files = filedialog.askopenfilenames(
            title="选择我的世界日志文件",
            filetypes=[("日志文件", "*.log *.txt"), ("所有文件", "*.*")]
        )
        if files:
            self.selected_files = list(files)
            return f"已选择 {len(self.selected_files)} 个文件"
        return "未选择任何文件"

    def clear_files(self):
        #清空已选文件
        self.selected_files = []
        return "未选择任何文件"

    def read_file(self, file_path):
        #读取文件内容
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()