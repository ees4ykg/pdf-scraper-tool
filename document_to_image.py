import fitz
from PIL import Image
import io

def pdf_to_images(pdf_bytes):
    images = []
    try:
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        print(f"[LOG] Opened PDF with {len(doc)} pages")
    except Exception as e:
        print(f"[ERROR] Failed to open PDF: {e}")
        return []

    for i in range(len(doc)):
        try:
            page = doc[i]
            pix = page.get_pixmap(dpi=150)

            img_bytes = pix.tobytes("png")  # Safe across all versions
            image = Image.open(io.BytesIO(img_bytes))
            image.load()

            buffer = io.BytesIO()
            image.save(buffer, format="PNG")
            images.append(buffer.getvalue())
            print(f"[LOG] Page {i+1} converted to image, size: {image.size}")

        except Exception as e:
            print(f"[ERROR] Failed to process page {i+1}: {e}")

    doc.close()
    print(f"[LOG] Total images returned: {len(images)}")
    return images