from bs4 import BeautifulSoup
from urllib.request import urlopen

import urllib.error

from PyQt4 import QtGui


class BadURLException(Exception):
    pass

class NaverWidget(QtGui.QWidget):
    
    def __init__(self, parent):
        super(NaverWidget, self).__init__(parent)
        self._urlBox = None
        self._textBox = None
        self._parent = parent
        self._parent.statusBar().showMessage("Welcome!")
        self.initUI()
        
    def initUI(self):

        urlLabel = QtGui.QLabel('URL')
        goBtn = QtGui.QPushButton('Go', self)
        titleLabel = QtGui.QLabel('Title')
        textLabel = QtGui.QLabel('Text')
        
        goBtn.clicked.connect(self.buttonClicked)
        
        self._urlBox = QtGui.QLineEdit()
        self._titleBox = QtGui.QLineEdit()
        self._textBox = QtGui.QTextEdit()
        
        
        grid = QtGui.QGridLayout()
        grid.setSpacing(10)

        grid.addWidget(urlLabel, 1, 0)
        grid.addWidget(self._urlBox, 1, 1)
        grid.addWidget(goBtn, 1, 2)

        grid.addWidget(titleLabel, 2, 0)
        grid.addWidget(self._titleBox, 2, 1, 1, 2)
        
        grid.addWidget(textLabel, 3, 0)
        grid.addWidget(self._textBox, 3, 1, 5, 2)
        
        self.setLayout(grid)

        
        
    def connectToNaver(self, url):
        self._parent.statusBar().showMessage("Loading URL...")
        try:
            page=urlopen(url)
        except ValueError:
            raise BadURLException("Bad URL")
        except urllib.error.HTTPError:
            raise BadURLException("Bad URL")
        except urllib.error.URLError:
            raise BadURLException("Bad URL")
        soup = BeautifulSoup(page.read())
        self._parent.statusBar().showMessage("Done!")
        
        result = {}
        divTitle = soup.find_all('meta', attrs={'property':'og:title'})
        for titles in divTitle:
            result['title'] = titles['content']
        divText = soup.find_all('div', attrs={'class':'detail_view_content ft15'})
        if len(divText) == 0:
            raise BadURLException("Bad URL")
        for e in divText:
            spans = soup.find_all('span')
            for span in spans:
                span.decompose()
            result['text'] = e.get_text("\n")
        return result
            
    
    def buttonClicked(self):
        try:
            url = self._urlBox.text()
            result = self.connectToNaver(url)
            title = result['title']
            self._titleBox.setText(title)
            text = result['text']
            self._textBox.setText(text)
        except BadURLException:
            msgBox = QtGui.QMessageBox()
            msgBox.setWindowTitle("Error!")
            msgBox.setText("Invalid URL")
            msgBox.exec_()
        
class MainWindow(QtGui.QMainWindow):
    
    def __init__(self):
        super(MainWindow, self).__init__()
        self.form_widget = NaverWidget(self) 
        self.setCentralWidget(self.form_widget)
        self.initUI()
        
    def initUI(self):
        self.statusBar()
        menubar = self.menuBar()
        aboutAction = QtGui.QAction('About', self)
        aboutAction.setStatusTip('About')
        aboutAction.triggered.connect(self.showAbout)
        
        exitAction = QtGui.QAction('Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(self.close)
        
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(aboutAction)
        fileMenu.addAction(exitAction)
        self.setGeometry(300, 300, 550, 600)
        self.setWindowTitle('Naver Story Getter')
        self.show()
    
    def showAbout(self):
        msgBox = QtGui.QMessageBox()
        msgBox.setWindowTitle("About")
        msgBox.setText("Copy a naver story URl into the field and press the button.\nCreated by Luke Li on July 23, 2013")
        msgBox.exec_()

def main():
    
    app = QtGui.QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

