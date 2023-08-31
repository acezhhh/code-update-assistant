from tkinter import *
from tkinter.ttk import *
from typing import Dict
import ctypes
from tkinter import filedialog
from tkinter import messagebox
import configparser
import os
import sys
import subprocess
import configparser

# 创建 ConfigParser 对象
config = configparser.ConfigParser()
# 读取配置文件
with open('config.ini', 'r', encoding='utf-8') as file:
    config.read_file(file)
ctypes.windll.shcore.SetProcessDpiAwareness(1)
# 创建 ConfigParser 对象
directory_path = config.get('variable', 'project_root')
config = configparser.ConfigParser()
# 读取配置文件
with open('config.ini', 'r', encoding='utf-8') as file:
    config.read_file(file)
class WinGUI(Tk):
    widget_dic: Dict[str, Widget] = {}
    def __init__(self):
        super().__init__()
        self.__win()
        self.widget_dic["tk_label_javaLabel"] = self.__tk_label_javaLabel(self)
        self.widget_dic["tk_label_projectLabel"] = self.__tk_label_projectLabel(self)
        self.widget_dic["tk_label_mavenLabel"] = self.__tk_label_mavenLabel(self)
        self.widget_dic["tk_button_projectButton"] = self.__tk_button_projectButton(self)
        self.widget_dic["tk_button_javaButton"] = self.__tk_button_javaButton(self)
        self.widget_dic["tk_button_mavenButton"] = self.__tk_button_mavenButton(self)
        self.widget_dic["tk_input_projectText"] = self.__tk_input_projectText(self)
        self.widget_dic["tk_input_javaText"] = self.__tk_input_javaText(self)
        self.widget_dic["tk_input_mavenText"] = self.__tk_input_mavenText(self)
        self.widget_dic["tk_button_nextButton"] = self.__tk_button_nextButton(self)
    def __win(self):
        self.title("代码更新助手")
        # 设置窗口大小、居中
        width = 600
        height = 300
        screenwidth = self.winfo_screenwidth()
        screenheight = self.winfo_screenheight()
        geometry = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        self.geometry(geometry)
        self.resizable(width=False, height=False)
        # 自动隐藏滚动条
    def scrollbar_autohide(self,bar,widget):
        self.__scrollbar_hide(bar,widget)
        widget.bind("<Enter>", lambda e: self.__scrollbar_show(bar,widget))
        bar.bind("<Enter>", lambda e: self.__scrollbar_show(bar,widget))
        widget.bind("<Leave>", lambda e: self.__scrollbar_hide(bar,widget))
        bar.bind("<Leave>", lambda e: self.__scrollbar_hide(bar,widget))

    def __scrollbar_show(self,bar,widget):
        bar.lift(widget)
    def __scrollbar_hide(self,bar,widget):
        bar.lower(widget)

    def vbar(self,ele, x, y, w, h, parent):
        sw = 15 # Scrollbar 宽度
        x = x + w - sw
        vbar = Scrollbar(parent)
        ele.configure(yscrollcommand=vbar.set)
        vbar.config(command=ele.yview)
        vbar.place(x=x, y=y, width=sw, height=h)
        self.scrollbar_autohide(vbar,ele)
    def __tk_label_javaLabel(self,parent):
        label = Label(parent,text="   JAVA_HOME:",anchor="center", )
        label.place(x=40, y=95, width=160, height=60)
        return label
    def __tk_label_projectLabel(self,parent):
        label = Label(parent,text="PROJECT_ROOT:",anchor="center", )
        label.place(x=35, y=55, width=160, height=60)
        return label
    def __tk_label_mavenLabel(self,parent):
        label = Label(parent,text="MAVEN_SETTING:",anchor="center", )
        label.place(x=28, y=135, width=160, height=60)
        return label
    def __tk_button_projectButton(self,parent):
        btn = Button(parent, text="选择", takefocus=False,)
        btn.place(x=470, y=70, width=59, height=30)
        return btn
    def __tk_button_javaButton(self,parent):
        btn = Button(parent, text="选择", takefocus=False,)
        btn.place(x=470, y=110, width=59, height=30)
        return btn
    def __tk_button_mavenButton(self,parent):
        btn = Button(parent, text="选择", takefocus=False,)
        btn.place(x=470, y=150, width=59, height=30)
        return btn
    def __tk_button_nextButton(self,parent):
        btn = Button(parent, text="下一步", takefocus=False,)
        btn.place(x=250, y=220, width=80, height=40)
        return btn
    def __tk_input_projectText(self,parent):
        ipt = Entry(parent, )
        ipt.place(x=190, y=70, width=280, height=30)
        return ipt
    def __tk_input_javaText(self,parent):
        ipt = Entry(parent, )
        ipt.place(x=190, y=110, width=280, height=30)
        return ipt
    def __tk_input_mavenText(self,parent):
        ipt = Entry(parent, )
        ipt.place(x=190, y=150, width=280, height=30)
        return ipt
class Win(WinGUI):
    def __init__(self):
        super().__init__()
        self.__event_bind()
        # 读取配置文件回显
        JAVA_HOME = config.get('variable', 'JAVA_HOME')
        if JAVA_HOME != "":
            self.widget_dic["tk_input_javaText"].insert(END, JAVA_HOME)
        PROJECT_ROOT = config.get('variable', 'PROJECT_ROOT')
        if PROJECT_ROOT != "":
            self.widget_dic["tk_input_projectText"].insert(END, PROJECT_ROOT)
        MAVEN_SETTING = config.get('variable', 'MAVEN_SETTING')
        if MAVEN_SETTING != "":
            self.widget_dic["tk_input_mavenText"].insert(END, MAVEN_SETTING)

    def fn_project(self, evt):
        text = self.widget_dic["tk_input_projectText"]
        folder_path = filedialog.askdirectory()
        if folder_path == "":
            return
        text.delete(0, END)  # 清空文本框内容
        text.insert(END, folder_path)  # 将文件夹路径插入文本框

    def fn_java(self, evt):
        text = self.widget_dic["tk_input_javaText"]
        folder_path = filedialog.askdirectory()
        if folder_path == "":
            return
        text.delete(0, END)  # 清空文本框内容
        text.insert(END, folder_path)  # 将文件夹路径插入文本框
    def fn_maven(self, evt):
        text = self.widget_dic["tk_input_mavenText"]
        folder_path = filedialog.askopenfilename()
        if folder_path == "":
            return
        text.delete(0, END)  # 清空文本框内容
        text.insert(END, folder_path)  # 将文件夹路径插入文本框
        print("Selected file:", folder_path)

    # 下一步按钮
    # 将配置设置到配置文件中
    def fn_next(self, evt):
        if not self.valid_param():
            return

        java_text = self.widget_dic["tk_input_javaText"].get()
        maven_text = self.widget_dic["tk_input_mavenText"].get()
        project_text = self.widget_dic["tk_input_projectText"].get()

        config.set('variable', 'JAVA_HOME', java_text)
        config.set('variable', 'PROJECT_ROOT', project_text)
        config.set('variable', 'MAVEN_SETTING', maven_text)
        # 保存修改后的配置文件
        with open('config.ini', 'w', encoding='utf-8') as configfile:
            config.write(configfile)
        self.open_another_file()

    # 校验参数
    def valid_param(self):
        java_text = self.widget_dic["tk_input_javaText"].get()
        maven_text = self.widget_dic["tk_input_mavenText"].get()
        project_text = self.widget_dic["tk_input_projectText"].get()
        if java_text == "":
            messagebox.showinfo("提示", "JAVA_HOME不能为空!")
            return False
        if maven_text == "":
            messagebox.showinfo("提示", "MAVEN_SETTING不能为空!")
            return False
        if project_text == "":
            messagebox.showinfo("提示", "PROJECT_ROOT不能为空!")
            return False
        if self.valid_path(java_text):
            messagebox.showinfo("提示", "JAVA_HOME路径无效!")
            return False
        if self.is_file_exists(maven_text):
            messagebox.showinfo("提示", "MAVEN_SETTING路径无效!")
            return False
        if self.valid_path(project_text):
            messagebox.showinfo("提示", "PROJECT_ROOT路径无效!")
            return False
        return True

    # 校验路径是否存在
    def valid_path(self, path):
        return not os.path.exists(path)
    # 校验文件是否存在
    def is_file_exists(self, file_path):
        return not os.path.isfile(file_path)

    def open_another_file(self):
        relative_path = "generator.py"

        # 获取特殊路径
        if getattr(sys, 'frozen', False):
            # 在打包后的可执行文件中运行
            base_path = os.path.abspath(sys.executable)
            # creationflags = subprocess.CREATE_NO_WINDOW
            # subprocess.Popen(['code-update-assistant', relative_path])
            # 在当前命名空间中执行另一个 Python 文件
            # 使用 compile() 函数编译代码

            # 关闭当前文件
            # sys.exit()
        else:
            # 在源代码中运行
            base_path = os.path.abspath(__file__)
            # python_exe = sys.executable
            # 构建新的命令来打开另一个文件
            # cmd = f"{python_exe} {target_file}"
            # 设置创建子进程的标志位，不显示控制台窗口
            # print(cmd)
            # subprocess.Popen(cmd)

            # 使用 compile() 函数编译代码
        # current_dir = os.path.dirname(base_path)
        # target_file = os.path.join(current_dir, relative_path)
        # with open(target_file, encoding='utf-8') as file:
        #     code = compile(file.read(), target_file, 'exec')
        # # 执行编译后的代码
        # exec(code)

        # python_exe = sys.executable
        # # 构建新的命令来打开另一个文件
        # cmd = f"{python_exe} {target_file}"
        # # 设置创建子进程的标志位，不显示控制台窗口
        # print(cmd)
        # subprocess.Popen(cmd)
        # subprocess.Popen(['code-update-assistant', relative_path])
        # sys.exit()

        current_dir = os.path.dirname(base_path)
        target_file = os.path.join(current_dir, relative_path)
        # python_exe = sys.executable
        # 构建新的命令来打开另一个文件
        # cmd = f"{python_exe} {target_file}"
        # try:
        #     print("cmd:" + cmd)
        #     subprocess.Popen(['code-update-assistant', target_file])
        #     sys.exit()
        # except FileNotFoundError:
        #     with open(target_file, encoding='utf-8') as file:
        #         code = compile(file.read(), target_file, 'exec')
        #     # 执行编译后的代码
        #     exec(code)
        with open(target_file, encoding='utf-8') as file:
            code = compile(file.read(), target_file, 'exec')
        # 执行编译后的代码
        exec(code)

    def __event_bind(self):
        self.widget_dic["tk_button_projectButton"].bind('<Button-1>',self.fn_project)
        self.widget_dic["tk_button_javaButton"].bind('<Button-1>',self.fn_java)
        self.widget_dic["tk_button_mavenButton"].bind('<Button-1>',self.fn_maven)
        self.widget_dic["tk_button_nextButton"].bind('<Button-1>', self.fn_next)
        pass
if __name__ == "__main__":
    win = Win()
    win.mainloop()