import signal
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QTextEdit, QMessageBox
from PyQt6.QtCore import Qt, QTimer, QObject, QThread, pyqtSignal
from PyQt6.QtGui import QIcon
import sys
import os
import datetime

from cli import CookieTester

# Step 1: Create a worker class
class Worker(QObject):
    finished = pyqtSignal()
    progress = pyqtSignal(int)
    
    def __init__(self, folder_path, appendText):
        super().__init__(None)
        self.folder_path = folder_path
        self.appendText = appendText

    def run(self):
        CookieTester.run(self.folder_path, "https://netflix.com", self.appendText)

class CookieCheckerApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowIcon(QIcon('nf.png'))
        self.setWindowTitle('NF Cookies Checker')
        self.setGeometry(500, 200, 600, 450)

        layout = QVBoxLayout()

        self.text_edit = QTextEdit()
        self.text_edit.setReadOnly(True)  # Make the text edit box uneditable
        layout.addWidget(self.text_edit)

        self.pick_button = QPushButton('Pick Folder', self)
        self.pick_button.clicked.connect(self.pickFolder)
        layout.addWidget(self.pick_button)

        self.start_button = QPushButton('Start', self)
        self.start_button.clicked.connect(self.startTesting)
        layout.addWidget(self.start_button)

        self.setLayout(layout)

        self.folder_path = None

    def pickFolder(self):
        selected_folder = QFileDialog.getExistingDirectory(self, "Select Folder", self.folder_path)
        if selected_folder:
            self.folder_path = selected_folder
            self.text_edit.clear()
            self.text_edit.append(f"Selected Folder: {self.folder_path}\n")

    def startTesting(self):
        
        if self.folder_path:
            # Set logging file details
            log_dir = os.path.join(self.folder_path, "gui_nf_checker_logs")
            if not os.path.exists(log_dir):
                os.makedirs(log_dir)
            log_file = os.path.join(log_dir, f"nf_checker_log_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.txt")
            
            self.start_button.setEnabled(False)  # Disable start button during testing
            
            # Step 2: Create a QThread object
            self.thread = QThread()
            # Step 3: Create a worker object
            self.worker = Worker(self.folder_path,self.appendText)
            # Step 4: Move worker to the thread
            self.worker.moveToThread(self.thread)
            # Step 5: Connect signals and slots
            self.thread.started.connect(self.worker.run)
            self.worker.finished.connect(self.thread.quit)
            self.worker.finished.connect(self.worker.deleteLater)
            self.thread.finished.connect(self.thread.deleteLater)
            # Step 6: Start the thread
            self.thread.start()
            
            def end():
                # Enable start button after testing
                self.longRunningBtn.setEnabled(True)
                # Log the contains of text box
                open(log_file,"w").write(self.text_edit.toPlainText())
                
                QMessageBox.information(self,"Success","Testing done successfully")
            self.thread.finished.connect(end)
            

            QMessageBox.information(self, "Testing in progress", "Please wait. Script is testing all cookie file. I am noob coder + lazy so skipped adding Thread. Program will be freezy 😁🦥🦥🦥")
        else:
            QMessageBox.warning(self, "Error", "Please select a folder before starting testing.")

    def appendText(self, text):
        self.text_edit.append(text+"\n")

def sigint_handler(*args):
    """Handler for the SIGINT signal."""
    QApplication.quit()
        
def main():
    signal.signal(signal.SIGINT, sigint_handler)
    
    app = QApplication(sys.argv)
    
    timer = QTimer()
    timer.start(500)  # You may change this if you wish.
    timer.timeout.connect(lambda: None)  # Let the interpreter run each 500 ms.
    
    window = CookieCheckerApp()
    window.show()
    
    
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
