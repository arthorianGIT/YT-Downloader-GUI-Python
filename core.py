import yt_dlp
import asyncio

async def video_info(url):
    info = await asyncio.to_thread(yt_dlp.YoutubeDL().extract_info, url, download=False)
    return info

async def download_video(url, video_ext_value, video_scale_value):
    ydl_opts = {
        'format': f'bestvideo[height={video_scale_value.split('p')[0]}][ext={video_ext_value.lower()}]',
        'quiet': False,
        'outtmpl': 'E:/test_videos_audios/%(uploader)s - %(title)s.%(ext)s'
    }
    await asyncio.to_thread(yt_dlp.YoutubeDL(ydl_opts).download, [url])

async def download_audio(url, audio_ext_value, audio_kbps_value):
    ydl_opts = {
        'format': 'bestaudio',
        'extractaudio': True,
        'audioformat': f'{audio_ext_value.lower()}',
        'quiet': False,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': f'{audio_ext_value.lower()}',
            'preferredquality': f'{audio_kbps_value.split('k')[0]}'
        }],
        'outtmpl': 'E:/test_videos_audios/%(title)s.%(ext)s'
    }
    await asyncio.to_thread(yt_dlp.YoutubeDL(ydl_opts).download, [url])

async def download_both(url, video_ext_value, video_scale_value, audio_ext_value, audio_kbps_value):
    ydl_opts = {
        'format': f'bestvideo[height<={video_scale_value.split('p')[0]}]+bestaudio[ext={audio_ext_value.lower()}][tbr<={audio_kbps_value.split('k')[0]}]',
        'merge_output_format': f'{video_ext_value.lower()}',
        'quiet': False,
        'outtmpl': 'E:/test_videos_audios/%(uploader)s - %(title)s'
    }
    await asyncio.to_thread(yt_dlp.YoutubeDL(ydl_opts).download, [url])