# 🐋 ORCA — Marine Ecosystems for Collaborative Agents

ORCA is an ocean intelligence platform that turns raw marine data (forecasts, buoy observations, satellite-derived layers) into **trustworthy, actionable advisories** for fishermen, coastal communities and marine researchers. A team of collaborating agents scores, cross-checks and explains each prediction, so users see not just *what* the model says but *how much to trust it*.

**Live demo:** [orca-official.vercel.app](https://orca-official.vercel.app/)

---

## ✨ Key Features

| Module | What it does |
|---|---|
| Advisory Reliability Score | Compares forecasts against buoy observations to score how reliable an advisory is. |
| Causal Hypothesis Engine | Proposes and ranks likely causes behind observed ocean conditions. |
| PFZ Scoring | Scores Potential Fishing Zones from environmental signals. |
| **Boat-Relative Safety Score | Converts sea state into a safety rating for a specific vessel. |
| **IMBL Boundary-Crossing Risk | Estimates the risk of drifting or navigating across the International Maritime Boundary Line. |
| **Anomaly Detection | Flags unusual readings in incoming ocean data. |

---

## 🏗️ Architecture

```
          ┌──────────────┐
          │   Frontend   │  dashboards, maps, advisories
          └──────┬───────┘
                 │ REST
          ┌──────▼───────┐
          │   Backend    │  API layer
          └──────┬───────┘
                 │
          ┌──────▼───────┐        ┌──────────┐
          │ Coordinator  │◄──────►│ Database │
          └──────┬───────┘        └──────────┘
        ┌────────┼────────┐
   ┌────▼───┐ ┌──▼─────┐ ┌▼───────┐
   │ Agent  │ │ Agent  │ │ Agent  │  reliability · PFZ · safety · IMBL · anomaly
   └────────┘ └────────┘ └────────┘
```

The **coordinator** routes each request to the relevant specialist **agents**, collects their outputs, and returns a combined, explainable result through the **backend** API to the **frontend**.

---

## 📁 Repository Structure

```
orca/
├── .agent/            # Agent configuration
├── .github/workflows/ # CI pipelines
├── agents/            # Specialist agents (scoring & prediction modules)
├── backend/           # API server
├── coordinator/       # Orchestration across agents
├── database/          # Schemas, migrations, seed data
├── docs/              # Documentation
├── frontend/          # Web UI
├── scripts/           # Utility & data scripts
├── tests/             # Test suite
├── .env.example       # Environment variable template
├── docker-compose.yml # Multi-service local setup
├── Makefile           # Common dev commands
├── package.json       # Frontend dependencies
├── pyproject.toml     # Python project config
└── requirements.txt   # Python dependencies
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- Node.js 18+
- Docker & Docker Compose (optional)

### 1. Clone

```bash
git clone https://github.com/Kishore2005-Tech/orca.git
cd orca
```

### 2. Configure environment

```bash
cp .env.example .env
# then fill in the required values
```

### 3. Run with Docker

```bash
docker compose up --build
```

### 4. Or run manually

```bash
# Backend & agents
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# Frontend
npm install
npm run dev
```

> Check the `Makefile` for shortcut commands (`make` targets) once populated.

---

## 🧪 Testing

```bash
pytest tests/
```

---

## 🗺️ Roadmap

- [ ] Real-time buoy and forecast ingestion
- [ ] Production-ready PFZ and IMBL models
- [ ] Multi-language advisories for coastal communities
- [ ] Mobile-friendly and offline-capable advisory view
- [ ] Public API documentation in `docs/`

---

## 🤝 Contributing

Contributions are welcome.

1. Fork the repo
2. Create a branch: `git checkout -b feature/your-feature`
3. Commit your changes: `git commit -m "Add your feature"`
4. Push and open a Pull Request

---

## 📄 License

Add a license file (e.g. MIT) and reference it here.

---

## 👤 Author

**Kishore P** — [@Kishore2005-Tech](https://github.com/Kishore2005-Tech)
