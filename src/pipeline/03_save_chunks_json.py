from pathlib import Path
from bs4 import BeautifulSoup
from langchain_text_splitters import RecursiveCharacterTextSplitter
import json

# Step 1: HTML filings folder
raw_folder = Path("data/raw")
processed_folder = Path("data/processed")

# Step 2: Create processed folder
processed_folder.mkdir(parents=True, exist_ok=True)

# Step 3: Find all HTML filings
html_files = list(raw_folder.glob("*.html"))
print(f"Found {len(html_files)} HTML files.\n")

# Step 4: Reusable text extraction function
def extract_clean_text(file_path):
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        html_content = f.read()

    soup = BeautifulSoup(html_content, "lxml")

    for tag in soup(["script", "style", "ix:header", "head", "title", "meta", "link"]):
        tag.decompose()

    for hidden in soup.select('[style*="display:none"], [style*="display: none"]'):
        hidden.decompose()

    text = soup.get_text(separator="\n")

    lines = [line.strip() for line in text.splitlines()]
    lines = [line for line in lines if line]

    clean_text = "\n".join(lines)
    return clean_text

# Step 5: Create the splitter
splitter = RecursiveCharacterTextSplitter(
    chunk_size=1500,
    chunk_overlap=200
)

# Step 6: Create the master chunk list
all_chunks = []

# Step 7: Process each filing
for file_path in html_files:
    print("=" * 80)
    print(f"Processing: {file_path.name}")

    clean_text = extract_clean_text(file_path)

    parts = file_path.stem.split("_")
    company = parts[0]
    year = parts[1]

    chunks = splitter.split_text(clean_text)

    print(f"Company: {company}")
    print(f"Year: {year}")
    print(f"Number of chunks: {len(chunks)}")

    for i, chunk_text in enumerate(chunks):
        chunk_record = {
            "filename": file_path.name,
            "company": company,
            "year": year,
            "chunk_id": f"{company}_{year}_chunk_{i+1}",
            "chunk_text": chunk_text
        }
        all_chunks.append(chunk_record)

# Step 8: Define output path
output_file = processed_folder / "chunked_filings.json"

# Step 9: Write chunk data to JSON
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(all_chunks, f, indent=2, ensure_ascii=False)

# Step 10: Final summary
print("\n" + "=" * 80)
print(f"Finished processing all filings.")
print(f"Total chunks created: {len(all_chunks)}")
print(f"Chunk data saved to: {output_file}")
