# telegram_video_summary_bot/telegram_bot/telegram_client.py
from telethon import TelegramClient
import os

class TelegramBotClient:
    def __init__(self, api_id, api_hash, session_name='telegram_bot'):
        self.client = TelegramClient(session_name, api_id, api_hash)

    async def list_videos(self, canais):
        videos = []
        async with self.client:
            for canal in canais:
                async for message in self.client.iter_messages(canal):
                    if message.video:
                        videos.append((canal, message.id, message.message, message.date))
                        print(f"Vídeo encontrado no canal {canal}: {message.id}")
                        print(f"Data: {message.date}")
                        print(f"Descrição: {message.message}")
                        print("----------")
        return videos

    async def download_video(self, canal, message_id, download_path):
        async with self.client:
            message = await self.client.get_messages(canal, ids=message_id)
            if message.video:
                await message.download_media(file=download_path)
                print(f"Vídeo baixado: {download_path}")
                return download_path
        return None

    # Adicione este método para obter uma mensagem específica
    async def get_message(self, canal, message_id):
        async with self.client:
            message = await self.client.get_messages(canal, ids=message_id)
            return message
