import os
from docling.document_converter import DocumentConverter
from pathlib import Path

def analyze_document(file_name):
    file_path = Path(f"data/{file_name}")
    if not file_path.exists():
        print(f"❌ Error: {file_name} is not found! No action was taken in vain.")
        return

    print(f"🚀 {file_name} being analyzed...")
    
    try:
        converter = DocumentConverter()
        
        result = converter.convert(str(file_path))
        
        markdown_output = result.document.export_to_markdown()

        output_file = Path("data/output_report.md")
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(markdown_output)
            
        print(f"✅ Analysis successful! Output saved as 'data/output_report.md'.")
        print("💡 Hint: You no longer need to reread this document; we'll continue using Markdown.")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    analyze_document("strategic_report_2026.pdf")