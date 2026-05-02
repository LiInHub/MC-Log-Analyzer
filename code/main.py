import tkinter as tk
from tkinter import ttk, messagebox
import os
import threading

from config import LOG_MAX_LENGTH, MODEL_NAME, CONFIG_PATH
from api_manager import APIManager
from file_handler import FileHandler
from api_client import APIClient
from ui_components import UIComponents

class MCLogAnalyzer:
    def __init__(self, root):
        self.root = root
        UIComponents.setup_main_window(root)

        self.api_manager = APIManager()
        self.file_handler = FileHandler()
        self.api_client = None

        self.init_ui()

    def init_ui(self):
        # ===== 原有API框架代码 =====
        api_frame, self.api_var, self.api_combobox, self.api_input = UIComponents.create_api_frame(
            self.root, self.on_api_select
        )
        self.update_api_combobox()

        ttk.Button(api_frame, text="保存API", command=self.save_api_key).place(x=450, y=10, width=95)
        ttk.Button(api_frame, text="删除选中API", command=self.delete_api_key).place(x=550, y=10, width=95)

        for widget in api_frame.winfo_children():
            if widget.cget("text") == "清空输入框":
                widget.config(command=lambda: self.api_input.delete(0, tk.END))
                break

        # ===== 原有文件框架代码 =====
        file_frame, self.file_label = UIComponents.create_file_frame(self.root)
        ttk.Button(file_frame, text="选择日志文件", command=self.select_files).place(x=10, y=45, width=120)
        ttk.Button(file_frame, text="清空已选文件", command=self.clear_files).place(x=140, y=45, width=120)

        # ===== 分析按钮 =====
        self.analyze_btn = ttk.Button(self.root, text="开始分析日志", command=self.show_analyze_settings)
        self.analyze_btn.place(x=270, y=255, width=150, height=40)

        # ===== 新增：右下角【设置】按钮 =====
        self.settings_btn = ttk.Button(self.root, text="设置", command=self.open_settings_window)
        self.settings_btn.place(x=620, y=265, width=45, height=30)

    def on_api_select(self, event):
        api_key = self.api_var.get()
        self.api_input.delete(0, tk.END)
        self.api_input.insert(0, api_key)
        if api_key:
            self.api_client = APIClient(api_key)

    def update_api_combobox(self):
        self.api_combobox["values"] = self.api_manager.api_keys
        if self.api_manager.api_keys:
            self.api_combobox.current(0)
            self.api_client = APIClient(self.api_manager.api_keys[0])

    def save_api_key(self):
        if self.api_manager.add_api_key(self.api_input.get()):
            self.update_api_combobox()
            messagebox.showinfo("成功", "API密钥保存成功！")

    def delete_api_key(self):
        if self.api_manager.remove_api_key(self.api_var.get()):
            self.update_api_combobox()
            self.api_input.delete(0, tk.END)
            messagebox.showinfo("成功", "API密钥删除成功！")

    def select_files(self):
        msg = self.file_handler.select_files()
        self.file_label.config(text=msg)

    def clear_files(self):
        msg = self.file_handler.clear_files()
        self.file_label.config(text=msg)

    def show_analyze_settings(self):
        current_api = self.api_var.get()
        files = self.file_handler.selected_files

        if not current_api:
            messagebox.showwarning("错误", "请先选择API密钥！")
            return
        if not files:
            messagebox.showwarning("错误", "请先选择日志文件！")
            return

        # 获取主窗口的坐标
        root_x = self.root.winfo_x()
        root_y = self.root.winfo_y()
        
        set_win = tk.Toplevel(self.root)
        set_win.title("分析设置")
        # 设置窗口位置与主窗口相同，尺寸保持450x240
        set_win.geometry(f"450x240+{root_x}+{root_y}")
        set_win.resizable(False, False)
        set_win.transient(self.root)
        set_win.grab_set()

        enable_think = tk.BooleanVar(value=False)
        clean_md = tk.BooleanVar(value=True)

        ttk.Label(set_win, text="请选择分析选项", font=("微软雅黑", 12, "bold")).pack(pady=15)

        ttk.Checkbutton(
            set_win,
            text="深度思考",
            variable=enable_think
        ).pack(anchor="w", padx=30, pady=5)

        ttk.Checkbutton(
            set_win,
            text="清除Markdown格式（推荐开启）",
            variable=clean_md
        ).pack(anchor="w", padx=30, pady=5)

        # ✅ 修复：变量名统一为 clean_md
        def start():
            set_win.destroy()
            self.start_analyze(enable_think.get(), clean_md.get())

        ttk.Button(set_win, text="确认并开始分析", command=start).pack(pady=20)

    # ===== 新增：打开设置窗口（和主窗口同位置，450x240）=====
    def open_settings_window(self):
        # 获取主窗口位置
        root_x = self.root.winfo_x()
        root_y = self.root.winfo_y()
        
        # 创建设置窗口
        settings_win = tk.Toplevel(self.root)
        settings_win.title("系统设置")
        settings_win.geometry(f"450x240+{root_x}+{root_y}")
        settings_win.resizable(False, False)
        settings_win.transient(self.root)
        settings_win.grab_set()

        # 窗口内容
        ttk.Label(settings_win, text="系统设置", font=("微软雅黑", 12, "bold")).pack(pady=20)
        
        # 备用占位内容，可自行扩展
        ttk.Label(settings_win, text="当前配置文件路径：").pack(pady=5)
        ttk.Label(settings_win, text=CONFIG_PATH, wraplength=400).pack(pady=5)
        
        ttk.Button(settings_win, text="关闭", command=settings_win.destroy).pack(pady=20)

    def start_analyze(self, enable_thinking, clean_markdown):
        current_api = self.api_var.get()
        files = self.file_handler.selected_files

        if not self.api_client:
            self.api_client = APIClient(current_api)

        result_win, result_text = UIComponents.create_result_window()

        def show_loading():
            result_text.config(state=tk.NORMAL)
            result_text.delete(1.0, tk.END)
            result_text.insert(tk.END, "日志分析中，请稍候...\n")
            result_text.insert(tk.END, "正在调用AI接口，请不要关闭窗口\n")
            result_text.config(state=tk.DISABLED)

        show_loading()

        def run_analyze():
            try:
                full_result = ""
                for idx, path in enumerate(files, 1):
                    try:
                        content = self.file_handler.read_file(path)[-LOG_MAX_LENGTH:]
                        name = os.path.basename(path)
                        full_result += f"===== 第{idx}个文件：{name} =====\n"

                        result, err = self.api_client.analyze_log(
                            content,
                            stream=False,
                            enable_thinking=enable_thinking
                        )

                        if err:
                            full_result += f"{err}\n\n"
                            continue

                        if clean_markdown:
                            result = UIComponents.clean_markdown(result)

                        full_result += f"{result}\n\n{'-'*80}\n\n"

                    except Exception as e:
                        full_result += f"文件读取失败：{str(e)}\n\n"

                full_result += "所有文件分析完成！"
                self.root.after(0, lambda: self.show_final_result(result_text, full_result))

            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror("错误", f"分析失败：{str(e)}"))

        threading.Thread(target=run_analyze, daemon=True).start()

    def show_final_result(self, result_text, content):
        result_text.config(state=tk.NORMAL)
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, content)
        result_text.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    app = MCLogAnalyzer(root)
    root.mainloop()