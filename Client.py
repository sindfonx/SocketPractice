import tkinter as tk                       # 視窗圖形化標準模組
from tkinter import scrolledtext as tkSt   # 視窗圖形化標準模組 (帶有滾動條的視窗)
from tkinter import messagebox as tkMs     # 視窗圖形化標準模組 (提示對話視窗)
import requests                            # 連線標準模組
import time
import threading


class WindowCreator:
    def __init__(self, clientName, master):
        self.isDestroy = False
        self.isActive = True
        self.PrevInfoIndex = 0

        # 建立 tkinter 物件
        self.root = tk.Toplevel(master)
        uesName = clientName
        self.root.title(uesName)     # 建立 視窗title Name
        self.root.protocol("WM_DELETE_WINDOW", self.CloseWindows)

        # 顯示聊天窗口
        self.textEdit = tkSt.ScrolledText(
            self.root, width=40, height=20)  # 建立 聊天室顯示窗口
        # 設定 聊天室顯示窗口內縮 (好看而已)
        self.textEdit.grid(pady=5, padx=5)
        # 設定 客戶端輸入顯示的顏色為藍
        self.textEdit.tag_config('guest', foreground='blue')
        # 設定 客戶端輸入顯示的顏色為藍
        self.textEdit.tag_config('server', foreground='red')
        # 執行 停止聊天室編輯的功能
        self.textEdit.config(state='disabled')

        # 編輯窗口
        self.inputText = tkSt.ScrolledText(
            self.root, width=40, height=3)  # 建立 聊天室輸入窗口
        # 設定 聊天室輸入窗口 (好看而已)
        self.inputText.grid(pady=5, padx=5)

        # 發送按鈕
        btnSend = tk.Button(self.root, text='發送', width=5, height=2,
                            command=self.selfTextSend)  # 建立 發送按鈕
        # 設定 按鈕位置
        btnSend.grid(row=2, column=0)

        print("-----歡迎來到聊天室-----")
        self.name = uesName
        print('-----------------%s------------------' % self.name)

        self.td = threading.Thread(target=self.pollingGetInfo)
        self.td.start()

        recvRowData = requests.get(
            'http://127.0.0.1:5000/GetCommunication', json={"Index": 0})
        jsonData = recvRowData.json()
        self.printOnDialog(jsonData)

    def CloseWindows(self):
        self.isActive = False

        self.td.join(0.1)
        self.isDestroy = True
        self.root.destroy()

    def selfTextSend(self):
        _selfStr = self.inputText.get('1.0', 'end-1c')    # 獲取 input 的內容。
        self.inputText.delete(1.0, 'end')                 # 刪除 input 的內容。

        if _selfStr != "":
            self.passingTime = 0
            receivedProtocolRowData = requests.post(
                'http://127.0.0.1:5000/AddCommunication', json={'Add': _selfStr})
            decodeJsonData = receivedProtocolRowData.json()
            self.printOnDialog(decodeJsonData)
            return
        else:
            tkMs.showerror('警告', "不能發送空白訊息！")

    def pollingGetInfo(self):
        while True:
            time.sleep(2.0)
            receivedProtocolRowData = requests.get(
                'http://127.0.0.1:5000/GetCommunication', json={'Index': self.PrevInfoIndex})
            decodeJsonData = receivedProtocolRowData.json()
            self.printOnDialog(decodeJsonData)

    def printOnDialog(self, recvProtocol):
        if self.isActive:
            recvIndex = recvProtocol['Index']
            recvContent = recvProtocol['Content']
            if recvIndex > self.PrevInfoIndex:
                addContent = []
                for i in range(len(recvContent)):
                    reverseIndex = len(recvContent) - i - 1
                    addContent.append(recvContent[reverseIndex])
                    if recvIndex - i - 1 == self.PrevInfoIndex:
                        break
                self.PrevInfoIndex = recvIndex
                addContent.reverse()

                self.textEdit.config(state='normal')             # 開啟聊天室編輯的功能

                for i in range(len(addContent)):
                    self.textEdit.insert(
                        tk.END, addContent[i] + '\n', 'server')   # 顯示輸入值，並換行。
                # 設定 滾動條拉 移至最新消息。
                self.textEdit.see('end')

                self.textEdit.config(state='disabled')           # 停止聊天室編輯的功能


def CreateWindow(master):
    windowName = f'聊天室{round(time.time(), 2)}'
    WindowCreator(windowName, master)


mainWindow = tk.Tk()
mainWindow.title('創建大廳')
mainWindow.geometry('0x0')

currentWindowNumber = 1
WindowCreator('聊天室1', mainWindow)
WindowCreator('聊天室22', mainWindow)
WindowCreator('聊天室333', mainWindow)
WindowCreator('聊天室4444', mainWindow)
WindowCreator('聊天室55555', mainWindow)

tk.mainloop()
