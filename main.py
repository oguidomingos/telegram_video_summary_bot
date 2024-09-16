# telegram_video_summary_bot/main.py
import asyncio
from transcriber.whisper_transcriber import WhisperTranscriber
from telegram_bot.telegram_client import TelegramBotClient
from agents.agent_manager import AgentManager

API_ID = 25822041
API_HASH = 'cbf47fe46777aab7dfa7478c67eca1e9'
VIDEO_DOWNLOAD_PATH = 'videos/'

# Configurações do LLaMA


config_list_llama = [{
    "model": "llama3-70b-8192",
    "api_key": "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",
    "base_url": "https://api.groq.com/openai/v1"

}]


# telegram_video_summary_bot/main.py
async def main():
    # Inicializa os componentes
    transcriber = WhisperTranscriber(model_size="base")
    telegram_bot = TelegramBotClient(API_ID, API_HASH)
    agent_manager = AgentManager(config_list_llama)

    # Listar vídeos
    canais_para_monitorar = [-1002144101724]  # Certifique-se de usar o ID correto
    print("Listando vídeos...")
    videos = await telegram_bot.list_videos(canais_para_monitorar)

    # Seleção manual do vídeo
    canal_selecionado = int(input("Digite o nome do canal para baixar o vídeo: "))  # Converta o ID para int
    message_id = int(input("Digite o ID da mensagem do vídeo que deseja baixar: "))

    # Baixar vídeo
    print(f"Iniciando o download do vídeo com ID da mensagem: {message_id}...")
    video_message = await telegram_bot.get_message(canal_selecionado, message_id)
    video_title = video_message.message  # Use o título da mensagem para o título do PDF
    video_path = f"{VIDEO_DOWNLOAD_PATH}video_{message_id}.mp4"
    video_path = await telegram_bot.download_video(canal_selecionado, message_id, video_path)

    if video_path:
        print(f"Vídeo baixado com sucesso em: {video_path}")
        # Transcrever e iniciar chat com agentes
        print("Iniciando a transcrição do vídeo...")
        transcricao = transcriber.transcribe_video(video_path)
        print("Transcrição concluída.")

        print("Iniciando a geração do resumo...")
        agent_manager.start_conversation(transcricao, video_title)


if __name__ == "__main__":
    asyncio.run(main())
