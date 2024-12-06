import os
import sys
from pathlib import Path
import shutil
import subprocess

# -----------------------------------------------
# Nome do Script: processar_imagens.py
# Descrição: Renomeia, redimensiona, aplica marca d'água e organiza imagens
# Autor: Nome do Autor
# Data: 2024-10-10
# Versão: 1.1
#
# Uso: python processar_imagens.py [diretório]
#
# Dependências: ImageMagick (mogrify, convert)
# -----------------------------------------------

def verificar_dependencia(comando):
    """Verifica se um comando está disponível no sistema."""
    if shutil.which(comando) is None:
        print(f"O comando '{comando}' não está instalado. Instale o ImageMagick.")
        sys.exit(1)

def criar_pasta(diretorio):
    """Cria um diretório se ele não existir."""
    Path(diretorio).mkdir(parents=True, exist_ok=True)

def renomear_arquivos(pasta):
    """Renomeia os arquivos de imagem para um formato padronizado."""
    original_dir = Path(pasta) / "original"
    criar_pasta(original_dir)
    contador = 1

    for arquivo in Path(pasta).iterdir():
        if arquivo.is_file():
            extensao = arquivo.suffix.lower()
            if extensao in [".jpg", ".jpeg", ".png", ".webp", ".heic"]:
                novo_nome = original_dir / f"{Path(pasta).name} {contador:03d}{extensao}"
                while novo_nome.exists():
                    contador += 1
                    novo_nome = original_dir / f"{Path(pasta).name} {contador:03d}{extensao}"
                arquivo.rename(novo_nome)
                contador += 1

def redimensionar_e_converter(pasta):
    """Redimensiona e converte imagens HEIC para JPG."""
    original_dir = Path(pasta) / "original"
    arquivos = list(original_dir.glob("*.*"))
    if arquivos:
        comando = [
            "mogrify",
            "-resize", "1500x1500",
            "-quality", "80",
            "-format", "jpg"
        ] + [str(arquivo) for arquivo in arquivos]
        subprocess.run(comando, check=True)
        
        # Remove arquivos HEIC, JPEG e WEBP após a conversão
        for extensao in [".heic", ".jpeg", ".webp"]:
            for arquivo in original_dir.glob(f"*{extensao}"):
                arquivo.unlink()

def aplicar_marca_dagua(pasta, marca_dagua):
    """Aplica uma marca d'água em todas as imagens JPG."""
    original_dir = Path(pasta) / "original"
    if not Path(marca_dagua).is_file():
        print(f"Arquivo de marca d'água não encontrado: {marca_dagua}")
        sys.exit(1)

    for imagem in original_dir.glob("*.jpg"):
        output_path = Path(pasta) / imagem.name
        comando = [
            "convert",
            str(imagem),
            str(marca_dagua),
            "-gravity", "South",
            "-geometry", "+0+25",
            "-composite",
            str(output_path)
        ]
        resultado = subprocess.run(comando)
        if resultado.returncode == 0:
            print(f"Marca d'água aplicada com sucesso em {imagem.name}")
        else:
            print(f"Erro ao aplicar marca d'água em {imagem.name}")

def main():
    # Diretório passado como argumento
    pasta = sys.argv[1] if len(sys.argv) > 1 else os.getcwd()
    pasta = Path(pasta).resolve()

    # Dependências necessárias
    verificar_dependencia("mogrify")
    verificar_dependencia("convert")

    # Processamento
    print("Renomeando arquivos...")
    renomear_arquivos(pasta)
    
    print("Redimensionando e convertendo arquivos...")
    redimensionar_e_converter(pasta)
    
    marca_dagua = "/home/rodrigo/LC Imobiliária/md250.jpg"
    print("Aplicando marca d'água...")
    aplicar_marca_dagua(pasta, marca_dagua)

    print("Processamento concluído.")

if __name__ == "__main__":
    main()
