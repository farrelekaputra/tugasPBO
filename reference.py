from vendor import iconsbase64 as icons
from tkinter import *
import tkinter as tk
import pygame, threading
from PIL import ImageTk
import base64, os
import audio_metadata, time
from mutagen.mp3 import MP3
from PIL import Image as SM
from PIL import ImageFilter
from eyed3 import id3 as eye
from tkinter import messagebox
from tkinter import filedialog, ttk
import random

class WINDOW:
    def __init__(self):
        # icons, images path
        self.MAIN = "assets/icons/IconLogo.png"
        self.LOGO = "assets/icons/logo.png"
        self.PAUSE = "assets/icons/pause.png"
        self.PLAY = "assets/icons/play.png"
        self.DEC_VOL = "assets/icons/muted.png"
        self.INC_VOL = "assets/icons/notmuted.png"
        self.FORWARD = "assets/icons/next.png"
        self.BACK = "assets/icons/prev.png"
        self.MUSIC = "assets/icons/music.png"
        self.FOLDER = "assets/icons/folder.png"
        self.SHUFFLE = "assets/icons/shuffle.png"
        self.SHUFFLE_ON = "assets/icons/shuffleon.png"
        self.REPEAT = "assets/icons/repeat.png"
        self.REPEAT_ON = "assets/icons/repeaton.png"
        self.LEFT_FRAME = "assets/icons/left_bar.png"
        self.RIGHT_FRAME = "assets/icons/right_bar.png"
        self.NO_IMAGE = icons.NOImage
        
        # colors
        self.TEXT_COLOR = 'white'
        self.FRAME_COLOR_THEME = '#131313'
        self.FRAME_TEXT_COLOR_THEME = 'white'
        
        # default window geometry
        self.HEIGHT=620 
        self.WIDTH=1060
        
        # window initiation
        self.windows = tk.Tk()
        self.windows.title('Wave - Music Player')
        self.screen_width = self.windows.winfo_screenwidth()
        self.screen_height = self.windows.winfo_screenheight()
        # self.windows.bind('<space>', self.play_space)

        # window geometry set, based on user screen
        self.x = int((self.screen_width/2) - (self.WIDTH/2))
        self.y = int((self.screen_height/2) - (self.HEIGHT/2))
        self.windows.geometry("{}x{}+{}+{}".format(self.WIDTH, self.HEIGHT, self.x, self.y))
        self.windows.config(bg='#1e1e1e')
        
        self.background = Label(self.windows, borderwidth=0)
        self.background.place(x=0,y=0)

        self.root=Frame(self.windows, height=self.HEIGHT, width=self.WIDTH, bg="#131313")
        self.root.pack()
        

        
        self.windows.protocol("WM_DELETE_WINDOW", self.exit)
        
        
        
    def window(self):   
        window_type = self.windows.state()
        if window_type == 'zoomed':
            temp = self.screen_height // 100
            temp = temp * 100
            var = temp - 620
            padding = var // 2
            self.root.pack(pady=padding)
            
        elif window_type == 'normal':
            self.root.config(highlightthickness=0)
            self.root.pack(pady=0)
        self.root.after(100, self.window, )
    
    def get_icons(self, icons):
        base64_img_bytes = icons.encode('utf-8')
        decoded_image_data = base64.decodebytes(base64_img_bytes)
        ico = PhotoImage(data=decoded_image_data)
        return ico
    
    def getimages(self, images_path):
        image_obj = PhotoImage(file=images_path)
        return image_obj

    def exit(self):
        # Munculkan pesan dialog untuk validasi keluar aplikasi
        result = messagebox.askyesno(title="Exit", message="Apakah Anda yakin ingin keluar?")

        # Jika pengguna memilih "OK", keluar aplikasi
        if result:
            self.windows.destroy()
            
class MusicPlayer(WINDOW):
    
    def __init__(self):
        super().__init__()

        # threading initiation
        self.mainWindowThread = threading.Thread(target=self.window)
        self.mainWindowThread.start()
        
        self.song_dir, self.song_name, self.file_found, self.music_list = "","","", ""
        global pas, tl, Stop
        self.check_song, self.slide, tl = "","",""
        self.song_len = ""
        pas = False
        self.muted = True
        self.paused = False
        Stop = False
        
        pygame.mixer.init()
        
        #APPLICATION MAIN ICON
        self.mainico = self.getimages(self.MAIN)
        self.windows.iconphoto(False, self.mainico)


        #RIGHT FRAME
        self.rightFrame = Frame(self.root,height=600, width=620, bg=self.FRAME_COLOR_THEME)
        self.rightFrame.place(x=250, y=20)

        #RIGHTCONTENT FRAME, NOW PLAYING SONG 
        self.imageee = self.getimages(self.RIGHT_FRAME)
        self.rightCONTENTFrame = Frame(self.root, height=620, width=250,bg=self.FRAME_COLOR_THEME)
        self.rightCONTENTFrame.place(x=810, y=0)
        self.sha = Label(self.rightCONTENTFrame, height=620, width=250, image=self.imageee, borderwidth=0)
        self.sha.place(x=0,y=0)

        
        self.nowplay = Frame(self.rightCONTENTFrame, height=30, width=200,bg='#464545')
        self.nowplay.place(x=23, y=20)
        self.nowplaylbl = Label(self.nowplay, text='',fg='white', bg='#464545',font=('CreatoDisplay-Bold', 13))
        self.nowplaylbl.place(x=25,y=0)
        self.nowplaypic = Frame(self.rightCONTENTFrame, height=200, width=200, bg='#1e1e1e')
        self.nowplaypic.place(x=23,y=50)

        self.detailsframe = Frame(self.rightCONTENTFrame, height=70, width=225, bg=self.FRAME_COLOR_THEME)
        self.detailsframe.place(x=23, y=245)
        
        self.song_info = Label(self.detailsframe, text="Unknown Song", bg=self.FRAME_COLOR_THEME, fg=self.FRAME_TEXT_COLOR_THEME)
        self.song_info.config(font=('CreatoDisplay-Bold', 11))
        self.song_info.place(x=0, y=15)
    
        self.song_info1 = Label(self.detailsframe, text="Unknown Artist", bg=self.FRAME_COLOR_THEME, fg=self.FRAME_TEXT_COLOR_THEME)
        self.song_info1.place(x=0, y=35)

        #MUSIC LIST DISPLAY BOX
        self.musicboxFRAME = Frame(self.root,height=500, width=560)
        self.musicboxFRAME.place(x=250,y=20)
        self.music_list = Listbox(self.musicboxFRAME, height=27, width=89, border=0  ,bg="#1e1e1e", fg=self.TEXT_COLOR)
        self.music_list.pack(side='left', fill='y')
        self.scroll = ttk.Scrollbar(self.musicboxFRAME, orient='vertical')
        self.scroll.pack(side='right', fill='y')

        #LEFT FRAME-----------------------------------------------------------------------------------
        self.leftFrame = Frame(self.root, height=620, width=250, bg=self.FRAME_COLOR_THEME)#bg='#eeeeee'
        self.leftFrame.place(x=0,y=0)
        self.lftImg = self.getimages(self.LEFT_FRAME)
        self.lftframe = Label(self.leftFrame, height=700, width=250, image=self.lftImg, borderwidth=0)
        self.lftframe.place(x=0, y=0)
        
        #HEADING (PLAYER NAME)
        self.head = Frame(self.leftFrame, height=50, width=173,bg=self.FRAME_COLOR_THEME)
        self.head.place(x=35,y=15)
        self.pic = self.getimages(self.LOGO)
        self.headlbl = Label(self.head, image=self.pic, bg=self.FRAME_COLOR_THEME) #font=('CoolveticaRg-Regular', 25) text='MusicByte',
        self.headlbl.place(x=0, y=5)

        #MANAGEMENT i.e ADD SONGS AND ETC OPTIONS
        self.addlibrary = Frame(self.leftFrame, height=280, width=210, bg=self.FRAME_COLOR_THEME)
        self.addlibrary.place(x=10, y=70)

        self.text2 = Label(self.addlibrary, text="Folder",font=('CreatoDisplay-BOLD', 13), fg=self.TEXT_COLOR,bg=self.FRAME_COLOR_THEME) #SUBHEADINGS
        self.text2.place(x=55,y=40)
        self.folderico = self.getimages(self.FOLDER)
        self.folderlabel = Label(self.addlibrary, image=self.folderico, bg=self.FRAME_COLOR_THEME)
        self.folderlabel.place(x=28,y=43)
        self.btn = Button(self.addlibrary, activebackground=self.FRAME_COLOR_THEME, text="Tambahkan Folder",font=('CreatoDisplay-REGULAR', 12), borderwidth=0, fg=self.TEXT_COLOR,bg=self.FRAME_COLOR_THEME, command=self.addlibFolder) #ADD FOLDER TO LIBRARY
        self.btn.place(x=55,y=70)
        self.btn3 = Button(self.addlibrary, activebackground=self.FRAME_COLOR_THEME, text="Hapus Folder",font=('CreatoDisplay-REGULAR', 12), borderwidth=0, fg=self.TEXT_COLOR,bg=self.FRAME_COLOR_THEME, command=lambda: self.removeSongs('ALL')) #Removes all songs from LIBRARY
        self.btn3.place(x=55,y=95) #145
        self.textmus = Label(self.addlibrary, text="Musik",font=('CreatoDisplay-BOLD', 13), fg=self.TEXT_COLOR,bg=self.FRAME_COLOR_THEME) #SUBHEADINGS
        self.textmus.place(x=55,y=135)
        self.musicico = self.getimages(self.MUSIC)
        self.musiclabel = Label(self.addlibrary, image=self.musicico, bg=self.FRAME_COLOR_THEME)
        self.musiclabel.place(x=28,y=138)
        self.btn1 = Button(self.addlibrary, activebackground=self.FRAME_COLOR_THEME, text="Tambahkan Musik",font=('CreatoDisplay-REGULAR', 12), borderwidth=0, fg=self.TEXT_COLOR,bg=self.FRAME_COLOR_THEME, command=self.addSongs) #ADD SONGS TO LIBRARY
        self.btn1.place(x=55,y=165)
        self.btn2 = Button(self.addlibrary, activebackground=self.FRAME_COLOR_THEME, text="Hapus Musik",font=('CreatoDisplay-REGULAR', 12), borderwidth=0, fg=self.TEXT_COLOR,bg=self.FRAME_COLOR_THEME, command=lambda: self.removeSongs('ONE')) #Removes current song from LIBRARY
        self.btn2.place(x=55,y=190)

        #FRAME BAWAH
        self.framebawah = Frame(self.root, height=180, width=560, bg=self.FRAME_COLOR_THEME)
        self.framebawah.place(x=250, y=488)

        #CONTROL FRAME (MAIN)-------------------------------------------------------------------------
        self.controlFRAME = Frame(self.framebawah,height=100, width=560, background=self.FRAME_COLOR_THEME)
        self.controlFRAME.place(x=0, y=25)

        #Time FUNCTION
        self.sliderlength = Frame(self.controlFRAME, height=21, width=35, bg=self.FRAME_COLOR_THEME)
        self.sliderlength.place(x=500, y=5)
        self.sliderlengthlbl = Label(self.sliderlength, text='00:00', bg=self.FRAME_COLOR_THEME, fg=self.FRAME_TEXT_COLOR_THEME)
        self.sliderlengthlbl.place(x=0,y=0)
        self.timeframe = Frame(self.controlFRAME, height=21, width=40)
        self.timeframe.place(x=20, y=7)
        self.progressBar = Label(self.timeframe, text="00:00", relief=GROOVE, anchor=E, borderwidth=0, bg=self.FRAME_COLOR_THEME, fg=self.FRAME_TEXT_COLOR_THEME)
        self.progressBar.pack(fill=X, side=BOTTOM)


        #SLIDER FRAME
        self.sliderFrame = Frame(self.controlFRAME, height=21, width=350, bg=self.FRAME_COLOR_THEME)
        self.sliderFrame.place(x=58, y=4)
        self.sliderstyle = ttk.Style()
        self.sliderstyle.configure("TScale", background=self.FRAME_COLOR_THEME)
        self.progressBar1 = ttk.Scale(self.sliderFrame, from_=0, to=100, orient=HORIZONTAL, value=0,length=432, command=self.slider)
        self.progressBar1.pack()


        #CONTROLS
        self.controlFrame1 = Frame(self.controlFRAME, height=48, width=140, bg=self.FRAME_COLOR_THEME)
        self.controlFrame1.place(x=200,y=33)

        self.icon1 = self.getimages(self.PLAY)
        global playBTN
        playBTN = Button(self.controlFrame1, activebackground=self.FRAME_COLOR_THEME, image=self.icon1, borderwidth=0, bg=self.FRAME_COLOR_THEME, command=lambda: self.play(self.paused))
        self.icon3 = self.getimages(self.FORWARD)
        self.forewardBTN = Button(self.controlFrame1, activebackground=self.FRAME_COLOR_THEME, image=self.icon3, borderwidth=0, bg=self.FRAME_COLOR_THEME, command=self.foreward)
        self.icon4 = self.getimages(self.BACK)
        self.backBTN = Button(self.controlFrame1, activebackground=self.FRAME_COLOR_THEME, image=self.icon4, borderwidth=0, bg=self.FRAME_COLOR_THEME, command=self.previous)
        self.icon5 = self.getimages(self.DEC_VOL)

        self.backBTN.place(x=0,y=5)
        playBTN.place(x=45,y=0)
        self.forewardBTN.place(x=104,y=5)

        
        #SHUFFLE AND REPEAT
        self.shufflerepeat = Frame(self.controlFRAME, height=30, width=30, bg=self.FRAME_COLOR_THEME)
        self.shufflerepeat.place(x=20, y=48)
        
        global shuffleBTN, repeatBTN, shuffled, repeated
        shuffled = False
        repeated = False
        self.shuffleBTNimg = self.getimages(self.SHUFFLE)
        self.repeatBTNimg= self.getimages(self.REPEAT)
        
        shuffleBTN = Button(self.shufflerepeat, image=self.shuffleBTNimg, borderwidth=0, command=self.shuffle, bg=self.FRAME_COLOR_THEME, activebackground=self.FRAME_COLOR_THEME)
        shuffleBTN.grid(column=0, row=0)
        repeatBTN= Button(self.shufflerepeat, image=self.repeatBTNimg, borderwidth=0, command=self.repeat, bg=self.FRAME_COLOR_THEME, activebackground=self.FRAME_COLOR_THEME)
        repeatBTN.grid(column=1, row=0, padx=10)


        #VOLUME SLIDER
        self.volsliderFrame = Frame(self.controlFRAME, height=21, width=300, bg=self.FRAME_COLOR_THEME)
        self.volsliderFrame.place(x=415, y=43)
        self.imginvol = self.getimages(self.INC_VOL)
        self.imgdevol = self.getimages(self.DEC_VOL)
        self.devol = Label(self.volsliderFrame, image=self.imgdevol, borderwidth=0, bg=self.FRAME_COLOR_THEME, activebackground=self.FRAME_COLOR_THEME)
        self.devol.grid(column=0, row=0)
        self.volumeSlider = ttk.Scale(self.volsliderFrame, from_=0, to=1, orient=HORIZONTAL, value=0.75,length=75, command=self.volume)
        self.volumeSlider.grid(column=1, row=0, padx=5)
        self.invol = Label(self.volsliderFrame, image=self.imginvol, borderwidth=0, bg=self.FRAME_COLOR_THEME, activebackground=self.FRAME_COLOR_THEME)
        self.invol.grid(column=2, row=0, padx=5)
        
        
    def updatetitle(self, title):
        global tl
        tl = title
        title = title.replace('       ', '')
        
        if self.file_found != True:
            title = f'Wave - Add songs to playlist first! ' + title
            self.root.title(title)
            self.root.update()
            return
        title = f'Wave - Playing:   ' + title
        self.windows.title(title)
        self.windows.update()
    
    
    def getsongINFO(self):
        global pas, Stop
        if Stop:
            return
        activeClick = self.music_list.get(ACTIVE)
        activeClick = activeClick.replace('       ', '')
        self.song = os.path.join(self.song_dir, activeClick)
        try:
            song_load = MP3(self.slide)
        except:
            return
        self.song_len = song_load.info.length
        def gettime():
            currentTIME = pygame.mixer.music.get_pos() / 1000
            ctyme = time.strftime('%M:%S', time.gmtime(currentTIME))
            styme = time.strftime('%M:%S', time.gmtime(float(self.song_len)))
            #currentTIME+=1
            if int(self.progressBar1.get() == int(self.song_len)):
                self.progressBar.config(text=styme)
                self.foreward()
            elif self.paused:
                pass
            elif int(self.progressBar1.get()) == int(currentTIME):
                #no movement to the slider
                self.sliderPOS = int(self.song_len)
                self.progressBar1.config(to=self.sliderPOS, value=int(currentTIME))
            else:
                #slider moved
                self.sliderPOS = int(self.song_len)
                self.progressBar1.config(to=self.sliderPOS, value=int(self.progressBar1.get()))
                ctyme = time.strftime('%M:%S', time.gmtime(int(self.progressBar1.get())))
                self.sliderlengthlbl.config(text=styme)
                self.progressBar.config(text=ctyme)
                nextt = int(self.progressBar1.get()) + 1
                self.progressBar1.config(value=nextt)

            self.progressBar.after(1000, gettime)
        if pas == False:
            gettime()
            pas = True
        else:
            pass
            


    def nextinfo(self, info):
        if info == None:
            pass

        else:
            try:
                song_load = MP3(info)
            except:
                info = info.replace("\\", "/")
            song_load = MP3(info)
            song_len1 = song_load.info.length
            styme1 = time.strftime('%M:%S', time.gmtime(song_len1))
            tagg = eye.Tag()
            tagg.parse(info)
            artist = tagg.artist
            
            if artist == None:
                pass

            else:
                pass


            # bitrate = song_load.info.bitrate / 1000


    
    def slider(self, x):
        '''activeClick = self.music_list.get(ACTIVE)
        activeClick = activeClick.replace('       ','')
        song = os.path.join(self.song_dir, activeClick)'''
        try:
            pygame.mixer.music.load(self.slide)
            pygame.mixer.music.play(loops=0, start=int(self.progressBar1.get()))
        except:
            pass
        #sliderLBL.config(text=f'{int(progressBar1.get())} 
    
    def volume(self, percent):
        pygame.mixer.music.set_volume(self.volumeSlider.get())
        # vol = pygame.mixer.music.get_volume() * 100
        # self.vLabelpercent.config(text=f'{int(vol)}%')
        
    def mute(self,muteornot):
        global muteBTN
        if muteornot:
            pygame.mixer.music.set_volume(0)
            # self.vLabelpercent.config(text='self.mutedd')
            icon5 = self.getimages(self.DEC_VOL)
            muteBTN.config(image=icon5)
            muteBTN.img = icon5
            self.muted = False
        else:
            pygame.mixer.music.set_volume(self.volumeSlider.get())
            vol = pygame.mixer.music.get_volume() * 100
            # self.vLabelpercent.config(text=f'{int(vol)}%')
            icon6 = self.getimages(self.INC_VOL)
            muteBTN.config(image=icon6)
            muteBTN.img = icon6
            self.muted = True
    
    def getmetadata(self, filee):
        tag = eye.Tag()
        try:
            tag.parse(filee)
            artist = tag.artist
            title = tag.title
            if artist == None:
                self.song_info1.config(text='Unknown Artist')
            else:
                self.song_info1.config(text=artist)
            if title == None:
                self.song_info.config(text='Unknown Title', font=('CreatoDisplay-Bold', 11))
            else:
                self.song_info.config(text=title, font=('CreatoDisplay-Bold', 11))
            self.file_found = True
        except:
            pass
        try:
            load = MP3(filee)
            songbit = load.info.bitrate // 1000
            self.songbitrate.config(text=f'Bitrate: {songbit}kbps')
        except:
            return
        
    def getalbumArt(self, art, nextart):
        
        self.getmetadata(art)
        if self.file_found !=True:
            return
        image = 'Artwork-now.jpg'
        image2 = 'Artwork-next.jpg'
        backgroundIMG = 'bg.png'

        currentdir = os.getcwd()
        Folder = 'mp3playerCache'
        workinfFolder = os.path.join(currentdir, Folder)

        if not os.path.exists(workinfFolder):
            os.makedirs(workinfFolder)
        path = os.path.join(workinfFolder, image)

        path2 = os.path.join(workinfFolder, image2)
        BGPath = os.path.join(workinfFolder, backgroundIMG)
        # For Current Album Art
        try:
            metadata=audio_metadata.load(art)
            artwork = metadata.pictures[0].data
            with open(path, 'wb') as f:
                f.write(artwork)
            width = 200
            height = 200
            imggg = SM.open(path)
            try:
                left = 6
                top = self.screen_height / 2
                right = 900
                bottom = 2 * self.screen_height / 2
                im1 = imggg.crop((left, top, right, bottom)) 
                im2 = im1.resize((self.screen_width,self.screen_height), SM.LANCZOS)
                im2 = im2.filter(ImageFilter.GaussianBlur(radius=15)) 
                im2.save(BGPath)
                im2 = self.getimages(BGPath)
                self.background.config(image=im2)
                self.background.img = im2
            except:
                pass
            imggg = imggg.resize((width,height), SM.LANCZOS)
            photoImg =  ImageTk.self.getimages()
            for things in self.nowplaypic.winfo_children():
                things.destroy()
            self.nowplayingLabel = Label(self.nowplaypic, height=200, width=200, image=photoImg, borderwidth=0)
            self.nowplayingLabel.img = photoImg
            self.nowplayingLabel.place(x=0,y=0)
        except:
            # pass
            for things in self.nowplaypic.winfo_children():
                things.destroy()
            imgg = self.get_icons(self.NO_IMAGE)
            self.nowplayingLabel = Label(self.nowplaypic, height=200, width=200, image=imgg, borderwidth=0)
            self.nowplayingLabel.img = imgg
            self.nowplayingLabel.place(x=0,y=0)
        
   
    def addlibFolder(self):
        self.song_dir = filedialog.askdirectory()
        try:
            songs = os.listdir(self.song_dir)
            # Filter hanya file dengan ekstensi ".mp3"
            mp3_files = [song for song in songs if song.endswith('.mp3')]
            self.file_found = True
        except FileNotFoundError:
            self.file_found = False
            return
        # iconnn = self.getimages(self.PLAY)
        # playBTN.config(image=iconnn)
        # playBTN.img = iconnn

        self.music_list.delete('0', 'end')
        self.music_list.config(yscrollcommand=self.scroll.set)
        self.scroll.config(command=self.music_list.yview)
        
        for song in mp3_files:
            self.music_list.config(font=('CreatoDisplay-THIN',10))
            self.music_list.insert(END, f'       {song}')
        
        self.music_list.config(height=29, width=67)
        

    def addSongs(self):
        global playBTN
        
        songFilename = filedialog.askopenfilenames(initialdir="/", title="Select File",
                                            filetypes=(("mp3 files", "*.mp3"),("all files", "*.*")))  
        if songFilename == "":
            self.file_found = False
            return
        else:
            self.file_found = True 
        # iconnn = self.getimages(self.PLAY)
        # playBTN.config(image=iconnn)
        # playBTN.img = iconnn                                 
        # self.music_list.delete('0', 'end')                                     
        # self.music_list.insert(ANCHOR, " \n ")                                      
        for song in songFilename:                                 
            self.song_name = os.path.basename(song)
            self.music_list.config(font=('CreatoDisplay-THIN',10))
            self.music_list.insert(END, f'       {self.song_name}')
        # self.music_list.config(height=29, width=67)
        self.music_list.config(height=29, width=67)
        try:
            path = songFilename[0]
        except IndexError:
            return
        self.song_name = os.path.basename(path)
        path = path.replace(self.song_name, "")
        self.song_dir = path.replace("\\", "/")
        
        
        
    
    def play(self, check):
        global Stop, tl, repeated, shuffled
        global  playBTN
        try:
            Stop = False
            activeClick = self.music_list.get(ACTIVE)
            self.updatetitle(activeClick)
            song = os.path.join(self.song_dir, activeClick)
            song = song.replace('\\', '/')
            song = song.replace('       ', '')
            ran = random.randint(-2, 2)
            upnext = self.music_list.curselection()
            if repeated or shuffled:
                if repeated:
                    upnext=upnext[0]
                if shuffled:
                    upnext=upnext[0]+ran
            else:
                upnext = upnext[0]+1
            # upnext = upnext[0]+1
            song2 = self.music_list.get(upnext)
            filetype = song2[-3:]
            filetype = filetype.lower()
            if filetype == "mp3" or filetype == "wav" or filetype == "m4a" or filetype == "aac":
                path2 = os.path.join(self.song_dir, song2)
                path2 = path2.replace('\\', '/')
                path2 = path2.replace('       ', '')
            else:
                path2 = None

            self.nextinfo(path2)
            if song != self.check_song:
                try:
                    pygame.mixer.music.load(song)
                    pygame.mixer.music.play(loops=0)
                    self.slide = song
                    icon2 = self.getimages(self.PAUSE)
                    playBTN.config(image=icon2)
                    playBTN.img = icon2
                    self.check_song = song
                    self.paused = False
                    #Reset Progress Slider
                    self.progressBar1.config(value=0)
                    self.getsongINFO()
                    #sliderPOS = int(self.song_len)
                    #progressBar1.config(to=sliderPOS, value=0)
                except:
                    pass
            elif self.check_song == song:
                self.paused = check
                if self.paused:
                    tl = tl.replace('       ', '')
                    t = f'Wave - Playing:   ' + tl
                    pygame.mixer.music.unpause()
                    icon2 = self.getimages(self.PAUSE)
                    playBTN.config(image=icon2)
                    playBTN.img = icon2
                    self.windows.title(t)
                    self.windows.update()
                    self.paused = False
                else:
                    t = 'Wave - Paused'
                    pygame.mixer.music.pause()
                    iconnn = self.getimages(self.PLAY)
                    playBTN.config(image=iconnn)
                    playBTN.img = iconnn
                    self.windows.title(t)
                    self.windows.update()
                    self.paused = True
            self.getalbumArt(song, path2)
        except:
            False
    
    def play_space(self, event:None):
        self.play(self.paused)
    
    def foreward(self):
        global playBTN, repeated, shuffled
        upnext = self.music_list.curselection()
        iconnn = self.getimages(self.PAUSE)
        playBTN.config(image=iconnn)
        playBTN.img = iconnn
        # print(ran)
        #Get the next song number (Tuple Number)
        nextsong = self.music_list.curselection()
        try:
            if repeated or shuffled:
                if repeated:
                    nextsong = nextsong[0]
                if shuffled:
                    ran = random.randint(-2, 2)
                    # self.music_list.selection_set
                    nextsong = nextsong[0]+ran
                    # print("bisa")
            else:
                nextsong = nextsong[0]+1
            # nextsong = nextsong[0]+1
        except:
            return
        upnext = upnext[0]+2
        song2 = self.music_list.get(upnext)
        filetype = song2[-3:]
        filetype = filetype.lower()
        if filetype == "mp3": #or filetype == "wav" or filetype == "m4a" or filetype == "aac":
            path2 = os.path.join(self.song_dir, song2)
            path2 = path2.replace('\\', '/')
            path2 = path2.replace('       ', '')
        else:
            path2 = None

        song = self.music_list.get(nextsong)
        if song == "" or song == None:
            return
        #Reset Progress Slider
        self.progressBar1.config(value=0)

        path = os.path.join(self.song_dir, song)
        path = path.replace('\\', '/')
        path = path.replace('       ', '')
        self.slide = path
        try:
            pygame.mixer.music.load(path)
            pygame.mixer.music.play(loops=0)
            self.slide = path
            self.paused = False
            self.check_song = path
            self.getsongINFO()
        except:
            pass
        try:
            self.music_list.selection_clear(0, END)
            self.music_list.activate(nextsong)
            self.music_list.selection_set(nextsong, last=None)
            self.updatetitle(self.music_list.get(ACTIVE))
        except:
            pass
        self.nextinfo(path2)
        self.getalbumArt(path, path2)
    
    def previous(self):
        global playBTN
        iconnn = self.getimages(self.PAUSE)
        playBTN.config(image=iconnn)
        playBTN.img = iconnn
        upnext = self.music_list.curselection()

        previoussong = self.music_list.curselection()
        previoussong = previoussong[0]-1
        song = self.music_list.get(previoussong)

        upnext = upnext[0]
        song2 = self.music_list.get(upnext)

        if previoussong <=0:
            return

        try:
            path2 = os.path.join(self.song_dir, song2)
            path2 = path2.replace('\\', '/')
            path2 = path2.replace('       ', '')
        except:
            path2 = None

        self.nextinfo(path2)
        path = os.path.join(self.song_dir, song)
        path = path.replace('\\', '/')
        path = path.replace('       ', '')


        try:
            #Reset Progress Slider
            self.progressBar1.config(value=0)

            pygame.mixer.music.load(path)
            pygame.mixer.music.play(loops=0)
            self.paused = False
            self.check_song = path
            self.slide = path
            self.getsongINFO()
        except:
            pass

        try:
            self.music_list.selection_clear(0, END)
            self.music_list.activate(previoussong)
            self.music_list.selection_set(previoussong, last=None)
            self.updatetitle(self.music_list.get(ACTIVE))
        except:
            pass
        self.getalbumArt(path, path2)
    
    def removeSongs(self, typee):
        global Stop
        currentsong = self.music_list.curselection()
        #nextsong = currentsong[0]+1
        
        if typee == 'ONE':
            try:
                #Reset Progress Slider
                self.progressBar1.config(value=0)
                self.music_list.delete(currentsong)
                pygame.mixer.music.stop()

                self.music_list.selection_set(currentsong, last=None)
                nextsong = 0
                
                Stop = True
            except:
                pass
        elif typee == 'ALL':
            #Reset Progress Slider
            self.progressBar1.config(value=0)
            self.music_list.delete(0, END)
            pygame.mixer.music.stop()
            
            Stop = True
        else:
            pass

    def shuffle(self):
        global shuffleBTN, shuffled, repeated
        if shuffled:
            shuffled = False
            imggg = self.getimages(self.SHUFFLE)
            shuffleBTN.config(image=imggg)
            shuffleBTN.img = imggg
            # repeated = True
            
            # print("01")

        else:
            shuffled = True
            imgg = self.getimages(self.SHUFFLE_ON)
            shuffleBTN.config(image=imgg)
            shuffleBTN.img = imgg
            # print("00")
            if repeated:
                self.repeat()
    
    def repeat(self):
        global repeatBTN, repeated, shuffled
        if repeated:
            repeated = False
            imggg= self.getimages(self.REPEAT)
            repeatBTN.config(image=imggg)
            repeatBTN.img = imggg
            # print("11")
        else:
            repeated = True
            imgg1 = self.getimages(self.REPEAT_ON)
            repeatBTN.config(image=imgg1)
            repeatBTN.img = imgg1
            # print("10")
            if shuffled:
                self.shuffle()
        
    

        

if __name__ == "__main__":
    App=MusicPlayer()
    App.windows.mainloop()
