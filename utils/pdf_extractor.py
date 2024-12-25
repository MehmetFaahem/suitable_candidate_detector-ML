import PyPDF2

class PDFExtractor:
    @staticmethod
    def extract_text_from_pdf(pdf_path):
        """Extract text content from a PDF file."""
        try:
            with open(pdf_path, 'rb') as file:
                # Create PDF reader object
                pdf_reader = PyPDF2.PdfReader(file)
                
                # Extract text from all pages
                text = ""
                for page in pdf_reader.pages:
                    text += page.extract_text()
                
                return text.strip()
        except Exception as e:
            raise Exception(f"Error extracting PDF content: {str(e)}")