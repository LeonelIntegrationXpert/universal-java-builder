# ⚙️ Universal Java & Maven Multi-Build Tool (v1.1)

<p align="center">
  <img src="https://capsule-render.vercel.app/api?type=waving&color=0:0C2340,100:00BFFF&height=200&section=header&text=JDK+%2B+Maven+Switcher&fontSize=38&fontColor=ffffff&animation=fadeIn" alt="Banner" />
</p>

<p align="center">
  <a href="https://adoptium.net/"> <img src="https://img.shields.io/badge/JDK-8%2C11%2C17%2C21-blue?logo=java" /></a>
  <a href="https://maven.apache.org/"> <img src="https://img.shields.io/badge/Maven-3.6.x--3.9.x-red?logo=apache-maven" /></a>
  <a href="#"> <img src="https://img.shields.io/badge/Script-Python%203.10+-yellow?logo=python" /></a>
</p>

---

## 📦 Visão Geral

Ferramenta interativa em Python que:

✅ Permite **escolher a versão do JDK (8/11/17/21)**  
✅ Permite **escolher a versão do Maven (3.6.3–3.9.6)**  
✅ **Baixa, extrai e configura** automaticamente o ambiente  
✅ Gera dinamicamente `MAVEN_OPTS` com `--add-opens` para JDK ≥ 17  
✅ Executa o build do seu projeto com `mvn clean install -DskipTests`  
✅ Gera **logs de compilação separados por data e versão**

Ideal para desenvolvedores que trabalham com múltiplas versões de Java, builds MuleSoft, projetos legados ou ambientes heterogêneos.

---

## 🧰 Funcionalidades

| Recurso                  | Detalhes                                                                 |
|--------------------------|--------------------------------------------------------------------------|
| 🗂 Seleção interativa     | Menu para escolha do JDK e Maven                                          |
| 📥 Download automático    | Baixa e extrai os binários (cache por zip)                               |
| 🔀 Compatibilidade       | Testado com JDKs da Temurin (Adoptium) e Maven Apache                    |
| 💻 Ajuste automático      | JAVA_HOME, M2_HOME e PATH são configurados dinamicamente                 |
| 🔐 Suporte a `--add-opens` | Para builds que dependem de reflexão com JDK 17+                         |
| 📜 Logs detalhados        | Criados automaticamente por build                                        |

---

## 📂 Estrutura do Projeto

```

.
├── tooling/
│   ├── jdks/          # JDKs baixados e extraídos
│   ├── mavens/        # Mavens baixados e extraídos
│   └── logs/          # Logs por build
├── execute\_java.py    # Script principal
└── README.md

````

---

## 🚀 Execução

1. Clone o repositório:
   ```bash
   git clone https://github.com/seuusuario/universal-java-maven-builder.git
   cd universal-java-maven-builder

2. Execute o script:

   ```bash
   python execute_java.py
   ```

3. Siga as instruções no terminal para:

   * Escolher a pasta do seu projeto (`pom.xml`)
   * Escolher o JDK
   * Escolher a versão do Maven

> ⚠️ É necessário ter Python 3.10+ instalado.

---

## ⚙️ Exemplo de Output

```
📁 Digite o caminho do projeto: C:\meu\projeto

Selecione o JDK:
  [1] 8    Temurin 8u412
  [2] 11   Temurin 11.0.21
  [3] 17   Temurin 17.0.11
  [4] 21   Temurin 21.0.3
👉 Número: 3

Selecione o Maven:
  [1] 3.6.3
  [2] 3.8.8
  [3] 3.9.5
  [4] 3.9.6
👉 Número: 4

✅ JAVA_HOME e MAVEN_HOME configurados
✅ mvn clean install -DskipTests
📑 Log salvo em tooling/logs/build_17_3.9.6_20250520_1530.log
```

---

## 📜 Requisitos

* Python 3.10+
* Permissão de escrita na pasta `tooling/`
* Conexão com a internet para baixar os binários na primeira execução

---

## 👨‍💼 Desenvolvedor Responsável

**Autor:** Leonel Dorneles Porto  
**Email:** [leoneldornelesporto@outlook.com.br](mailto:leoneldornelesporto@outlook.com.br)  
**Organização:** Accenture

---

<p align="center">
  <img src="https://readme-typing-svg.herokuapp.com?font=Fira+Code&size=20&pause=1000&color=00BFFF&center=true&vCenter=true&width=1000&lines=JDK+%2B+Maven+Builder+feito+com+💙+para+projetos+Java%2FMuleSoft!" alt="Typing SVG" />
</p>


---
