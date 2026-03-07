from pathlib import Path
from bs4 import BeautifulSoup

# Step 1: HTML filings folder   
raw_folder = Path("data/raw")

# Step 2: HTML files
html_files = list(raw_folder.glob("*.html"))

print(f"Found {len(html_files)} HTML files.\n")

# Step 3: Function to extract and clean text from HTML
def extract_clean_text(file_path):
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        html_content = f.read()

    soup = BeautifulSoup(html_content, "lxml")

    # Remove noisy tags
    for tag in soup(["script", "style", "ix:header", "head", "title", "meta", "link"]):
        tag.decompose()

    # Remove hidden elements
    for hidden in soup.select('[style*="display:none"], [style*="display: none"]'):
        hidden.decompose()

    # Extract text
    text = soup.get_text(separator="\n")

    # Clean empty lines
    lines = [line.strip() for line in text.splitlines()]
    lines = [line for line in lines if line]

    clean_text = "\n".join(lines)
    return clean_text

# Step 4: Create a list to hold all processed filings
documents = []

# Step 5: Loop through each HTML file
for file_path in html_files:
    print("=" * 80)
    print(f"Processing: {file_path.name}")

    clean_text = extract_clean_text(file_path)

    # Parse filename to get company and year
    parts = file_path.stem.split("_")
    company = parts[0]
    year = parts[1]

    document = {
        "filename": file_path.name,
        "company": company,
        "year": year,
        "text": clean_text
    }

    documents.append(document)

    print(f"Company: {company}")
    print(f"Year: {year}")
    print(f"Characters extracted: {len(clean_text)}")
    print("Preview:")
    print(clean_text[:500])
    print("\n")

# Step 6: Final summary
print("=" * 80)
print(f"Finished processing {len(documents)} filings.")