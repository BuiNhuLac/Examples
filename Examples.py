# -*-coding:utf-8-*-
import re
import base64
import Cookie
import requests
import cookielib

from PyQt4.QtCore import (QObject, pyqtSignal, QEventLoop, QTimer)
from PyQt4.Qt import QMutex

class Examples(QObject):
	updateCountInfoTable = pyqtSignal(int)
	updateInfoTable = pyqtSignal(str, int, int)
	updateCurrentFile = pyqtSignal()
	updateTotal = pyqtSignal()
	updateChanged = pyqtSignal()
	updateOk = pyqtSignal()
	updateDie = pyqtSignal()
	updateError = pyqtSignal()
	updateIP = pyqtSignal()
	ckeckNetworkReset = pyqtSignal(int)

	def __init__(self, parent=None):
		super(Examples, self).__init__(parent)
		
		# Email related variables
		self.mailhost = 'xxx.xxx.xxx.xxx'
		self.mailUser = 'xxxxxxxx'
		self.mailPass = 'xxxxxxxx'
		self.mailFolder = 'INBOX'
		self.mail = Mails(self.mailhost)
		self.mail.Login(self.mailUser, self.mailPass)
		self.mail.selectFolder(self.mailFolder)

		# File-related variables
		self.files = ['/home/quan/import/a.txt', '/home/quan/import/b.txt', '/home/quan/import/c.txt', ...]
		self.fileCount = 3
		self.fileName = 'a.txt'
		self.file = AccessFile(self.files[0])
		self.fileLen = None
		self.start = None
		self.end = None
		self.tokens = []

		# variables related to stream processing
		self.threadFinish = []
		self.threadCame = []
		self.threadsStopped = []
		self.threadsPaused = []

		# Used to loop through files and lines in the file
		self.f = 0
		self.i = 1
		self.loop = 0
		self.loopCount = 0

		# variables specify the status of the application
		self.stop = False
		self.pause = False


		# states when interacting with files
		self.isInitializing = True
		self.isInitialized = False
		self.fileInitializationError = False
		self.fileSummation = False

		# Network-related data
		self.networkJump = 24
		self.isResetNetwork = False
		self.sleepWhileResetNetwork = [5000, 5000]
		self.ip = ''

		# store active state data to display the interface
		self.total = 0
		self.changed = 0
		self.ok = 0
		self.checkpoint = 0
		self.die = 0
		self.error = 0

		self.mutex  = QMutex()
		# self.ckeckNetworkReset.connect(self.ckeckAndResetNetwork)

	# Function Below