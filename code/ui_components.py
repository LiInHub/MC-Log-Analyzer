import tkinter as tk
from tkinter import ttk

class UIComponents:
    @staticmethod
    def clean_markdown(text):
        #清除Markdown格式
        text = text.replace("#", "").replace("**", "").replace("*", "")
        text = text.replace("`", "").replace("```", "").replace("> ", "")
        text = text.replace("---", "").replace("- ", "")
        return text.strip()

    @staticmethod
    def setup_main_window(root):
        #设置主窗口
        root.title("我的世界 日志分析工具 - deepseek API")
        root.geometry("700x310")  
        root.resizable(False, False)

    @staticmethod
    def create_api_frame(root, callback_select):
        api_frame = ttk.LabelFrame(root, text="deepseek API 管理")
        api_frame.place(x=20, y=10, width=660, height=120)

        ttk.Label(api_frame, text="选择API密钥：").place(x=10, y=10)
        api_var = tk.StringVar()
        api_combobox = ttk.Combobox(api_frame, textvariable=api_var, state="readonly", width=45)
        api_combobox.place(x=110, y=10)
        api_combobox.bind("<<ComboboxSelected>>", callback_select)

        ttk.Label(api_frame, text="输入新API：").place(x=10, y=45)
        api_input = ttk.Entry(api_frame, width=48)
        api_input.place(x=110, y=45)

        ttk.Button(api_frame, text="清空输入框").place(x=450, y=43, width=100)
        return api_frame, api_var, api_combobox, api_input

    @staticmethod
    def create_file_frame(root):
        #文件上传区域
        file_frame = ttk.LabelFrame(root, text="日志文件上传。实例目录→ logs/latest.log 或 crash-reports")
        file_frame.place(x=20, y=140, width=660, height=100)
        file_label = ttk.Label(file_frame, text="未选择任何文件")
        file_label.place(x=10, y=10)
        return file_frame, file_label

    @staticmethod
    def create_result_window():
        #分析结果窗口
        result_win = tk.Toplevel()
        result_win.title("分析结果")
        result_win.geometry("800x620")
        result_win.resizable(False, False)

        result_text = tk.Text(result_win, wrap=tk.WORD, font=("微软雅黑", 10), state=tk.DISABLED)
        result_text.place(x=10, y=10, width=780, height=595)
        scrollbar = ttk.Scrollbar(result_text, command=result_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        result_text.config(yscrollcommand=scrollbar.set)
        return result_win, result_text