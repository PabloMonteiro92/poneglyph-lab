#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════╗
║     ☀️  RESTAURAÇÃO DO SUNNY — DESCRIPTOGRAFIA       ║
║          Project Poneglyph | Cybersecurity DIO       ║
╚══════════════════════════════════════════════════════╝

Reverte o ataque do Buster Call, recuperando os arquivos
criptografados usando a chave salva em 'log_pose.key'.

⚠️  AVISO: Script de uso EXCLUSIVAMENTE educacional.
"""

import os
from cryptography.fernet import Fernet

# ── Constantes ────────────────────────────────────────────────────────────────
KEY_FILE        = "log_pose.key"
RANSOM_NOTE     = "RESGATE_BERRIES.txt"
TARGET_EXT      = ".txt"
PROTECTED_FILES = {RANSOM_NOTE, "readme.txt", "README.md"}

# ── Funções ───────────────────────────────────────────────────────────────────

def carregar_log_pose() -> bytes | None:
    """Tenta carregar a chave de descriptografia."""
    try:
        with open(KEY_FILE, "rb") as kf:
            return kf.read()
    except FileNotFoundError:
        print(f"[!] ERRO CRÍTICO: '{KEY_FILE}' não encontrada!")
        print("[!] O Sunny está à deriva — sem a chave os dados estão perdidos.")
        return None


def restaurar_sistema_sunny(chave: bytes) -> int:
    """Descriptografa os arquivos afetados. Retorna o nº de arquivos restaurados."""
    fernet = Fernet(chave)

    alvos = [
        f for f in os.listdir(".")
        if f.endswith(TARGET_EXT) and f not in PROTECTED_FILES
    ]

    if not alvos:
        print("[*] Nenhum arquivo criptografado encontrado para restaurar.")
        return 0

    print(f"\n[*] {len(alvos)} arquivo(s) encontrado(s). Iniciando restauração...\n")
    sucessos = 0

    for arquivo in alvos:
        try:
            with open(arquivo, "rb") as f:
                dados_enc = f.read()
            dados_ori = fernet.decrypt(dados_enc)
            with open(arquivo, "wb") as f:
                f.write(dados_ori)
            print(f"  [V] SUPEEEER! '{arquivo}' restaurado com sucesso.")
            sucessos += 1
        except Exception:
            print(f"  [!] '{arquivo}' — chave inválida ou arquivo não estava criptografado.")

    return sucessos


def limpar_rastros_ataque() -> None:
    """Remove artefatos do ataque após restauração bem-sucedida."""
    artefatos = [RANSOM_NOTE, KEY_FILE]
    print("\n[*] Limpando o convés (removendo artefatos do ataque)...")

    for arq in artefatos:
        if os.path.exists(arq):
            try:
                os.remove(arq)
                print(f"  [*] '{arq}' jogado ao mar.")
            except Exception as e:
                print(f"  [!] Não foi possível remover '{arq}': {e}")


# ── Entry point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("=" * 56)
    print("  ☀️   MANUTENÇÃO DO SUNNY — INICIANDO...   ☀️")
    print("=" * 56)

    chave = carregar_log_pose()

    if chave:
        restaurados = restaurar_sistema_sunny(chave)
        if restaurados > 0:
            limpar_rastros_ataque()
            print(f"\n[*] {restaurados} arquivo(s) recuperado(s). O navio está pronto para zarpar! ⚓")
        else:
            print("\n[*] Nada a restaurar. Encerrando.")
    else:
        print("\n[!] Restauração abortada — Log Pose não encontrada.")
