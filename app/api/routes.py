from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.s3_service import S3Service
from app.services.textract_service import TextractService

import logging

router = APIRouter()
s3_service = S3Service()
textract_service = TextractService()

@router.post("/api/v1/invoice")
async def upload_invoice(file: UploadFile = File(...)):
    try:
        # Lê a imagem enviada
        image_bytes = await file.read()
        file_name = file.filename

        # Salva no INPUT_BUCKET
        s3_service.upload_file(image_bytes, file_name)

        # Processa a imagem com Textract
        csv_content = textract_service.process_and_convert(image_bytes)

        # Salva o CSV no OUTPUT_BUCKET
        csv_file_name = file_name.replace(".jpg", ".csv").replace(".png", ".csv")
        s3_service.upload_csv(csv_file_name, csv_content)

        return {"message": "Invoice processed successfully", "csv_file": csv_file_name}

    except Exception as e:
        logging.error(f"Erro no processamento: {e}")
        raise HTTPException(status_code=500, detail=f"Erro no processamento: {str(e)}")
