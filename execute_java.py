#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════════╗
║        🔧  UNIVERSAL JAVA & MAVEN MULTI-BUILD TOOL – v1.3 (2025)     ║
║                                                                      ║
║  • Escolha JDK (8/11/17/21…) + Maven (3.6.3–3.9.6)                   ║
║  • Escolha do projeto (digite caminho ou .)                          ║
║  • Downloads com cache em ./tooling/                                 ║
║  • Ajuste JAVA_HOME, M2_HOME, PATH, MAVEN_OPTS                       ║
║  • Build: mvn clean install -DskipTests + log                        ║
╚══════════════════════════════════════════════════════════════════════╝
"""

import os, sys, zipfile, subprocess, ctypes, re
from pathlib import Path
from datetime import datetime
from typing import Dict

try:
    import requests
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "requests"])
    import requests

# ── Diretórios internos ───────────────────────────────────────────────
ROOT_DIR  = Path("tooling")
JDK_DIR   = ROOT_DIR / "jdks"
MAVEN_DIR = ROOT_DIR / "mavens"
LOG_DIR   = ROOT_DIR / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

# ── Versões disponíveis ───────────────────────────────────────────────
JDKS: Dict[str, Dict[str, str]] = {
    "8":  {"desc": "Temurin 8u412",  "url": "https://github.com/adoptium/temurin8-binaries/releases/download/jdk8u412-b08/OpenJDK8U-jdk_x64_windows_hotspot_8u412b08.zip"},
    "11": {"desc": "Temurin 11.0.21","url": "https://github.com/adoptium/temurin11-binaries/releases/download/jdk-11.0.21%2B9/OpenJDK11U-jdk_x64_windows_hotspot_11.0.21_9.zip"},
    "17": {"desc": "Temurin 17.0.11","url": "https://github.com/adoptium/temurin17-binaries/releases/download/jdk-17.0.11%2B9/OpenJDK17U-jdk_x64_windows_hotspot_17.0.11_9.zip"},
    "21": {"desc": "Temurin 21.0.3", "url": "https://github.com/adoptium/temurin21-binaries/releases/download/jdk-21.0.3%2B9/OpenJDK21U-jdk_x64_windows_hotspot_21.0.3_9.zip"}
}

MAVENS: Dict[str, str] = {
    "3.6.3": "https://archive.apache.org/dist/maven/maven-3/3.6.3/binaries/apache-maven-3.6.3-bin.zip",
    "3.8.8": "https://archive.apache.org/dist/maven/maven-3/3.8.8/binaries/apache-maven-3.8.8-bin.zip",
    "3.9.5": "https://archive.apache.org/dist/maven/maven-3/3.9.5/binaries/apache-maven-3.9.5-bin.zip",
    "3.9.6": "https://archive.apache.org/dist/maven/maven-3/3.9.6/binaries/apache-maven-3.9.6-bin.zip"
}

ADD_OPENS_EXTRA = ["--add-opens java.base/java.nio=ALL-UNNAMED"]

# ── ANSI cores ────────────────────────────────────────────────────────
if os.name == "nt":
    ctypes.windll.kernel32.SetConsoleMode(ctypes.windll.kernel32.GetStdHandle(-11), 7)
C_RST, C_CYA, C_GRY, C_GRN, C_RED, C_YLW = "\033[0m", "\033[96m", "\033[90m", "\033[92m", "\033[91m", "\033[93m"

# ── Funções utilitárias ───────────────────────────────────────────────
def banner():
    print("\n" + "═"*70)
    print(f"{C_CYA}{'JAVA & MAVEN MULTI-BUILD TOOL'.center(70)}{C_RST}")
    print("═"*70 + "\n")

def ask_choice(options: Dict[str, object], title: str) -> str:
    while True:
        print(f"{C_YLW}{title}{C_RST}")
        print(f"  {C_RED}[0]{C_RST} Sair")
        for idx, key in enumerate(options, 1):
            desc = options[key].get("desc", "") if isinstance(options[key], dict) else ""
            print(f"  {C_CYA}[{idx}]{C_RST} {key:<6} {desc}")
        sel = input(f"{C_GRN}👉 Número: {C_RST}").strip()
        if sel == "0": sys.exit(0)
        if sel.isdigit() and 1 <= int(sel) <= len(options):
            return list(options.keys())[int(sel)-1]
        print(f"{C_RED}❌ Seleção inválida.\n{C_RST}")

def ask_project() -> Path:
    while True:
        p = input(f"{C_GRN}📁 Caminho do projeto (ou .): {C_RST}").strip()
        proj = Path(p or ".").expanduser().resolve()
        if proj.is_dir() and (proj / "pom.xml").exists():
            return proj
        print(f"{C_RED}❌ Pasta inválida ou sem pom.xml.{C_RST}")

def download_zip(url: str, dest: Path) -> Path:
    dest.mkdir(parents=True, exist_ok=True)
    zp = dest / url.split("/")[-1]
    if not zp.exists():
        print(f"{C_CYA}⬇️  Baixando {zp.name}{C_RST}")
        with requests.get(url, stream=True) as r, open(zp, "wb") as f:
            for chunk in r.iter_content(8192): f.write(chunk)
        print(f"{C_GRN}✔ Download concluído.{C_RST}")
    else:
        print(f"{C_GRY}📦 Cache: {zp.name}{C_RST}")
    return zp

def extract_zip(zp: Path, dest: Path) -> Path:
    print(f"{C_CYA}🗜️  Extraindo {zp.name}…{C_RST}")
    with zipfile.ZipFile(zp) as z:
        z.extractall(dest)
        dirs = {Path(n).parts[0] for n in z.namelist() if "/" in n}
    root = dest / sorted(dirs)[0] if dirs else next(dest.iterdir())
    print(f"{C_GRN}✔ Pasta: {root}{C_RST}")
    return root.resolve()

def prepare_tool(url: str, base: Path) -> Path:
    return extract_zip(download_zip(url, base), base)

def run_build(project: Path, jdk: Path, mvn: Path):
    env = os.environ.copy()
    env["JAVA_HOME"], env["M2_HOME"] = map(str, (jdk, mvn))
    env["PATH"] = f"{mvn/'bin'}{os.pathsep}{jdk/'bin'}{os.pathsep}{env['PATH']}"

    major_match = re.search(r"\d+", jdk.name)
    major = int(major_match.group()) if major_match else 0
    if major >= 17:
        opens = [
            "java.base/java.lang","java.base/java.util","java.base/java.io",
            "java.base/java.lang.reflect","java.base/java.util.regex",
            "java.base/java.net","java.xml/javax.xml.namespace"
        ] + [p.split(" ")[1] for p in ADD_OPENS_EXTRA]
        env["MAVEN_OPTS"] = " ".join(f"--add-opens {o}=ALL-UNNAMED" for o in opens)

    subprocess.run(["java", "-version"], env=env, shell=True)
    subprocess.run(["mvn", "-version"], env=env, shell=True)

    cmd = ["mvn", "clean", "install", "-DskipTests"]
    print(f"{C_YLW}🚀 {' '.join(cmd)}{C_RST}")
    res = subprocess.run(cmd, cwd=project, env=env, capture_output=True, text=True, shell=True)
    log_file = LOG_DIR / f"{project.name}_{jdk.name}_{mvn.name}_{datetime.now():%Y%m%d_%H%M%S}.log"
    log_file.write_text(res.stdout + res.stderr, encoding="utf-8")
    print(f"{C_GRY}📑 Log: {log_file}{C_RST}")

    if res.returncode == 0:
        print(f"{C_GRN}✅ Build OK!{C_RST}")
    else:
        print(f"{C_RED}❌ Build falhou (veja log).{C_RST}")
        print(res.stderr[-400:])

# ── EXECUÇÃO ──────────────────────────────────────────────────────────
if __name__ == "__main__":
    banner()
    project_path = ask_project()
    jdk_choice   = ask_choice(JDKS,   "Selecione o JDK:")
    mvn_choice   = ask_choice({k:{} for k in MAVENS}, "Selecione o Maven:")

    jdk_path  = prepare_tool(JDKS[jdk_choice]["url"], JDK_DIR)
    mvn_path  = prepare_tool(MAVENS[mvn_choice],      MAVEN_DIR)

    run_build(project_path, jdk_path, mvn_path)
