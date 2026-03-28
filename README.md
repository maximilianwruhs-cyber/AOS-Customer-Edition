# 🏛️ AOS — Agentic Operating System (Customer Edition)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Platform: Ubuntu](https://img.shields.io/badge/platform-Ubuntu%2024.04-E95420?logo=ubuntu&logoColor=white)](https://ubuntu.com/)
[![Part of: AgenticOS](https://img.shields.io/badge/ecosystem-AgenticOS-blue)](https://github.com/maximilianwruhs-cyber)

**The Plug-and-Play, Agentic-First Operating System for the Cloud-Edge Era.**

AOS is a sovereign artificial intelligence layer built for Ubuntu that treats large language models as its engine. It natively hot-swaps AI models in and out of GPU VRAM based on real-time task complexity and Intel RAPL energy telemetry (Intelligence per Watt).

## System Requirements

- **OS:** Ubuntu 24.04 LTS (fresh installation recommended)
- **RAM:** 8 GB minimum (16 GB recommended)
- **Disk:** 8 GB free space minimum
- **Internet:** Required for initial setup

## Quick Install

On a fresh **Ubuntu 24.04 LTS** machine, run:

```bash
curl -fsSL https://raw.githubusercontent.com/maximilianwruhs-cyber/AOS-Customer-Edition/master/deploy/bootstrap.sh | bash
```

<details>
<summary>Manual Installation (fallback)</summary>

```bash
sudo apt update && sudo apt install -y ansible git
git clone https://github.com/maximilianwruhs-cyber/AOS-Customer-Edition.git ~/AOS
cd ~/AOS
ansible-playbook deploy/ansible/install.yml --connection=local -K
```

</details>

## Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                    🖥️  VS Codium + Continue.dev              │
│                    (AI-Powered Code Editor)                   │
├──────────────────────────────────────────────────────────────┤
│                    🏛️  AOS Gateway (:8000)                   │
│              Reactive Inference Router + Triage              │
│         ┌──────────────┬──────────────────────┐              │
│         │ Energy Meter  │  Shadow Evaluator    │              │
│         │ (Intel RAPL)  │  (LLM-Judge)         │              │
│         └──────────────┴──────────────────────┘              │
├──────────────────────────────────────────────────────────────┤
│  🧠 LM Studio (:1234)  │  🦙 Ollama (:11434)               │
│  (Primary AI Engine)    │  (Embeddings + Fallback)            │
├──────────────────────────────────────────────────────────────┤
│  📚 RAG Pipeline        │  🗄️  pgvector (:5432)              │
│  LiteParse → Embed →    │  (Document Intelligence)            │
│  Query with Citations   │                                     │
└──────────────────────────────────────────────────────────────┘
```

## CLI Reference

After installation, the `aos` command is available system-wide:

| Command | Description |
|---|---|
| `aos health` | Check system status and service health |
| `aos ask "your prompt"` | Run inference through the gateway |
| `aos models` | List available models |
| `aos hosts` | List LLM backends |
| `aos switch <key>` | Switch active backend |
| `aos ingest <file>` | Ingest a document into the knowledge base |
| `aos query "question"` | Query your knowledge base with RAG |
| `aos bench` | Run model benchmarks |
| `aos leaderboard` | View model performance rankings |

## Document Ingestion

AOS includes a fully local RAG (Retrieval-Augmented Generation) pipeline. Ingest your documents and query them with AI — all on-device, zero cloud.

### Supported Formats

| Format | Requirement |
|---|---|
| `.pdf` | Native |
| `.doc`, `.docx`, `.ppt`, `.pptx`, `.xls`, `.xlsx`, `.odt`, `.rtf` | LibreOffice (auto-installed) |
| `.jpg`, `.png`, `.tiff`, `.svg` | ImageMagick (auto-installed) |

### Usage

```bash
# Ingest a document
aos ingest ~/Documents/report.pdf

# Query your knowledge base
aos query "What were the key findings in the Q4 report?"
```

## VS Codium Extension

The **AOS Intelligence Dashboard** extension provides:
- Real-time energy monitoring (Intel RAPL telemetry)
- Model benchmark results visualization
- LLM performance leaderboard
- System health overview in the sidebar

The extension is pre-installed during setup.

## Project Structure

```
AOS/
├── src/aos/                    # Python package
│   ├── gateway/                # FastAPI reactive inference router
│   ├── telemetry/              # Energy-aware benchmarking & evaluation
│   ├── tools/                  # Hardware telemetry, VRAM manager, watchdog
│   ├── cli.py                  # CLI interface
│   ├── config.py               # Centralized configuration
│   └── rag_engine.py           # Local RAG pipeline (LiteParse + pgvector)
├── config/                     # Runtime configuration files
├── deploy/                     # Deployment & provisioning
│   ├── ansible/                # Ansible playbooks
│   ├── extensions/             # Pre-built VS Codium extension
│   └── bootstrap.sh            # One-command setup script
├── data/                       # Runtime data (gitignored)
├── pyproject.toml              # Python package definition
├── docker-compose.yml          # pgvector database
└── requirements.txt            # Pinned dependencies
```

## Troubleshooting

### Services not running
```bash
# Check individual services
systemctl status aos-core
systemctl status lm-studio

# View logs
journalctl -u aos-core -f
journalctl -u lm-studio -f
```

### pgvector database issues
```bash
# Restart the container
docker compose up -d

# Check container status
docker ps | grep aos-pgvector
```

### LM Studio not responding
```bash
# Check if LM Studio is running
curl http://localhost:1234/v1/models

# Restart the service
sudo systemctl restart lm-studio
```

### Document ingestion fails
```bash
# Verify LiteParse is installed
which liteparse

# Verify Ollama embedding model is available
ollama list | grep nomic-embed-text

# If missing, pull it
ollama pull nomic-embed-text
```

---

## AgenticOS Ecosystem

| Project | Description |
|---------|-------------|
| [**AOS**](https://github.com/maximilianwruhs-cyber/AOS) | The flagship sovereign AI layer — core architecture & development |
| [**AOS Intelligence Dashboard**](https://github.com/maximilianwruhs-cyber/AOS-Intelligence-Dashboard) | VS Codium extension for real-time energy monitoring & LLM leaderboard |
| [**Obolus**](https://github.com/maximilianwruhs-cyber/Obolus) | Intelligence per Watt — benchmark which LLM is most efficient on your hardware |
| [**HSP**](https://github.com/maximilianwruhs-cyber/HSP) | Hardware Sonification Pipeline — turn machine telemetry into music |
| [**HSP VS Codium Extension**](https://github.com/maximilianwruhs-cyber/HSP-VS-Codium-Extension) | VS Codium sidebar for live HSP telemetry visualization |

## License

MIT License — see [LICENSE](LICENSE) for details.
