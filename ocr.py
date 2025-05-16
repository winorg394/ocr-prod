import os
import easyocr
from PIL import Image
import fitz  # PyMuPDF
from openai import OpenAI
import tempfile
from dotenv import load_dotenv  # Add this import at the top

def extract_text_from_image(image_path):
    """
    Extract text from an image using EasyOCR
    
    Args:
        image_path (str): Path to the image file
        
    Returns:
        str: Extracted text from the image
    """
    try:
        reader = easyocr.Reader(['fr'])  # Specify French language
        result = reader.readtext(image_path, detail=0)
        text = "\n".join(result)
        return text
    except Exception as e:
        print(f"Error extracting text from image: {e}")
        return ""

def convert_image_to_pdf(image_path):
    """
    Convert an image to PDF format
    
    Args:
        image_path (str): Path to the image file
        
    Returns:
        str: Path to the converted PDF file
    """
    try:
        # Create a temporary file for the PDF
        temp_pdf = tempfile.NamedTemporaryFile(suffix='.pdf', delete=False)
        temp_pdf_path = temp_pdf.name
        temp_pdf.close()
        
        # Open the image and convert to PDF
        image = Image.open(image_path)
        # Convert to RGB if image is in RGBA mode (e.g., PNG with transparency)
        if image.mode == 'RGBA':
            image = image.convert('RGB')
        image.save(temp_pdf_path, 'PDF', resolution=100.0)
        
        print(f"Image converted to PDF: {temp_pdf_path}")
        return temp_pdf_path
    except Exception as e:
        print(f"Error converting image to PDF: {e}")
        return None

def extract_text_from_pdf(pdf_path):
    """
    Extract text from a PDF file using PyMuPDF
    
    Args:
        pdf_path (str): Path to the PDF file
        
    Returns:
        str: Extracted text from the PDF
    """
    try:
        doc = fitz.open(pdf_path)
        text = ""
        for page in doc:
            text += page.get_text()
        return text
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
        return ""

def process_text(text, model):
    """
    Process extracted text with the OpenAI model
    """
    load_dotenv()  # Load environment variables
    
    client = OpenAI(
        base_url=os.getenv('OPENROUTER_BASE_URL', 'https://models.github.ai/inference'),
        api_key=os.getenv('OPENROUTER_API_KEY'),
    )
    
    # System prompts to guide the model
    system_prompts = [
        "You are an expert system specialized in extracting information from flight tickets.",
        "Extract all relevant information from the flight ticket text provided.",
        "Return the information in a well-structured JSON format.",
        "Include the following fields if available: airline, flight_number, passenger_name, departure_airport, arrival_airport, departure_date, departure_time, arrival_date, arrival_time, seat_number, booking_reference, ticket_number, fare_class, baggage_allowance.",
        "If a field is not visible or not present in the ticket, set its value to null.",
        "Do not include any explanations or notes in your response, only the JSON object.",
        "Ensure all dates are in YYYY-MM-DD format and times are in 24-hour format (HH:MM).",
        "Use IATA codes for airports when available (e.g., JFK, LAX).",
        "If you detect multiple flight segments, include them as an array under 'segments'."
    ]
    
    completion = client.chat.completions.create(
        extra_headers={
            # Optional headers for OpenRouter rankings
            # "HTTP-Referer": "your-site-url",
            # "X-Title": "Flight Ticket OCR System",
        },
        model=model,
        messages=[
            {
                "role": "system",
                "content": "\n".join(system_prompts)
            },
            {
                "role": "user",
                "content": f"Extract all information from this flight ticket text and return it as a JSON object:\n\n{text}"
            }
        ],
        response_format={"type": "json_object"}
    )
    
    # Return the raw JSON content without any additional formatting
    return completion.choices[0].message.content

def process_file(file_path, model="deepseek/deepseek-chat-v3-0324:free"):
    """
    Process a file (image or PDF) and extract information
    
    Args:
        file_path (str): Path to the file
        model (str): Model to use for processing
        
    Returns:
        str: JSON response with extracted information
    """
    file_extension = os.path.splitext(file_path)[1].lower()
    temp_pdf_path = None
    
    try:
        if file_extension in ['.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.tif']:
            # Convert image to PDF first
            temp_pdf_path = convert_image_to_pdf(file_path)
            if temp_pdf_path:
                # Extract text from the converted PDF
                text = extract_text_from_pdf(temp_pdf_path)
                # If no text was extracted from PDF, try direct image OCR as fallback
                if not text:
                    print("No text extracted from PDF, trying direct image OCR...")
                    text = extract_text_from_image(file_path)
            else:
                # If conversion failed, use direct image OCR
                text = extract_text_from_image(file_path)
        elif file_extension == '.pdf':
            text = extract_text_from_pdf(file_path)
        else:
            return f"Unsupported file format: {file_extension}"
        
        if not text:
            return "No text was extracted from the file"
        
        return process_text(text, model)
    finally:
        # Clean up temporary PDF file if it was created
        if temp_pdf_path and os.path.exists(temp_pdf_path):
            try:
                os.unlink(temp_pdf_path)
            except Exception as e:
                print(f"Error removing temporary PDF file: {e}")

# Remove the process_base64 function since we're not using base64 anymore

if __name__ == "__main__":
    # Example usage
    import sys
    
    if len(sys.argv) < 2:
        # Use Billet.pdf as the default file path
        file_path = "Billet.pdf"
        print(f"No file path provided, using default: {file_path}")
    else:
        file_path = sys.argv[1]
    
    model = sys.argv[2] if len(sys.argv) > 2 else "deepseek/deepseek-chat-v3-0324:free"
    
    result = process_file(file_path, model)
    print(result)