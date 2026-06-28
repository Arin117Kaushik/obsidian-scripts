import fitz
import pytesseract
from PIL import Image
import io
import os
from tkinter import filedialog, Tk

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
os.environ["TESSDATA_PREFIX"] = r"C:\Users\Arin\tessdata"

# Open file picker dialog
root = Tk()
root.withdraw()  # Hide the root window
PDF_PATH = filedialog.askopenfilename(
    title="Select PDF file to extract text from",
    filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")]
)
root.destroy()

if not PDF_PATH:
    print("No file selected. Exiting...")
    exit()

# Generate output path from input path
base_name = os.path.splitext(os.path.basename(PDF_PATH))[0]
out_dir = os.path.dirname(PDF_PATH)
OUT_PATH = os.path.join(out_dir, f"{base_name}_extracted.txt")

doc = fitz.open(PDF_PATH)
total = len(doc)
print(f"Total pages: {total}")

all_text = []

for i, page in enumerate(doc):
    print(f"Processing page {i+1}/{total}...", end="\r")
    # Render page at 300 DPI for good OCR accuracy
    mat = fitz.Matrix(300/72, 300/72)
    pix = page.get_pixmap(matrix=mat, colorspace=fitz.csRGB)
    img_data = pix.tobytes("png")
    img = Image.open(io.BytesIO(img_data))
    text = pytesseract.image_to_string(img, lang="hin", config="--psm 3")
    all_text.append(f"--- Page {i+1} ---\n{text.strip()}")

doc.close()

final_text = "\n\n".join(all_text)
with open(OUT_PATH, "w", encoding="utf-8") as f:
    f.write(final_text)

print(f"\nDone. Saved to: {OUT_PATH}")
print(f"Total characters extracted: {len(final_text)}")
