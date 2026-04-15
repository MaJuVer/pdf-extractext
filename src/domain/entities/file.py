# src/domain/entities/file.py
class File:
    def __init__(self, name: str, content: bytes):
        self.name = name
        self.content = content

    def is_pdf(self) -> bool:
        return self.name.endswith(".pdf")

    def size(self) -> int:
        return len(self.content)