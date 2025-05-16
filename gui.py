import customtkinter as ctk
from core import video_info, download_video, download_audio, download_both
from PIL import Image
import aiohttp
from io import BytesIO
import asyncio
import threading
from tkinter.filedialog import askdirectory

directory = 'C:/'

def interface():
    app = ctk.CTk()
    app.geometry('900x500')
    app.title('Downloader from different sites        Kirwl.Who')
    app.resizable(False, False)
    app._set_appearance_mode('dark')

    async def video_information(video_url):
        info = await video_info(video_url)
        async with aiohttp.ClientSession() as session:
            async with session.get(info['thumbnail']) as response:
                if response.status == 200:
                    image_data = await response.read()
                    img = ctk.CTkImage(dark_image=Image.open(BytesIO(image_data)), size=(300, 200))
                    preview.configure(image=img)
                else:
                    preview.configure(text='Cannot download template')
        description_textbox.configure(state='normal')
        description_textbox.delete('0.0', 'end')
        description_textbox.insert('0.0', f'Title: {info['title']}\nAuthor: {info['uploader']}\nDuration: {info['duration'] / 60:.2f} minutes\nPublish date: {info['upload_date']}\n')
        description_textbox.configure(state='disabled')
    
    def run_video_information():
        v_url = url.get().strip()
        asyncio.run(video_information(v_url))

    def start_video_information():
        threading.Thread(target=run_video_information).start()
    
    def run_video_audio_download():
        global directory
        v_url = url.get().strip()
        f_value = format_value.get()
        v_ext_value = video_ext_value.get()
        a_ext_value = audio_ext_value.get()
        a_kbps_value = audio_kbps_value.get()
        v_scale_value = video_scale_value.get()
        if f_value == 'Video+Audio':
            asyncio.run(download_both(v_url, v_ext_value, v_scale_value, a_ext_value, a_kbps_value, directory))
        elif f_value == 'Video':
            asyncio.run(download_video(v_url, v_ext_value, v_scale_value, directory))
        elif f_value == 'Audio':
            asyncio.run(download_audio(v_url, a_ext_value, a_kbps_value, directory))
    
    def start_download_video_audio():
        threading.Thread(target=run_video_audio_download).start()
    
    def change_directory():
        global directory
        directory = askdirectory()

    frame1 = ctk.CTkFrame(app, width=400, height=500, fg_color='#2c2c2c', bg_color='#2c2c2c')
    frame2 = ctk.CTkFrame(app, width=425, height=235, fg_color='#2c2c2c', bg_color='#2c2c2c')
    frame3 = ctk.CTkFrame(app, width=425, height=230, fg_color='#2c2c2c', bg_color='#2c2c2c')
    preview = ctk.CTkLabel(app, text='', text_color='white', fg_color='#242424', bg_color='#2c2c2c', width=300, height=200)
    url = ctk.CTkEntry(app, fg_color='#242424', bg_color='#2c2c2c', corner_radius=5, text_color='white',
                        font=('Helvetica', 14, 'bold'), width=230)
    get_info_button = ctk.CTkButton(app, text='Video Info', fg_color='#1474df', bg_color='#1474df', corner_radius=3,
                                    command=start_video_information, width=100)
    download_button = ctk.CTkButton(app, text='Download', fg_color='#1474df', bg_color='#1474df', corner_radius=3,
                                    command=start_download_video_audio, width=100)
    directory_button = ctk.CTkButton(app, text='Save Directory', fg_color='#1474df', bg_color='#1474df', corner_radius=3,
                                     command=change_directory)
    description_textbox = ctk.CTkTextbox(app, width=375, height=200, font=('Helvetica', 17, 'bold'), border_width=2,
                                         fg_color='#242424', text_color='white', bg_color='#2c2c2c')
    format_value = ctk.StringVar(value='Video+Audio')
    download_format_combobox = ctk.CTkComboBox(app, width=200, values=['Video+Audio', 'Video', 'Audio'],
                                               bg_color='#2c2c2c', corner_radius=10, font=('Helvetica', 15, 'bold'),
                                               button_color='#41517e', border_color='#41517e', variable=format_value)
    video_ext_value = ctk.StringVar(value='MP4')
    download_video_ext_combobox = ctk.CTkComboBox(app, width=200, values=['MP4', 'WEBM', 'MKV'], corner_radius=10,
                                                   font=('Helvetica', 15, 'bold'), button_color='#41517e',
                                                   border_color='#41517e', variable=video_ext_value, bg_color='#2c2c2c')
    audio_ext_value = ctk.StringVar(value='MP3')
    download_audio_ext_combobox = ctk.CTkComboBox(app, width=200, corner_radius=10, font=('Helvetica', 15, 'bold'),
                                                  bg_color='#2c2c2c', button_color='#41517e', variable=audio_ext_value,
                                                    values=['M4A', 'OPUS', 'VORBIS', 'MP3', 'WAV'])
    audio_kbps_value = ctk.StringVar(value='192kbps')
    download_audio_kbps_combobox = ctk.CTkComboBox(app, width=200, font=('Helvetica', 15, 'bold'), bg_color='#2c2c2c',
                                                   button_color='#41517e', border_color='#41517e', corner_radius=10,
                                                   variable=audio_kbps_value,
                                                   values=['320kbps', '256kbps', '192kbps', '160kbps', '128kbps', '96kbps', '64kbps'])
    video_scale_value = ctk.StringVar(value='720p')
    download_video_scale_combobox = ctk.CTkComboBox(app, width=180, font=('Helvetica', 15, 'bold'), corner_radius=10,
                                                    bg_color='#2c2c2c', border_color='#41517e', button_color='#41517e',
                                                    variable=video_scale_value, height=29,
                                                    values=['2160p', '1080p', '720p', '480p', '360p', '240p', '144p'])

    description_textbox.insert('0.0', 'Title: None\nAuthor: None\nDuration: None\nPublish Date: None\n')
    description_textbox.configure(state='disabled')

    preview.place(x=85, y=50)
    url.place(x=120, y=310)
    get_info_button.place(x=250, y=365)
    download_button.place(x=180, y=420)
    directory_button.place(x=100, y=365)
    description_textbox.place(x=485, y=30)
    download_format_combobox.place(x=485, y=290)
    download_video_ext_combobox.place(x=485, y=345)
    download_audio_ext_combobox.place(x=485, y=400)
    download_audio_kbps_combobox.place(x=485, y=455)
    download_video_scale_combobox.place(x=695, y=290)
    frame1.place(x=40, y=0)
    frame2.place(x=460, y=15)
    frame3.place(x=460, y=260)

    app.mainloop()