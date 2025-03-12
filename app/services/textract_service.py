import boto3
import csv
import io
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class TextractService:
    def __init__(self):
        self.textract_client = boto3.client('textract')

    def process_image(self, image_bytes):
        """
        Processa uma imagem com o AWS Textract e retorna o conteúdo extraído.
        """
        try:
            response = self.textract_client.detect_document_text(Document={'Bytes': image_bytes})
            return response
        except Exception as e:
            logger.error(f"Erro ao processar imagem com Textract: {e}")
            raise

    def extract_text_to_csv(self, textract_response):
        """
        Converte a resposta do Textract para formato CSV.
        """
        extracted_data = [["BlockType", "Text", "Confidence", "Left", "Top", "Width", "Height"]]
        
        for item in textract_response.get('Blocks', []):
            if 'Text' in item:
                extracted_data.append([
                    item['BlockType'],
                    item['Text'],
                    item.get('Confidence', ''),
                    item.get('Geometry', {}).get('BoundingBox', {}).get('Left', ''),
                    item.get('Geometry', {}).get('BoundingBox', {}).get('Top', ''),
                    item.get('Geometry', {}).get('BoundingBox', {}).get('Width', ''),
                    item.get('Geometry', {}).get('BoundingBox', {}).get('Height', '')
                ])
        
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerows(extracted_data)
        return output.getvalue()

    def process_and_convert(self, image_bytes):
        """
        Processa uma imagem e retorna os dados extraídos em formato CSV.
        """
        textract_response = self.process_image(image_bytes)
        return self.extract_text_to_csv(textract_response)
