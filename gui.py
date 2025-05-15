import customtkinter as ctk
from core import video_info
from PIL import Image
import aiohttp
from io import BytesIO
import asyncio
import threading

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

    frame1 = ctk.CTkFrame(app, width=400, height=500, fg_color='#2c2c2c', bg_color='#2c2c2c')
    frame2 = ctk.CTkFrame(app, width=425, height=235 ,fg_color='#2c2c2c', bg_color='#2c2c2c')
    preview = ctk.CTkLabel(app, text='', text_color='white', fg_color='#242424', bg_color='#2c2c2c', width=300, height=200)
    url = ctk.CTkEntry(app, fg_color='#242424', bg_color='#2c2c2c', corner_radius=5, text_color='white',
                        font=('Helvetica', 14, 'bold'), width=230)
    get_info_button = ctk.CTkButton(app, text='Video Info', fg_color='#1474df', bg_color='#1474df', corner_radius=3,
                                    command=start_video_information)
    download_button = ctk.CTkButton(app, text='Download', fg_color='#1474df', bg_color='#1474df', corner_radius=3)
    description_textbox = ctk.CTkTextbox(app, width=375, height=200, font=('Helvetica', 17, 'bold'), border_width=2,
                                         fg_color='#242424', text_color='white', bg_color='#2c2c2c')

    description_textbox.insert('0.0', 'Title: None\nAuthor: None\nDuration: None\nPublish Date: None\n')
    description_textbox.configure(state='disabled')

    preview.place(x=85, y=50)
    url.place(x=120, y=310)
    get_info_button.place(x=200, y=365)
    download_button.place(x=165, y=420)
    description_textbox.place(x=485, y=30)
    frame1.place(x=40, y=0)
    frame2.place(x=460, y=15)

    app.mainloop()