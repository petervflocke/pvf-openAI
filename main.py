import os
import logging
import json
import openai
from PyQt5.QtCore import QThread, pyqtSignal, QEvent, Qt, QTimer
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QLabel,
    QSizePolicy,
    QPushButton,
    QSizeGrip,
    QMainWindow,
    QTextEdit,
)

# from text_ui import Ui_MainWindow
from assistent import Ui_MainWindow

# local DB handling
import assistantDB

# defualt prompts and state machine for assitant status
from params import SYSTEM_PROMPTS, assistantStatus


# This class will represent your state machine
class Assistant:
    def __init__(self):
        self.state = assistantStatus.idle
        self.system = ""
        self.assistant = ""
        self.user = ""
        self.conversation = []

    def update_state(self, new_state):
        self.state = new_state

    def get_state(self):
        return self.state


MODEL = "gpt-3.5-turbo"
MODEL = "gpt-4"

DATABASE = os.path.dirname(os.path.abspath(__file__)) + "/example.db"
db_handler = assistantDB.SQLiteHandler(DATABASE)


class openAIBackgroundTask(QThread):
    progress = pyqtSignal(str)
    finished = pyqtSignal()

    def __init__(self, my_assistant, openai_arg, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.openai_arg = openai_arg
        self.my_assistant = my_assistant

    def run(self):
        self.my_assistant.assistant = ""
        try:
            if self.my_assistant.state == assistantStatus.openai_waiting:
                print("Procesing openai:", self.openai_arg)
                for chunk in openai.ChatCompletion.create(**self.openai_arg):
                    if self.isInterruptionRequested():
                        break
                    content = chunk["choices"][0].get("delta", {}).get("content")
                    if content is not None:
                        self.progress.emit(content)
                        self.my_assistant.assistant += content
                self.progress.emit("\n")
                self.finished.emit()
            elif self.my_assistant.state == assistantStatus.local_waiting:
                #print("Procesing: ", self.openai_arg)
                response = openai.ChatCompletion.create(**self.openai_arg)
                self.my_assistant.assistant = response["choices"][0]["message"]["content"]
                self.finished.emit()
        except openai.error.InvalidRequestError as e:
            print(e)
            self.progress.emit("InvalidRequestError")
            self.finished.emit()
        except openai.error.RateLimitError as e:
            print(e)
            self.progress.emit("RateLimitError")
            self.finished.emit()


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.my_assistant = Assistant()        

        # check if the MainWinow class works ;)
        self.ui.prompt.setText("Ask me anything")
        self.ui.text_user.setPlaceholderText("Your prompt goes here:")

        # remove windows titel and frame to imitate modern UIX
        self.setWindowFlag(Qt.FramelessWindowHint)

        # add resize grip to the right down windows corner
        layout = QVBoxLayout()
        sizegrip = QSizeGrip(self.ui.corner)
        layout.addWidget(sizegrip, 0, Qt.AlignBottom | Qt.AlignRight)

        # connect button(s) to method(s)
        self.ui.button_abort.clicked.connect(self.submit_abort)

        # self.close_button = QPushButton('Close', self)
        # self.close_button.clicked.connect(self.close_application)
        # layout.addWidget(self.close_button)

        # add enter and ctr+enter handler for text_user field
        self.ui.text_user.installEventFilter(self)

        # self.background_task = openAIBackgroundTask(openai_arg)
        self.background_task = openAIBackgroundTask(self.my_assistant, "")
        self.background_task.progress.connect(self.update_text_message)
        self.background_task.finished.connect(self.done_text_message)
        self.my_assistant.state == assistantStatus.idle
        self.process_state()


    # Assitant state machine
    def process_state(self):
        # Process the current state
        if self.my_assistant.state == assistantStatus.idle:
            pass
        elif self.my_assistant.state == assistantStatus.local:
            # let's check the intention
            openai_arg = {
                "model": MODEL,
                "messages": [
                    {
                        "role": "system",
                        "content": SYSTEM_PROMPTS[assistantStatus.local],
                    },
                    {"role": "user", "content": self.ui.text_user.toPlainText()},
                ],
                "stream": False,
            }
            self.update_text_message("Thinking ...\n")
            self.background_task.openai_arg = openai_arg
            self.my_assistant.state = assistantStatus.local_waiting
            self.background_task.start()
            print("background job started")
        elif self.my_assistant.state == assistantStatus.local_waiting:
            pass
        elif self.my_assistant.state == assistantStatus.local_done:
            pass
        elif self.my_assistant.state == assistantStatus.openai:
            # act with gpt
            print("In openai status")
            if self.my_assistant.system:
                message = { 
                    "role": "system",
                    "content": self.my_assistant.system
                }
                self.my_assistant.conversation.append(message)
            if self.my_assistant.assistant:
                message = {
                    "role": "assistant", 
                    "content": self.my_assistant.assistant
                }
                self.my_assistant.conversation.append(message)
            if self.my_assistant.user:
                message = {
                    "role": "user", 
                    "content": self.my_assistant.user
                }
                self.my_assistant.conversation.append(message)
            openai_arg = {
                "model": MODEL,
                "messages": self.my_assistant.conversation,
                "stream": True,
            }
            self.ui.text_message.append(self.my_assistant.user + "\n\n")
            self.my_assistant.system = ""
            self.my_assistant.user = ""            
            self.background_task.openai_arg = openai_arg
            print (json.dumps(openai_arg))
            self.my_assistant.state = assistantStatus.openai_waiting
            self.background_task.start()
        elif self.my_assistant.state == assistantStatus.openai_waiting:
            pass
        elif self.my_assistant.state == assistantStatus.openai_done:
            print(self.my_assistant.assistant)
            self.my_assistant.conversation.append(
                { 
                    "role": "assistant",
                    "content": self.my_assistant.assistant
                },
            )
            self.my_assistant.assistant = ""
            self.my_assistant.state = assistantStatus.idle
        else:
            print("Uknown status")

        QTimer.singleShot(0, self.process_state)    

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
        if self.my_assistant.state == assistantStatus.local_waiting:
            try:
                json_assistant = json.loads(self.my_assistant.assistant)
                print(type(json_assistant))
                print(json_assistant)
                self.update_text_message(f"Action: {json_assistant['action']}. ")
                if json_assistant["action"] == "#remember":
                    what = json_assistant
                    del what["action"]
                    db_handler.insert_data(db_handler.db_table_ltsm, what)
                    self.update_text_message(f"Saved: {json_assistant['original_message']}.\n")
                    self.my_assistant.system = ""
                    self.my_assistant.assistant = ""
                    self.my_assistant.user = ""
                    self.ui.text_user.clear()
                    self.ui.text_user.setEnabled(True)
                    self.ui.text_user.setFocus()
                    self.my_assistant.state = assistantStatus.idle
                elif json_assistant["action"] == "#question":
                    qs = json_assistant["entities"]
                    search_for = json.dumps(qs) if isinstance(qs, list) else qs
                    context = db_handler.fuzzy_search_entities(search_for, threshold=60)
                    context = "\n".join(context)
                    self.update_text_message(f"For question: {json_assistant['original_message']} found: \n{context}.\n")
                    #self.my_assistant.system = SYSTEM_PROMPTS[assistantStatus.openai] + "\n### Additional information:\n" + context
                    self.my_assistant.system = ""
                    self.my_assistant.assistant = ""
                    self.my_assistant.user = f"\nAdditional information:\n {context} \n {json_assistant['original_message']}"
                    self.my_assistant.state = assistantStatus.openai
                elif json_assistant["action"] == "#pass":
                    self.my_assistant.system = SYSTEM_PROMPTS[assistantStatus.openai]
                    self.my_assistant.assistant = ""
                    self.my_assistant.user = json_assistant["original_message"]
                    self.my_assistant.state = assistantStatus.openai
                    print("passing detected", )
            except ValueError as e:
                print("Invalid JSON:", e)
                print("String:", self.my_assistant.assistant)
            except KeyError as e:
                print("Invalid key:", e)

        elif self.my_assistant.state == assistantStatus.openai_waiting:
            self.my_assistant.state = assistantStatus.openai_done
            self.ui.text_user.clear()
            self.ui.text_user.setEnabled(True)
            self.ui.text_user.setFocus()
            logging.debug("Finishing thread from: %s", "done")
            ## self.background_task.deleteLater() (we rather keep the taks for later)
        else:
            pass

    # handler for aborting runing worker with for incoming message from openAI
    def submit_abort(self):
        self.background_task.requestInterruption()
        logging.debug("Finishing thread from: %s", "abort")

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
        # we always start from local state
        self.my_assistant.state = assistantStatus.local
        # disable entry field
        self.ui.text_user.setEnabled(False)

if __name__ == "__main__":
    import sys
    import os

    if sys.version_info < (3, 10):
        print("Minimu Python version 3.7")
        sys.exit(1)

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
    exit_code = app.exec_()
    db_handler.close_connection()
    sys.exit(exit_code)
