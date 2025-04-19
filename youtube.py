import requests
import tkinter as tk
import customtkinter as ctk
from PIL import Image, ImageTk
from io import BytesIO
from pytubefix import YouTube

def updateThumbnail(event):
    # Clear message label
    message.configure(text="")
    
    # Reset progress percentage and progress bar
    progress_percent.configure(text="0%")
    progress_bar.set(0)

    #get link and create object
    try:
        url_link = linkEntry.get()
        yt_obj = YouTube(url_link)
        message.configure(text = '')
        title.configure(text = yt_obj.title)

        #fetch image from the url
        response = requests.get(yt_obj.thumbnail_url)
        response.raise_for_status()
        image_data = BytesIO(response.content)

        #process the image with pillow
        pil_image = Image.open(image_data)
        pil_image.thumbnail((400,400))

        #convert image to tkinter format
        tk_image = ImageTk.PhotoImage(pil_image)
            
        #update the image on the existing label
        image_label.configure(image=tk_image)
        image_label.image = tk_image
    except Exception as e:
        print(e)
        message.configure(text = "Invalid link", text_color = "red")

    


def beginDownload():
    #download video 
    url_link = linkEntry.get()
    yt_obj = YouTube(url_link, on_progress_callback= while_downloading)
    try:
        video = yt_obj.streams.get_highest_resolution()
        video.download()
        message.configure(text = "Download Successful", text_color = 'white')
    except:
        message.configure(text = "Download Error", text_color = "red")

def while_downloading(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    percentage_completed = (bytes_downloaded/total_size) *100
    percent = str(int(percentage_completed))
    progress_percent.configure(text = percent + "%")
    progress_percent.update()

    progress_bar.set(percentage_completed/100)

#creating the GUI
ctk.set_appearance_mode("System") 
ctk.set_default_color_theme("blue")

window = ctk.CTk()
window.geometry("500x480")
window.title("My Youtube Downloader")

title = ctk.CTkLabel(master=window, text="Enter your link here: ")
title.pack(pady = 10)

link = tk.StringVar()
linkEntry = ctk.CTkEntry(master=window, width= 400, height= 30, textvariable=link)
linkEntry.pack(pady = 5)
linkEntry.bind("<KeyRelease>", updateThumbnail)

message = ctk.CTkLabel(window, text="")
message.pack()

downloadBtn = ctk.CTkButton(master=window, width=100, height=30, text="Download", command=beginDownload)
downloadBtn.pack(pady= 10)

#progress bar and percentage
progress_percent = ctk.CTkLabel(window, text = "0%")
progress_percent.pack()
progress_bar = ctk.CTkProgressBar(window, width=300)
progress_bar.set(0)
progress_bar.pack(pady=5)

# Create a Label to display the image
image_label = tk.Label(window)
image_label.pack(padx=20, pady=20)

window.mainloop()