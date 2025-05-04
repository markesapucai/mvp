from utils.ai_handler import generate_report
from utils.file_processor import read_excel
import os

def main():
    # 1. Lê planilha do usuário (ex: upload via frontend)
    data = read_excel("assets/examples/dados_agua.xlsx")
    
    # 2. Gera relatório com IA
    report = generate_report(data, "Impactos Hidrológicos")
    
    # 3. Salva em Word/PDF (TODO)
    print(report)  # Saída inicial para testes

if __name__ == "__main__":
    main()