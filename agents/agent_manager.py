import autogen
from fpdf import FPDF
import re


class AgentManager:
    def __init__(self, config_list_llama):
        self.llm_config = {
            "temperature": 0.7,  # Pode ser ajustado para controlar a criatividade
            "timeout": 300,
            "seed": 1,
            "config_list": config_list_llama,
            "max_tokens": 1000  # Ajuste conforme necessário
        }

        # Agente de resumo
        self.summarizer = autogen.AssistantAgent(
            name="Summarizer",
            system_message="Você é um especialista em resumir conteúdos. Sua tarefa é fornecer resumos detalhados e abrangentes em português do conteúdo fornecido. Foque em capturar os pontos-chave e fornecer detalhes importantes, sempre respondendo em português.",
            llm_config=self.llm_config,
        )

    def clean_text(self, text):
        # Remove caracteres não ASCII
        return re.sub(r'[^\x00-\x7F]+', '', text)

    def split_text(self, text, max_length=1500):
        # Divida o texto em pedaços menores com base no tamanho máximo
        words = text.split()
        for i in range(0, len(words), max_length):
            yield ' '.join(words[i:i + max_length])

    def start_conversation(self, message, video_title):
        # Divida a transcrição em partes menores
        parts = list(self.split_text(message, max_length=800))  # Ajuste o tamanho conforme necessário

        # Resumir cada parte
        all_responses = []
        for part in parts:
            expanded_message = (
                    "Por favor, resuma o seguinte conteúdo de forma detalhada, "
                    "destacando os pontos-chave e fornecendo uma visão abrangente. "
                    "O resumo deve ser feito em português:\n\n" + part
            )
            print("Resumindo uma parte do conteúdo...")
            response = self.summarizer.generate_reply(messages=[{"role": "user", "content": expanded_message}])
            print("Resumo de uma parte gerado com sucesso.")
            all_responses.append(response)

        # Combinar todos os resumos
        combined_response = "\n\n".join(all_responses)

        # Limpar título e resumo de caracteres especiais
        clean_title = self.clean_text(video_title)
        clean_response = self.clean_text(combined_response)

        # Exportar o resumo combinado como um arquivo PDF
        self.export_to_pdf(clean_title, clean_response)

    def export_to_pdf(self, title, summary):
        # Nome do arquivo PDF
        pdf_filename = f"{title.replace(' ', '_')}.pdf"

        # Cria um objeto PDF
        pdf = FPDF()
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.set_font("Arial", size=12)

        # Adiciona o título do vídeo
        pdf.cell(200, 10, title, ln=True, align="C")
        pdf.ln(10)  # Espaço em branco

        # Adiciona o resumo ao PDF
        pdf.multi_cell(0, 10, summary)

        # Salva o PDF
        pdf.output(pdf_filename)
        print(f"Resumo exportado para o arquivo PDF: {pdf_filename}")
