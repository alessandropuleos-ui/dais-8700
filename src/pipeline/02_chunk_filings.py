from pathlib import Path
from bs4 import BeautifulSoup
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Step 1: HTML filings folder 
raw_folder = Path("data/raw")
html_files = list(raw_folder.glob("*.html"))

print(f"Found {len(html_files)} HTML files.\n")

# Step 2: Reusable function to extract and clean text from HTML
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

# Step 3: Create the text splitter
splitter = RecursiveCharacterTextSplitter(
    chunk_size=1500,
    chunk_overlap=200
)

# Step 4: Store all chunk records here
all_chunks = []

# Step 5: Loop through each filing
for file_path in html_files:
    print("=" * 80)
    print(f"Processing: {file_path.name}")

    clean_text = extract_clean_text(file_path)

    parts = file_path.stem.split("_")
    company = parts[0]
    year = parts[1]

    # Step 6: Split one filing into chunks
    chunks = splitter.split_text(clean_text)

    print(f"Company: {company}")
    print(f"Year: {year}")
    print(f"Number of chunks: {len(chunks)}")

    # Step 7: Create one record per chunk
    for i, chunk_text in enumerate(chunks):
        chunk_record = {
            "filename": file_path.name,
            "company": company,
            "year": year,
            "chunk_id": f"{company}_{year}_chunk_{i+1}",
            "chunk_text": chunk_text
        }
        all_chunks.append(chunk_record)

    print("First chunk preview:")
    print(chunks[0][:500])
    print("\n")

print("=" * 80)
print(f"Finished chunking all filings.")
print(f"Total chunks created: {len(all_chunks)}")