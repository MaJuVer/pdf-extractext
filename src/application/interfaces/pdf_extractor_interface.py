from abc import ABC, abstractmethod

class PDFExtractorInterface(ABC):
    @abstractmethod
    def extract_text(self, contenido_binario: bytes) -> str:
        pass