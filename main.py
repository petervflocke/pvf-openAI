from time import sleep
import logging
import openai
from PyQt5.QtCore import QThread, pyqtSignal, QEvent, Qt
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QSizePolicy, QPushButton, QSizeGrip, QMainWindow, QTextEdit

#from text_ui import Ui_MainWindow
from assistent import Ui_MainWindow

MODEL = "gpt-3.5-turbo"
MODEL = "gpt-4"

# openAI SYSTEM
SYSTEM = """
Your name is Peter, you are helpful assistent
"""

class openAIBackgroundTask(QThread):
    progress = pyqtSignal(str)
    finished = pyqtSignal()

    def __init__(self, openai_arg, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.openai_arg = openai_arg

    def run(self):
        for chunk in openai.ChatCompletion.create(
            **self.openai_arg
        ):
            if self.isInterruptionRequested():
                break
            content = chunk["choices"][0].get("delta", {}).get("content")
            if content is not None:
                self.progress.emit(content)
        self.progress.emit("\n")
        self.finished.emit()



class MainWindow(QMainWindow):    
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        #check if the MainWinow class works ;)
        self.ui.prompt.setText("Ask me anything")
        self.ui.text_user.setPlaceholderText('Your prompt goes here:')
        
        #remove windows titel and frame to imitate modern UIX
        self.setWindowFlag(Qt.FramelessWindowHint)

        # add resize grip to the right down windows corner
        layout = QVBoxLayout()
        sizegrip = QSizeGrip(self.ui.corner)
        layout.addWidget(sizegrip, 0, Qt.AlignBottom | Qt.AlignRight)

        #connect button(s) to method(s)
        self.ui.button_abort.clicked.connect(self.submit_abort)

        # self.close_button = QPushButton('Close', self)
        # self.close_button.clicked.connect(self.close_application)
        # layout.addWidget(self.close_button)

        # add enter and ctr+enter handler for text_user field
        self.ui.text_user.installEventFilter(self)

    # handle titelless window movement
    def mouseMoveEvent(self, event):
        newPos = event.globalPos() - self.offset
        self.move(newPos)

    def mousePressEvent(self, event):
        self.offset = event.pos()

    # add fake window decoretor to close window?
    def close_application(self):
        self.close()

    # handler for incoming stream from openAI add at the end of the current text
    def update_text_message(self, message):
        cursor = self.ui.text_message.textCursor()
        cursor.insertText(message)

    # stream from openAI has been finished reanable input field
    def done_text_message(self):
        self.ui.text_user.clear()
        self.ui.text_user.setEnabled(True)
        self.ui.text_user.setFocus()

    # handler for "enter" key (submit request) and ctr+enter add new line in the input field
    def eventFilter(self, obj, event):
        if event.type() == QEvent.KeyPress and obj is self.ui.text_user:
            if event.key() == Qt.Key_Return and self.ui.text_user.hasFocus():
                if QApplication.keyboardModifiers() == Qt.ControlModifier:
                    cursor = self.ui.text_user.textCursor()
                    cursor.insertText("\n")
                else:
                    # enter pressed detected submit request to openAI
                    self.submit_action() 
        return super().eventFilter(obj, event)

    # handling the openAI parameters before request submit and disable input to avoid paralel request
    def submit_action(self):
        self.ui.text_user.setEnabled(False)
        openai_arg = {
            'model': MODEL,
            'messages': [
                {"role": "system", "content": SYSTEM},
                {"role": "assistant", "content": self.ui.text_message.toPlainText()},
                {"role": "user", "content": self.ui.text_user.toPlainText()},
            ],
            # 'temperature': ,
            # 'max_tokens': ,
            # 'top_p': ,
            # 'frequency_penalty': ,
            # 'presence_penalty': ,
            'stream': True,
        }

        self.ui.text_message.append(self.ui.text_user.toPlainText() + "\n\n")

        self.background_task = openAIBackgroundTask(openai_arg)
        self.background_task.progress.connect(self.update_text_message)
        self.background_task.finished.connect(self.done_text_message)
        self.background_task.start()

    # handler for aborting runing worker with for incoming message from openAI
    def submit_abort(self):
        self.background_task.requestInterruption()
        self.ui.text_user.clear()
        self.ui.text_user.setEnabled(True)
        self.ui.text_user.setFocus()

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

