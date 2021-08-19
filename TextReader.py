#!/usr/bin/python3
from PyQt5.QtWidgets import QComboBox, QDialog, QFileDialog, QGridLayout, QLabel, QSlider, QSpinBox, QPlainTextEdit, QToolBar, QVBoxLayout, QWidget, QMainWindow, QApplication, QPushButton, QTabWidget, QLineEdit, QAction, QStatusBar, QMenu
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer, QMediaPlaylist
from PyQt5.QtGui import QCloseEvent, QIcon, QKeySequence, QResizeEvent
from PyQt5.QtCore import QUrl, Qt
from json import loads, dumps
from os import system, popen
from sys import exit, argv
from gtts import gTTS
currUsr=popen("echo $HOME").read().strip()
try: 
    settingsFile=open(f"{currUsr}/.config/TextReader/settings.json","r",encoding="UTF-8")
    settings=loads(settingsFile.read())
    settingsFile.close()
except:
    settings={"theme": 0, "fontSize": "16", "fontFamily": "Courier", "width": 1280, "height": 720, "lang":"English", "speechLang":"Turkish", "volume":66}
try:
    languageFile=open(f"/usr/share/TextReader/languages.json","r",encoding="UTF-8")
    lang=loads(languageFile.read())
    languageFile.close()
    fallBack=False
except:
    lang={"English":{
        "__comment__"  :"'&' Symbol defines 'Alt+[]' shortcut keys.",
        "shortCode"     :"en",
        "fileMenu"      :"&File",
        "editMenu"      :"&Edit",
        "viewMenu"      :"&View",
        "toolMenu"      :"&Tools",
        "fileOpen"      :"&Open",
        "fileNew"       :"&New",
        "fileSave"      :"&Save",
        "fileSaveAs"    :"Save &As",
        "fileClose"     :"&Close",
        "fileQuit"      :"&Quit",
        "editReload"    :"Rel&oad",
        "editSelectAll" :"Select &All",
        "editCut"       :"Cu&t",
        "editCopy"      :"&Copy",
        "editPaste"     :"&Paste",
        "editUndo"      :"&Undo",
        "editRedo"      :"&Redo",
        "viewAppearance":"&Appearance",
        "toolSpeech"    :"Text to &Speech",
        "toolPause"     :"Pause",
        "toolPlay"      :"Play",
        "toolRewind"    :"Rewind",
        "toolBackward"  :"Backward",
        "toolForward"   :"Forward",
        "toolToggleMute":"Toggle mute.",
        "toolVolUp"     :"Increase volume.",
        "toolVolDown"   :"Descrease volume.",
        "untitled"      :"Untitled",
        "char"          :"char",
        "word"          :"word",
        "line"          :"line",
        "pluralSuffix"  :"s",
        "criticalTitle" :"Warning",
        "warningTitle"  :"Attention",
        "DoYouQuit"     :"You have unsaved changes. Do you really want to quit?",
        "buttonYes"     :"Yes",
        "buttonNo"      :"No",
        "buttonDiscard" :"Discard",
        "buttonCancel"  :"Cancel",
        "buttonSave"    :"Save",
        "tipOpen"       :"Open a new text document in a new tab.",
        "tipNew"        :"Create a new text document in a new tab.",
        "tipSave"       :"Save content to file.",
        "tipSaveAs"     :"Save content to another file.",
        "tipClose"      :"Close currently active tab.",
        "tipQuit"       :"Exit the application.",
        "tipReload"     :"Import the saved file content to the editor.",
        "tipSelectAll"  :"Select all content.",
        "tipCut"        :"Cut selected text.",
        "tipCopy"       :"Copy selected text.",
        "tipPaste"      :"Paste the text from the clipboard to where cursor is.",
        "tipUndo"       :"Undo the last change.",
        "tipRedo"       :"Redo the last change.",
        "tipAppearance" :"Open appearance editor.",
        "tipSpeech"     :"Export the current content into mp3 file.",
        "tipShowToolBar":"Show/hide toolbar.",
        "tipSaveMp3"    :"Save the rendered sound file.",
        "tipRewind"      :"Rewind and replay.",
        "tipBackward"   :"Backward one second.",
        "tipPlay"       :"Resume/play audio file.",
        "tipPause"      :"Pause audio file.",
        "tipForward"    :"Forward one second.",
        "tipSoundOff"   :"Decrease volume.",
        "tipSoundOn"    :"Increase volume.",
        "tipMute"       :"Toggle mute.",
        "titleSaveFile" :"Save File",
        "titleOpenFile" :"Open File",
        "fileType"      :"Text Document",
        "DoYouReload"   :"Reloading may cause your changes to be lost. Do you still want to reload?",
        "ttlAppearance" :"Appearance",
        "themeList"        :["Default",
                             "Dark",
                             "Silver",
                             "Light",
                             "Matrix",
                             "Pink",
                             "High Contrast"],
        "fontFamily"    :"Font Family",
        "fontSize"      :"Font Size",
        "themes"        :"Themes",
        "appLanguage"   :"App Language",
        "speechLanguage":"Speech Language",
        "restartRequire":"Restart required.",
        "buttonOk"      :"Okay",
        "unsavedChanges":"You Have Unsaved Changes!",
        "placeHolder"   :"Start typing...",
        ".txtUnsaved"   :".txt has not saved. Do you want to save it?",
        "showToolBar"   :"Show tool bar",
        "cantReload"    :"Cannot reload an unsaved file!",
        "cantSpeech"    :"Please provide a text to speech.",
        "saveMp3"       :"Save rendered sound file."
    }}
    settings["lang"]="English"
    settings["speechLang"]="English"
    fallBack=True
language=lang[settings["lang"]]
soundButtons=["toolPause","toolBackward","toolForward","toolRewind","toolPlay","soundPos"]
shortCodes=[]
for i in lang:
    shortCodes.append(lang[i]["shortCode"])
styles=["",
        "background:#222;color:#eee;selection-background-color:#c88;",
        "background:#666;color:#eee;selection-background-color:#44c;",
        "background:#eee;color:#111;selection-background-color:#66f;",
        "background:#111;color:#4a4;selection-background-color:#4a4;selection-color:#111;",
        "background:#d99;color:#000;selection-background-color:#c79;}",
        "background:#000;color:#fff;selection-background-color:#fff;selection-color:#000;border:1px solid #fff;"
        ]
def updateStatus():
    content=main.tabs.currentWidget().code.toPlainText()
    length=len(content)
    words=len(content.split())
    lines=len(content.split("\n"))
    main.lenWorld.setText(f"{length} "+language["char"]+(language["pluralSuffix"] if length>1 else "")+f" | {words} "+language["word"]+(language["pluralSuffix"] if words>1 else "")+f" | {lines} "+language["line"]+(language["pluralSuffix"] if lines>1 else ""))
def toggleActions():
    widget=main.tabs.currentWidget()
    lastSaved=widget.lastSaved
    main.fileSave.setDisabled(lastSaved)
    main.fileSaveAs.setDisabled(lastSaved)
    for i in soundButtons: exec(f"main.{i}.setDisabled({widget.sound==None});")
class MainWin(QMainWindow):
    def __init__(self,):
        super(MainWin,self).__init__()
        self.fileName=language["untitled"]
        self.tabs=QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(lambda:self.closeTab())
        self.newTab()
        self.tabs.currentChanged.connect(lambda:[self.updateTitle(),updateStatus(),toggleActions(),main.player.setPlaylist(main.tabs.currentWidget().playList)])
        self.setCentralWidget(self.tabs)
        self.resize(settings["width"],settings["height"])
        self.menus=self.menuBar()
        self.fileMenu=QMenu(language["fileMenu"])
        self.editMenu=QMenu(language["editMenu"])
        self.viewMenu=QMenu(language["viewMenu"])
        self.toolMenu=QMenu(language["toolMenu"])
        self.fileOpen=QAction(QIcon(f"/usr/share/TextReader/assets/menuIcons/open.png"),language["fileOpen"],self)
        self.fileNew=QAction(QIcon(f"/usr/share/TextReader/assets/menuIcons/new.png"),language["fileNew"],self)
        self.fileSave=QAction(QIcon(f"/usr/share/TextReader/assets/menuIcons/save.png"),language["fileSave"],self)
        self.fileSaveAs=QAction(QIcon(f"/usr/share/TextReader/assets/menuIcons/saveas.png"),language["fileSaveAs"],self)
        self.fileClose=QAction(QIcon(f"/usr/share/TextReader/assets/menuIcons/close.png"),language["fileClose"],self)
        self.fileQuit=QAction(QIcon(f"/usr/share/TextReader/assets/menuIcons/quit.png"),language["fileQuit"],self)
        self.fileOpen.setShortcut(QKeySequence("Ctrl+O"))
        self.fileNew.setShortcut(QKeySequence("Ctrl+N"))
        self.fileSave.setShortcut(QKeySequence("Ctrl+S"))
        self.fileSaveAs.setShortcut(QKeySequence("Ctrl+Shift+S"))
        self.fileClose.setShortcut(QKeySequence("Ctrl+W"))
        self.fileQuit.setShortcut(QKeySequence("Alt+F4"))
        self.fileOpen.setStatusTip(language["tipOpen"])
        self.fileNew.setStatusTip(language["tipNew"])
        self.fileSave.setStatusTip(language["tipSave"])
        self.fileSaveAs.setStatusTip(language["tipSaveAs"])
        self.fileClose.setStatusTip(language["tipClose"])
        self.fileQuit.setStatusTip(language["tipQuit"])
        self.fileOpen.triggered.connect(lambda:self.openFile())
        self.fileNew.triggered.connect(lambda:self.newTab())
        self.fileClose.triggered.connect(lambda:self.closeTab())
        self.fileSave.triggered.connect(lambda:self.tabs.currentWidget().saveChanges())
        self.fileSaveAs.triggered.connect(lambda:self.tabs.currentWidget().saveChanges(saveAs=True))
        self.fileQuit.triggered.connect(lambda:self.closeEvent(QCloseEvent()))
        self.fileMenu.addActions([self.fileOpen,self.fileNew,self.fileSave,self.fileSaveAs,self.fileClose])
        self.fileMenu.addSeparator()
        self.fileMenu.addActions([self.fileQuit])
        self.editReload=QAction(QIcon(f"/usr/share/TextReader/assets/menuIcons/reload.png"),language["editReload"],self)
        self.editSelectAll=QAction(QIcon(f"/usr/share/TextReader/assets/menuIcons/selectall.png"),language["editSelectAll"],self)
        self.editCut=QAction(QIcon(f"/usr/share/TextReader/assets/menuIcons/cut.png"),language["editCut"],self)
        self.editCopy=QAction(QIcon(f"/usr/share/TextReader/assets/menuIcons/copy.png"),language["editCopy"],self)
        self.editPaste=QAction(QIcon(f"/usr/share/TextReader/assets/menuIcons/paste.png"),language["editPaste"],self)
        self.editUndo=QAction(QIcon(f"/usr/share/TextReader/assets/menuIcons/undo.png"),language["editUndo"],self)
        self.editRedo=QAction(QIcon(f"/usr/share/TextReader/assets/menuIcons/redo.png"),language["editRedo"],self)
        self.editReload.setStatusTip(language["tipReload"])
        self.editSelectAll.setStatusTip(language["tipSelectAll"])
        self.editCut.setStatusTip(language["tipCut"])
        self.editCopy.setStatusTip(language["tipCopy"])
        self.editPaste.setStatusTip(language["tipPaste"])
        self.editUndo.setStatusTip(language["tipUndo"])
        self.editRedo.setStatusTip(language["tipRedo"])
        self.editReload.triggered.connect(lambda:self.tabs.currentWidget().reload())
        self.editSelectAll.triggered.connect(lambda:self.tabs.currentWidget().selectAll())
        self.editCut.triggered.connect(lambda:self.tabs.currentWidget().cut())
        self.editCopy.triggered.connect(lambda:self.tabs.currentWidget().copy())
        self.editPaste.triggered.connect(lambda:self.tabs.currentWidget().paste())
        self.editUndo.triggered.connect(lambda:self.tabs.currentWidget().undo())
        self.editRedo.triggered.connect(lambda:self.tabs.currentWidget().redo())
        self.editReload.setShortcut(QKeySequence("F5"))
        self.editSelectAll.setShortcut(QKeySequence("Ctrl+A"))
        self.editCut.setShortcut(QKeySequence("Ctrl+X"))
        self.editCopy.setShortcut(QKeySequence("Ctrl+C"))
        self.editPaste.setShortcut(QKeySequence("Ctrl+V"))
        self.editUndo.setShortcut(QKeySequence("Ctrl+Z"))
        self.editRedo.setShortcut(QKeySequence("Ctrl+Y"))
        self.editMenu.addActions([self.editReload])
        self.editMenu.addSeparator()
        self.editMenu.addActions([self.editUndo,self.editRedo])
        self.editMenu.addSeparator()
        self.editMenu.addActions([self.editSelectAll])
        self.editMenu.addSeparator()
        self.editMenu.addActions([self.editCut,self.editCopy,self.editPaste])
        self.viewConfig=QAction(QIcon(f"/usr/share/TextReader/assets/menuIcons/config.png"),language["viewAppearance"],self)
        self.viewToolBar=QAction(language["showToolBar"],self)
        self.viewToolBar.setCheckable(True)
        self.viewToolBar.setChecked(True)
        self.viewConfig.triggered.connect(sett.show)
        self.viewConfig.setStatusTip(language["tipAppearance"])
        self.viewToolBar.setStatusTip(language["tipShowToolBar"])
        self.viewToolBar.setShortcut(QKeySequence("F1"))
        self.viewConfig.setShortcut(QKeySequence("F2"))
        self.viewMenu.addActions([self.viewConfig,self.viewToolBar])
        self.toolSpeech=QAction(QIcon(f"/usr/share/TextReader/assets/menuIcons/text2speech.png"),language["toolSpeech"],self)
        self.toolSaveMp3=QAction(QIcon(f"/usr/share/TextReader/assets/menuIcons/vinyl.png"),language["saveMp3"],self)
        self.toolSaveMp3.triggered.connect(lambda:main.tabs.currentWidget().saveMp3())
        self.toolSpeech.triggered.connect(lambda:[self.textSpeech(),self.player.play()])
        self.toolSpeech.setShortcut(QKeySequence("Alt+*"))
        self.toolMenu.addActions([self.toolSpeech,self.toolSaveMp3])
        self.menus.addMenu(self.fileMenu)
        self.menus.addMenu(self.editMenu)
        self.menus.addMenu(self.viewMenu)
        self.menus.addMenu(self.toolMenu)
        self.toolBar=QToolBar(self)
        self.toolBar.setContextMenuPolicy(Qt.PreventContextMenu)
        self.toolBar.setMovable(False)
        self.toolBar.addActions([self.fileOpen,self.fileNew,self.fileClose])
        self.toolBar.addSeparator()
        self.toolBar.addActions([self.fileSave,self.fileSaveAs])
        self.toolBar.addSeparator()
        self.toolBar.addActions([self.editUndo,self.editRedo])
        self.toolBar.addSeparator()
        self.toolBar.addActions([self.editReload])
        self.toolBar.addSeparator()
        self.toolBar.addActions([self.editSelectAll,self.editCut,self.editCopy,self.editPaste])
        self.soundPos=QSlider(1,self)
        self.volumePos=QSlider(1,self)
        self.volumePos.setMaximumWidth(150)
        self.soundPos.setMinimum(1)
        self.volumePos.valueChanged.connect(lambda:self.player.setVolume(self.volumePos.value()))
        self.player=QMediaPlayer(self)
        self.player.positionChanged.connect(self.updateSoundPos)
        self.player.stateChanged.connect(lambda:self.togglePlayPause())
        self.volumePos.setSliderPosition(self.player.volume())
        self.toolPause=QAction(QIcon(f"/usr/share/TextReader/assets/menuIcons/pause.png"),language["toolPause"],self)
        self.toolPlay=QAction(QIcon(f"/usr/share/TextReader/assets/menuIcons/play.png"),language["toolPlay"],self)
        self.toolRewind=QAction(QIcon(f"/usr/share/TextReader/assets/menuIcons/rewind.png"),language["toolRewind"],self)
        self.toolBackward=QAction(QIcon(f"/usr/share/TextReader/assets/menuIcons/backward.png"),language["toolBackward"],self)
        self.toolForward=QAction(QIcon(f"/usr/share/TextReader/assets/menuIcons/forward.png"),language["toolForward"],self)
        self.toolMute=QAction(QIcon(f"/usr/share/TextReader/assets/menuIcons/volumeMax.png"),"Mute",self)
        self.toolRewind.setShortcut(QKeySequence("Alt+Backspace"))
        self.toolPlay.setShortcut(QKeySequence("Alt+/"))
        self.toolPause.setShortcut(QKeySequence("Alt+P"))
        self.toolMute.setShortcut(QKeySequence("Alt+0"))
        self.toolBackward.setShortcut(QKeySequence("Alt+Left"))
        self.toolForward.setShortcut(QKeySequence("Alt+Right"))
        self.toolMute.triggered.connect(lambda:self.player.setMuted(not self.player.isMuted()))
        self.toolPause.setVisible(False)
        self.toolPause.triggered.connect(lambda:self.player.pause())
        self.toolPlay.triggered.connect(lambda:self.playSound())
        self.toolRewind.triggered.connect(lambda:[self.player.setPosition(0),self.player.play()])
        self.toolBackward.triggered.connect(lambda:self.player.setPosition(self.player.position()-1000))
        self.toolForward.triggered.connect(lambda:self.player.setPosition(self.player.position()+1000))
        self.toolPause.setDisabled(True)
        self.toolBackward.setDisabled(True)
        self.toolForward.setDisabled(True)
        self.toolRewind.setDisabled(True)
        self.toolPlay.setDisabled(True)
        self.soundPos.setDisabled(True)
        self.player.volumeChanged.connect(lambda:[self.volumePos.setSliderPosition(self.player.volume()),self.updateHoparlor(),self.changeStyle(sett.cbThemes.currentIndex())])
        self.player.mutedChanged.connect(lambda:self.updateHoparlor())
        self.player.setVolume(settings["volume"])
        self.toolVolDown=QAction(QIcon(f"/usr/share/TextReader/assets/menuIcons/volumeDown.png"),"Descrease Volume",self)
        self.toolVolDown.triggered.connect(lambda:self.player.setVolume(self.player.volume()-10))
        self.toolVolDown.setShortcut(QKeySequence("Alt+Down"))
        self.toolVolUp=QAction(QIcon(f"/usr/share/TextReader/assets/menuIcons/volumeUp.png"),"Increase Volume",self)
        self.toolVolUp.triggered.connect(lambda:self.player.setVolume(self.player.volume()+10))
        self.toolVolUp.setShortcut(QKeySequence("Alt+Up"))
        self.toolBar.addSeparator()
        self.toolBar.addActions([self.toolSpeech,self.toolSaveMp3])
        self.toolBar.addSeparator()
        self.toolBar.addActions([self.toolRewind,self.toolBackward,self.toolPause,self.toolPlay,self.toolForward])
        self.toolBar.addWidget(self.soundPos)
        self.toolBar.addActions([self.toolMute,self.toolVolDown])
        self.toolBar.addWidget(self.volumePos)
        self.toolBar.addActions([self.toolVolUp])
        self.toolSpeech.setStatusTip(language["tipSpeech"])
        self.toolSaveMp3.setStatusTip(language["tipSaveMp3"])
        self.toolBackward.setStatusTip(language["tipBackward"])
        self.toolForward.setStatusTip(language["tipForward"])
        self.toolRewind.setStatusTip(language["tipRewind"])
        self.toolPlay.setStatusTip(language["tipPlay"])
        self.toolPause.setStatusTip(language["tipPause"])
        self.toolVolDown.setStatusTip(language["tipSoundOff"])
        self.toolVolUp.setStatusTip(language["tipSoundOn"])
        self.toolMute.setStatusTip(language["tipMute"])
        self.toolPause.setStatusTip(language["tipPause"])
        self.addToolBar(self.toolBar)
        sett.cbThemes.currentIndexChanged.connect(lambda:main.changeStyle(sett.cbThemes.currentIndex()))
        self.soundPos.sliderMoved.connect(lambda:self.player.setPosition(self.soundPos.value()))
        self.viewToolBar.changed.connect(lambda:self.toolBar.setHidden(not self.viewToolBar.isChecked()))
        self.status=QStatusBar(self)
        self.setStatusBar(self.status)
        self.lenWorld=QLabel(f"0 "+language["char"]+" | 0 "+language["word"]+" | 1 "+language["line"])
        self.lenWorldIndicator=self.status.addPermanentWidget(self.lenWorld)
        if fallBack:
            self.status.addWidget(QLabel("FALLBACK MODE | PLEASE CHECK THE LANGUAGE PACK FILE."),1)
        self.show()
        self.changeStyle(settings["theme"]%len(styles))
    def updateHoparlor(self):
        if self.player.volume()==0 or self.player.isMuted(): self.toolMute.setIcon(QIcon(f"/usr/share/TextReader/assets/menuIcons/volumeMute.png"))
        elif self.player.volume()<33: self.toolMute.setIcon(QIcon(f"/usr/share/TextReader/assets/menuIcons/volumeMin.png"))
        elif self.player.volume()<66: self.toolMute.setIcon(QIcon(f"/usr/share/TextReader/assets/menuIcons/volumeMid.png"))
        else: self.toolMute.setIcon(QIcon(f"/usr/share/TextReader/assets/menuIcons/volumeMax.png"))
    def textSpeech(self):
        main.changeStyle(sett.cbThemes.currentIndex())
        widget=self.tabs.currentWidget()
        widget.sound=widget.code.toPlainText()
        if len(widget.sound)>0:
            mp3=gTTS(widget.sound,lang=shortCodes[sett.speechLanguage.currentIndex()])
            mp3File=f"{currUsr}/.cache/TextReader/{widget}.mp3".replace("<__main__.CodeEditor object at ","").replace(">","")
            mp3.save(mp3File)
            self.player.setPlaylist(widget.playList)
            widget.mp3File=mp3File
            widget.playList.removeMedia(0)
            widget.playList.addMedia(QMediaContent(QUrl.fromLocalFile(mp3File)))
            for i in soundButtons: exec(f"main.{i}.setDisabled({widget.sound==None});")
        else: self.status.showMessage(language["cantSpeech"],3000)
    def togglePlayPause(self):
        if self.player.state()==QMediaPlayer.PlayingState:
            self.toolPlay.setVisible(False)
            self.toolPause.setVisible(True)
        else:
            self.toolPlay.setVisible(True)
            self.toolPause.setVisible(False)
    def playSound(self):
        if self.player.state()==QMediaPlayer.StoppedState:
            self.player.setPosition(0)
        self.player.play()
    def pauseSound(self):
        self.player.pause()
    def updateSoundPos(self):
        self.soundPos.setMaximum(self.player.duration())
        self.soundPos.setSingleStep(500)
        self.soundPos.setSliderPosition(self.player.position())
    def closeEvent(self,event):
        main.changeStyle(sett.cbThemes.currentIndex())
        sett.close()
        states=[]
        for tab in range(self.tabs.count()):
            states.append(self.tabs.widget(tab).lastSaved)
        if all(states):
            return super().closeEvent(event)
        else:
            if self.tabs.count()==1:
                if self.tabs.tabText(0)==language["untitled"]+"*":
                    if not self.tabs.widget(0).saved:
                        if self.tabs.widget(0).code.toPlainText()=="":
                            system(f"rm -rf $HOME/.cache/TextReader")
                            return app.quit()
        Quit.show()
        return event.ignore()
    def resizeEvent(self, a0:QResizeEvent):
        settings["width"]=self.width()
        settings["height"]=self.height()
        open(f"{currUsr}/.config/TextReader/settings.json","w",encoding="UTF-8").write(dumps(settings))
        return super().resizeEvent(a0)
    def newTab(self,fileName=None):
        self.fileName=fileName
        if self.fileName==None:
                self.tabs.setCurrentIndex(self.tabs.addTab(CodeEditor(language["untitled"]),language["untitled"]))
        else:
            editor=CodeEditor(self.fileName)
            self.tabs.setCurrentIndex(self.tabs.addTab(editor,self.fileName))
        self.updateTitle()
    def closeTab(self):
        if not self.tabs.currentWidget().lastSaved:
            if self.tabs.count()==1:
                if self.tabs.tabText(0)==language["untitled"]:
                    if not self.tabs.widget(0).saved:
                        if self.tabs.widget(0).code.toPlainText()!="": save.show()
                    else: save.show()
                else: save.show()
            else: save.show()
            if self.tabs.count()==1:
                save.lastTab=True
            else: 
                save.lastTab=False
        else:
            if self.tabs.count()==1:
                self.newTab()
                system(f"rm {self.tabs.widget(0).mp3File}")
                self.tabs.removeTab(0)
            else:
                system(f"rm {self.tabs.currentWidget().mp3File}")
                self.tabs.removeTab(self.tabs.currentIndex())
    def changeStyle(self,style:int):
        app.setStyleSheet("QStatusBar {border-top:1px solid #a9a9a9} QTabWidget::pane {margin:-12px;} QSlider::handle {background-color:#38a1e3;border:1px solid #5a646a;} QPlainTextEdit {font-family:'"+sett.fontFamily.text().replace("'","")+"', monospace;font-size:"+str(sett.fontSize.text())+"pt;} * {"+styles[style]+"} ")
        settings["theme"]=style
        settings["fontFamily"]=sett.fontFamily.text()
        settings["fontSize"]=sett.fontSize.text()
        settings["lang"]=sett.language.currentText()
        settings["speechLang"]=sett.speechLanguage.currentText()
        settings["volume"]=self.player.volume()
        open(f"{currUsr}/.config/TextReader/settings.json","w",encoding="UTF-8").write(dumps(settings))
    def updateTitle(self):
        self.setWindowTitle(f"{self.tabs.currentWidget().fileName} - TextReader")
    def openFile(self,url=None):
        if url==None:
            file=QFileDialog().getOpenFileName(self,language["titleOpenFile"],"./",language["fileType"]+" (*.txt)")[0]        
        else:
            file=url
        if file!="":
            if file.split("/")[-1][:-4]!="":
                self.newTab(file.split("/")[-1][:-4])
                self.tabs.currentWidget().code.setPlainText(open(file,"r",encoding="UTF-8").read())
                self.tabs.currentWidget().saved=True
                self.tabs.currentWidget().filePath=file
            self.tabs.currentWidget().saveChanges()
            if self.tabs.count()==2:
                if self.tabs.tabText(0)==language["untitled"]:
                    if not self.tabs.widget(0).saved:
                        if self.tabs.widget(0).code.toPlainText()=="":
                            system(f"rm $HOME/.cache/TextReader/{self.tabs.widget(0).mp3File}")
                            self.tabs.removeTab(0)
                            
class CodeEditor(QWidget):
    def __init__(self,fileName=None):
        super(CodeEditor,self).__init__()
        self.fileName=fileName
        self.code=QPlainTextEdit(self)
        self.code.textChanged.connect(lambda:[self.unsavedStar(),updateStatus(),toggleActions()])
        self.code.setPlaceholderText(language["placeHolder"])
        self.layout=QVBoxLayout(self)
        self.layout.addWidget(self.code)
        self.filePath="./"+language["untitled"]+".txt"
        self.saved=False
        self.lastSaved=False
        self.content=""
        self.sound=None
        self.mp3File=None
        self.playList=QMediaPlaylist(self)
    def saveChanges(self,saveAs:bool=False):
        if saveAs or (not self.saved):
            self.filePath=QFileDialog.getSaveFileName(self,language["titleSaveFile"],self.code.toPlainText().split("\n")[0][:20],language["fileType"]+" (*.txt)")[0]
            if self.filePath.split("/")[-1]!="":
                lastSlash=self.filePath.split("/")[-1]
                self.fileName=lastSlash if lastSlash[-4:]!=".txt" else lastSlash[:-4]
                self.saved=True
                self.lastSaved=True
        if self.saved:
            file=open(self.filePath+".txt" if self.filePath[-4:]!=".txt" else self.filePath,"w",encoding="UTF-8")
            file.write(self.code.toPlainText())
            file.close()
            self.content=self.code.toPlainText()
            main.updateTitle()
        self.unsavedStar()
    def unsavedStar(self):
        if self.content!=self.code.toPlainText():
            main.tabs.setTabText(main.tabs.currentIndex(),self.fileName+"*")
            self.lastSaved=False
        else:
            main.tabs.setTabText(main.tabs.currentIndex(),self.fileName)
            self.lastSaved=True
    def selectAll(self):
        self.code.selectAll()
    def copy(self):
        self.code.copy()
    def paste(self):
        self.code.paste()
    def cut(self):
        self.code.cut()
    def undo(self):
        self.code.undo()
    def redo(self):
        self.code.redo()
    def reload(self):
        if main.tabs.currentWidget().saved:
            if not main.tabs.currentWidget().lastSaved:
              rlod.show()
        else: main.status.showMessage(language["cantReload"],3000)
    def updateStyle():
        main.changeStyle(sett.cbThemes.currentIndex())
    def saveMp3(self):
        if self.sound!=None:
            file=QFileDialog.getSaveFileName(self,"Save Mp3 File",filter="MP3 File Format (*.mp3)")
            if file[0]!="":
                path=file[0] if file[0][:-4]==".mp3" else file[0]+".mp3"
                system(f"cp {self.mp3File} {path}")
class Settings(QDialog):
    def __init__(self):
        super(Settings,self).__init__()
        self.setWindowModality(True)
        self.setWindowTitle(language["ttlAppearance"]+" - TextReader")
        self.setFixedSize(360,240)
        self.layout=QGridLayout(self)
        self.layout.addWidget(QLabel(language["themes"]),0,0)
        self.cbThemes=QComboBox(self)
        themes=language["themeList"]
        for i in themes:
            self.cbThemes.addItem(i)
        self.cbThemes.setCurrentIndex(settings["theme"])
        self.layout.addWidget(self.cbThemes,0,1)
        self.layout.addWidget(QLabel(language["fontFamily"]),1,0)
        self.fontFamily=QLineEdit(settings["fontFamily"],self)
        self.fontFamily.textChanged.connect(lambda:CodeEditor.updateStyle())
        self.layout.addWidget(self.fontFamily,1,1)
        self.fontSize=QSpinBox(self)
        self.fontSize.setValue(int(settings["fontSize"]))
        self.fontSize.setMinimum(8)
        self.fontSize.setMaximum(64)
        self.fontSize.textChanged.connect(lambda:CodeEditor.updateStyle())
        self.layout.addWidget(QLabel(language["fontSize"]),2,0)
        self.layout.addWidget(self.fontSize,2,1)
        self.layout.addWidget(QLabel(language["appLanguage"]+"*"),3,0)
        self.language=QComboBox(self)
        self.language.addItems(lang.keys())
        self.language.setCurrentText(settings["lang"])
        self.language.currentTextChanged.connect(lambda:CodeEditor.updateStyle())
        self.layout.addWidget(self.language,3,1)
        self.layout.addWidget(QLabel(language["speechLanguage"]),4,0)
        self.speechLanguage=QComboBox(self)
        self.speechLanguage.addItems(lang.keys())
        self.speechLanguage.setCurrentIndex(list(lang).index(settings["speechLang"]))
        self.speechLanguage.currentTextChanged.connect(lambda:CodeEditor.updateStyle())
        self.layout.addWidget(self.speechLanguage,4,1)
        self.layout.addWidget(QLabel("* "+language["restartRequire"]),5,0,1,2)
        self.bOkay=QPushButton(language["buttonOk"])
        self.bOkay.clicked.connect(lambda:[CodeEditor.updateStyle(),self.close()])
        self.layout.addWidget(self.bOkay,6,1)
class SaveExit(QDialog):
    def __init__(self):
        super(SaveExit,self).__init__()
        self.setWindowTitle(language["unsavedChanges"])
        self.setFixedSize(240,135)
        self.setWindowModality(Qt.ApplicationModal)
        self.layout=QGridLayout(self)
        fileName=main.tabs.tabText(main.tabs.currentIndex())
        self.lMessage=QLabel(fileName+language[".txtUnsaved"])
        self.lMessage.setWordWrap(True)
        self.bSave=QPushButton(language["buttonSave"])
        self.bDiscard=QPushButton(language["buttonDiscard"])
        self.bCancel=QPushButton(language["buttonCancel"])
        self.bCancel.clicked.connect(self.close)
        self.bDiscard.clicked.connect(lambda:[self.discard(),self.bCancel.setFocus()])
        self.bSave.clicked.connect(lambda:[self.save(),self.bCancel.setFocus()])
        self.layout.addWidget(self.lMessage,0,0,1,3)
        self.layout.addWidget(self.bCancel,1,0)
        self.layout.addWidget(self.bDiscard,1,1)
        self.layout.addWidget(self.bSave,1,2)
        self.lastTab=False
    def save(self):
        main.tabs.currentWidget().saveChanges()
        if main.tabs.currentWidget().saved:
            self.close()
    def discard(self):
        if self.lastTab:
            main.newTab(language["untitled"])
            system(f"rm {main.tabs.widget(0).mp3File}")
            main.tabs.removeTab(0)
        else: main.tabs.removeTab(main.tabs.currentIndex())
        self.close()
class ReallyQuit(QDialog):
    def __init__(self):
        super(ReallyQuit,self).__init__()
        self.setWindowTitle(language["criticalTitle"])
        self.setFixedSize(240,135)
        self.setWindowModality(Qt.ApplicationModal)
        self.layout=QGridLayout(self)
        self.lMessage=QLabel(language["DoYouQuit"])
        self.lMessage.setWordWrap(True)
        self.layout.addWidget(self.lMessage,0,0,1,2)
        self.bYes=QPushButton(QIcon(f"/usr/share/TextReader/assets/menuIcons/redYes.png"),language["buttonYes"])
        self.bYes.clicked.connect(lambda:[system(f"rm -rf $HOME/.cache/TextReader"),app.quit()])
        self.bNo=QPushButton(QIcon(f"/usr/share/TextReader/assets/menuIcons/greenNo.png"),language["buttonNo"])
        self.bNo.clicked.connect(self.close)
        self.layout.addWidget(self.bNo,1,1)
        self.layout.addWidget(self.bYes,1,0)
class ReallyReload(QDialog):
    def __init__(self):
        super(ReallyReload,self).__init__()
        self.setWindowTitle(language["warningTitle"])
        self.setFixedSize(240,135)
        self.setWindowModality(Qt.ApplicationModal)
        self.layout=QGridLayout(self)
        self.lMessage=QLabel(language["DoYouReload"])
        self.lMessage.setWordWrap(True)
        self.layout.addWidget(self.lMessage,0,0,1,2)
        self.bYes=QPushButton(QIcon(f"/usr/share/TextReader/assets/menuIcons/redYes.png"),language["buttonYes"])
        self.bYes.clicked.connect(lambda:self.yes())
        self.bNo=QPushButton(QIcon(f"/usr/share/TextReader/assets/menuIcons/greenNo.png"),language["buttonNo"])
        self.bNo.clicked.connect(self.close)
        self.layout.addWidget(self.bNo,1,1)
        self.layout.addWidget(self.bYes,1,0)
    def yes(self):
        file=open(main.tabs.currentWidget().filePath+".txt" if main.tabs.currentWidget().filePath[-4:]!=".txt" else main.tabs.currentWidget().filePath,"r",encoding="UTF-8")
        content=file.read()
        file.close()
        self.bNo.setFocus()
        main.tabs.currentWidget().code.setPlainText(content)
        self.close()
system(f"mkdir $HOME/.cache/TextReader")
system(f"mkdir $HOME/.config/TextReader/")
app=QApplication(argv)
app.setStyle("Fusion")
app.setWindowIcon(QIcon(f"/usr/share/TextReader/assets/icons/textreader.png"))
sett=Settings()
main=MainWin()
for i in argv[1:]:
    if QUrl.isValid(QUrl.fromLocalFile(i)):
        if i[-4:]==".txt":
            main.openFile(url=i)
save=SaveExit()
Quit=ReallyQuit()
rlod=ReallyReload()
exit(app.exec_())