import tkinter as tk
import os
import subprocess

try:
    from pytube import YouTube
    from pytube import Playlist
except Exception as e:
    print("Modules are missing {}".format(e))

#GLOBAL VARIABLES
formatOM = tk.OptionMenu


#FONCTIONS
def fncSearchInYouTube():
    fncURLAddress = urlTextBox.get()
    if str(fncURLAddress) != "":
        try:
            video = YouTube(urlTextBox.get())
            #Write video title to titleLabel
            titleLabel.configure(text=str(video.title))

            #Create options to download file
            videoStream = video.streams
            formatList = []
            for x in range(len(videoStream)):
                tempString = str(videoStream[x]).split('"')
                if tempString[5][-1] == "p":
                    formatList.append(tempString[3][6:] + " " +tempString[5])
            formatList = sorted(formatList)

            #Format label
            formatLabel = tk.Label(gui, text="Choose your movie format: ")
            formatLabel.place(x=10, y= 110)
            #Format listbox
            variable = tk.StringVar()
            variable.set("Format")  # default value
            formatOM = tk.OptionMenu(gui, variable, *formatList)
            formatOM.place(x=10, y=130)
            #Path label
            if os.name == 'nt':
                path = os.getcwd() + '\\'
            else:
                path = os.getcwd() + '/'

            def fncDownloadMovie():
                downloadValues = str(variable.get()).split(" ")
                print(downloadValues)
                downloadFormat = downloadValues[0]
                downloadQuality = downloadValues[1]
                krotka = tuple()
                for x in range(len(videoStream)):
                    tempString = str(videoStream[x]).split('"')
                    krotka += (tempString[1], tempString[3][6:], tempString[5])

                for x in range(len(krotka) - 1):
                    if (str(krotka[x]) == str(downloadFormat) and str(krotka[x + 1]) == str(downloadQuality)):
                        video.streams.get_by_itag(int(krotka[x - 1])).download(path)
                        break

            def fncDownloadMp3():
                name = str(video.title)
                file = YouTube(fncURLAddress).streams.filter(only_audio=True).first().download(path, filename=name)
                base = os.path.splitext(file)[0]
                os.rename(file, base+'.mp3')
                return 1

            #Button download video
            downloadVideoBtn = tk.Button(gui, text="Download movie", command=fncDownloadMovie)
            downloadVideoBtn.place(x=140, y=132)

            #Botton download mp3
            downloadMp3Btn = tk.Button(gui, text="Download MP3", command=fncDownloadMp3)
            downloadMp3Btn.place(x=260, y=132)

        except Exception as e:
            print("Error: {}".format(e))
    return 1

# Create window
gui = tk.Tk(className='YouTube Downloader by Krzysztof Szczęsniak')
# Window size
gui.geometry("600x300")

#ALL LABEL BELOW
# Label link to movie
linkToMovieLabel = tk.Label(gui, text="Your video URL address:")
linkToMovieLabel.place(x=10, y=10)
#Title label text
titleLabelText = tk.Label(gui, text="Video title:")
titleLabelText.place(x=10, y=60)
#Tile label
titleLabel = tk.Label(gui, text="", font="Helvetica 9 bold")
titleLabel.place(x=10, y=80)

#ALL TEXTBOX BELOW
#TextBox URL
urlAddress = tk.StringVar()
urlTextBox = tk.Entry(gui, width=80, textvariable=urlAddress)
urlTextBox.place(x=10, y=30)



#ALL BUTTONS BELOW
#Button search video in YouTube
searchBtn = tk.Button(gui, text="Search", command=fncSearchInYouTube)
searchBtn.place(x=500, y=26)

#Execute window
gui.mainloop()