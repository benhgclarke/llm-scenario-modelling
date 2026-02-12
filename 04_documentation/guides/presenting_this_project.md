# Documentation

## System Architecture

This project is structured around four independent deliverables that work together through a shared utilities layer.

**Project Structure:**
- **Deliverable 1: Scenario Modeling** (`01_scenario_modeling/`) — Generates multiple possible business futures using Monte Carlo simulation
- **Deliverable 2: Insight Extraction** (`02_insight_extraction/`) — Analyses operational data and surfaces key performance trends
- **Deliverable 3: Strategic Dashboard** (`03_strategic_dashboard/`) — Real-time view of business metrics and KPIs
- **Deliverable 4: Documentation** (`04_documentation/`) — Complete guides, architecture docs, and presentation materials

**Shared Utilities** (`shared/`):
- `data_generation/` — Synthetic data creation and scenario generation
- `utils/` — Processing, plotting, and LLM client integration
- `config/` — Configuration management (YAML-based settings)

**Why This Architecture?**
Each deliverable is self-contained with its own notebooks, source code, and data directories. Shared utilities eliminate duplication while keeping concerns separated. This makes the system modular, testable, and extensible. Notebooks serve as living documentation that actually executes, showing both methodology and results in one place.

**Technology Stack:**
- Python 3.x with pandas, NumPy for data manipulation
- Plotly Express for interactive visualisation
- Monte Carlo simulation for uncertainty quantification
- Claude API (Anthropic) for AI-powered insights
- Streamlit for web interface
- PyYAML for configuration

---

## AI Integration Guide

The Claude API enhances this system by translating quantitative analysis into business-friendly insights.

**How It Works:**
The AI integration is an optional enhancement layer. The system generates all charts, statistics, and scenarios without it. When enabled, Claude API processes the generated data and explains what it means in strategic business terms.

**Configuration:**
1. Create a `.env` file in the project root
2. Add your Anthropic API key: `ANTHROPIC_API_KEY=sk-...`
3. The system will automatically use it when available

**Prompt Engineering Approach:**
- Structured, numbered prompts for consistent output
- CSV data passed as context to keep AI grounded in real numbers
- Role-specific system prompts for different analysis types (financial, operational, risk)
- Clear instructions about format and tone expectations

**Graceful Degradation:**
If no API key is provided, the app displays helpful setup instructions. All statistical visualisations and analysis continue to work. This ensures the system never breaks due to missing credentials.

**What You Can Extend:**
- Modify system prompts in `shared/utils/llm_client.py` to change AI tone or focus
- Add new analysis types by creating additional prompt configurations
- Integrate different LLM providers (Claude, GPT, Cohere, etc.) by extending the client interface
- Add structured output validation to ensure consistency

---

## Quick Start Guide

Get the system running in five minutes.

**Prerequisites:**
- Python 3.8+
- pip or conda

**Installation Steps:**

1. **Clone or download the project**
   ```bash
   cd llm-scenario-modelling-main
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Streamlit app**
   ```bash
   streamlit run streamlit_app.py
   ```
   The app opens automatically in your browser at `http://localhost:8501`

4. **(Optional) Set up AI insights**
   - Copy `.env.example` to `.env`
   - Add your Anthropic API key
   - Restart the app to enable "Get AI Insights" button

**First Steps:**
- Navigate through all 4 deliverables using the sidebar selector
- Interact with charts (hover for details, scroll for trends)
- Review the data visualisations and explanations
- Click "Get AI Insights" to see Claude's analysis (if API key is configured)

**Jupyter Notebooks:**
To explore the methodology in detail, open the notebooks in each deliverable folder:
- `01_scenario_modeling/notebooks/01_scenario_modeling_walkthrough.ipynb`
- `02_insight_extraction/notebooks/02_insight_extraction_walkthrough.ipynb`
- `03_strategic_dashboard/notebooks/03_dashboard_walkthrough.ipynb`
- `notebooks/00_project_overview.ipynb`

---

## Presentation Guide

Tips and talking points for presenting this project to stakeholders, investors, or interviewers.

**Recommended Walkthrough (13 minutes total):**

1. **Start with the Big Picture (2 min)**
   - Show the 4 deliverables and explain the flow
   - Mention the tech stack and why it matters for scalability
   - Frame it as: "Combining data science with AI to turn numbers into decisions"

2. **Scenario Modeling Demo (5 min)**
   - Show how multiple possible futures are generated
   - Explain the uncertainty bands ("best case, worst case, likely case")
   - Highlight the 200 Monte Carlo simulations and what they represent
   - Key talking point: "This isn't prediction—it's preparation"

3. **Insight Extraction Demo (3 min)**
   - Show the performance heatmap (which facilities perform best/worst)
   - Show the radar chart (multi-dimensional performance)
   - Explain how AI summarises this into actionable recommendations

4. **Dashboard & AI Insights (3 min)**
   - Show the KPI metrics and facility comparison
   - Click "Get AI Insights" live (if configured)
   - Highlight the real-time decision support aspect

**Talking Points for Questions:**

**"Why this approach?"**
- Uncertainty quantification helps leaders prepare for multiple outcomes, not just plan for one
- AI augments human analysis (doesn't replace it)—charts and statistics are the facts, AI provides interpretation
- Modular architecture means each component can evolve independently

**"How is the AI adding value?"**
- Statistical analysis identifies patterns; Claude translates them into business strategy
- Monte Carlo gives you probability distributions; AI explains what to do with them
- The system works without AI—Claude is truly an enhancement layer, not a dependency

**"What would you do next?"**
- Connect to live operational data (databases, ERP systems)
- Automated alerting when risk scores spike or anomalies appear
- Feedback loops to track whether AI recommendations actually drive better outcomes
- Advanced forecasting (ARIMA, Prophet) for longer-term planning

**"How did you approach the engineering?"**
- Separation of concerns—shared utilities support independent deliverables
- Configuration-driven (YAML files) so non-technical users can customise parameters
- Notebooks as documentation—code that demonstrates itself
- Graceful degradation when external APIs are unavailable

---

## Extension Guide

How to build on top of this system and integrate new capabilities.

**Adding New Data Sources:**

1. Modify `shared/data_generation/generate.py` to accept data from databases or APIs
2. Replace the synthetic data generation with real data loading
3. The rest of the pipeline (analysis, visualisation, AI insights) remains unchanged

**Creating New Visualisations:**

1. Add new functions to `shared/utils/plotting.py` following the existing pattern
2. Call them from the appropriate deliverable function
3. Use consistent colour schemes from `SCENARIO_COLORS` dict

**Extending AI Analysis:**

1. Edit `shared/utils/llm_client.py` to add new analysis types
2. Create role-specific prompts for different business functions (finance, operations, HR, etc.)
3. Implement output parsing to validate AI responses

**Adding More Deliverables:**

1. Create a new folder: `05_new_deliverable/`
2. Follow the existing structure: `src/`, `notebooks/`, `data/`
3. Add a new function `show_new_deliverable()` in `streamlit_app.py`
4. Register it in the `DELIVERABLE_VIEWS` router

**Deploying to Production:**

1. Replace synthetic data with live data sources
2. Secure your API keys (use environment variables, secrets managers)
3. Set up logging and error monitoring
4. Deploy Streamlit using Streamlit Cloud, Docker, or Kubernetes
5. Configure scheduled jobs for data refresh and analysis updates

**Scaling Tips:**

- Cache expensive computations with `@st.cache_data` decorator
- Use appropriate plot types for large datasets (heatmaps instead of scatter for >10k points)
- Implement data pagination for large result sets
- Consider databases (PostgreSQL, MongoDB) instead of CSV/synthetic data for production
