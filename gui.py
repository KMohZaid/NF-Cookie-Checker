import signal
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QTextEdit, QMessageBox
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QIcon
import sys
import os
import datetime

from cli import CookieTester

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
            log_dir = os.path.join(self.folder_path, "nf_checker_logs")
            if not os.path.exists(log_dir):
                os.makedirs(log_dir)
            log_file = os.path.join(log_dir, f"nf_checker_log_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.txt")
            
            self.start_button.setDisabled(True)  # Disable start button during testing
            
            QMessageBox.information(self, "Testing in progress", "Please wait. Script is testing all cookie file. I am noob coder + lazy so skipped adding Thread. Program will be freezy 😁🦥🦥🦥")
            CookieTester.run(self.folder_path, "https://netflix.com", self.appendText)
                        
            # Log the contains of text box
            with open(log_file,"w") as f:
              f.write(self.text_edit.toPlainText())
            
            self.start_button.setDisabled(False)  # Re-enable start button after testing
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
