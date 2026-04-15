from app.rag.loader import PDFLoader

from pathlib import Path

path = Path("data/raw_pdf")
def main():
    res=dict()
    pdf=PDFLoader()
    for formation_dir in path.iterdir():
        if formation_dir.is_dir():
            
            
            for pdf_path in formation_dir.glob("*.pdf"):
           
                l=pdf.load_pdf(pdf_path,formation_dir)
           
            res[formation_dir.name]=l
    for i in res.items:
        print(i.keys())

if __name__ == "__main__":
    main()