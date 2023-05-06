from time import sleep
import logging
import openai
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QSizePolicy, QPushButton, QSizeGrip, QMainWindow
from PyQt5.QtCore import Qt

#from text_ui import Ui_MainWindow
from assistent import Ui_MainWindow

MODEL = "gpt-3.5-turbo"
MODEL = "gpt-4"

# openAI SYSTEM
SYSTEM = """
You are Peter, a helpful assistent
"""

class openAIBackgroundTask(QThread):
    progress = pyqtSignal(str)

    def __init__(self, openai_arg, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.openai_arg = openai_arg

    def run(self):
        for chunk in openai.ChatCompletion.create(
            **self.openai_arg
        ):
            content = chunk["choices"][0].get("delta", {}).get("content")
            if content is not None:
                self.progress.emit(content)
        self.progress.emit("\n")


class MainWindow(QMainWindow):    
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        #check if the MainWinow class works ;)
        self.ui.prompt.setText("Ask me anything")
        self.ui.test_user.setPlaceholderText('Your prompt goes here:')
        
        #remove windows titel and frame to imitate modern UIX
        self.setWindowFlag(Qt.FramelessWindowHint)

        # add resize grip to the right down windows corner
        layout = QVBoxLayout()
        sizegrip = QSizeGrip(self.ui.corner)
        layout.addWidget(sizegrip, 0, Qt.AlignBottom | Qt.AlignRight)

        #connect button(s) to method(s)
        self.ui.button_submit.clicked.connect(self.submit_action)

        # self.close_button = QPushButton('Close', self)
        # self.close_button.clicked.connect(self.close_application)
        # layout.addWidget(self.close_button)

    def mousePressEvent(self, event):
        self.offset = event.pos()

    def mouseMoveEvent(self, event):
        newPos = event.globalPos() - self.offset
        self.move(newPos)

    # add fake window decoretor to close window?
    def close_application(self):
        self.close()

    def update_text_message(self, message):
        cursor = self.ui.text_message.textCursor()
        cursor.insertText(message)

    def submit_action(self):
        openai_arg = {
            'model': MODEL,
            'messages': [
                {"role": "system", "content": SYSTEM},
                {"role": "assistant", "content": self.ui.text_message.toPlainText()},
                {"role": "user", "content": self.ui.test_user.toPlainText()},
            ],
            # 'temperature': ,
            # 'max_tokens': ,
            # 'top_p': ,
            # 'frequency_penalty': ,
            # 'presence_penalty': ,
            'stream': True,
        }

        self.ui.text_message.append(self.ui.test_user.toPlainText() + "\n\n")

        self.background_task = openAIBackgroundTask(openai_arg)
        self.background_task.progress.connect(self.update_text_message)
        self.background_task.start()

        # create a python loop printing from 1 to 10
        self.ui.test_user.clear()


if __name__ == "__main__":
    import sys
    import os

    # DEBUG_MODE = "debug", "info", anything else for off
    DEBUG_MODE = ""
    if len(sys.argv) > 1:
        DEBUG_MODE = sys.argv[1]
    else:
        DEBUG_MODE = "off"
    if DEBUG_MODE == "debug":
        logging.basicConfig(
            level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s"
        )
    elif DEBUG_MODE == "info":
        logging.basicConfig(
            level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
        )
    else:
        logging.disable(sys.maxsize)

    # get openAI key
    OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
    if not OPENAI_API_KEY:
        raise ValueError(
            "openAI API KEY cannot be empty, setup environment variable OPENAI_API_KEY"
        )
    else:
        openai.api_key = OPENAI_API_KEY

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

