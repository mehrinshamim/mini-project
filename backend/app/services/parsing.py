import io

from docling.datamodel.base_models import DocumentStream, InputFormat
from docling.datamodel.pipeline_options import PdfPipelineOptions
from docling.document_converter import DocumentConverter, PdfFormatOption


class ParsingService:
    _pipeline_options = PdfPipelineOptions()
    _pipeline_options.do_ocr = False

    _converter = DocumentConverter(
        format_options={
            InputFormat.PDF: PdfFormatOption(pipeline_options=_pipeline_options)
        }
    )

    @classmethod
    def parse(cls, pdf_bytes: bytes) -> str:
        """Convert PDF bytes to Markdown string via Docling (OCR disabled)."""
        stream = DocumentStream(name="resume.pdf", stream=io.BytesIO(pdf_bytes))
        result = cls._converter.convert(stream)
        return result.document.export_to_markdown()
