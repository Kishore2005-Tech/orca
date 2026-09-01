import express from 'express';
import path from 'path';
import { createServer as createViteServer } from 'vite';
import { executeOrcaPipeline } from './server/orchestrator.ts';
import { REGIONAL_PROFILES } from './server/marineDataEngine.ts';

const app = express();
const PORT = 3000;

app.use(express.json());

// API Routes FIRST

// Health check
app.get('/api/health', (req, res) => {
  res.json({
    status: 'ok',
    service: 'ORCA — Marine Ecosystems Reasoning Platform',
    version: '1.0.0',
    geminiConfigured: !!process.env.GEMINI_API_KEY
  });
});

// Dynamic Query Execution Endpoint
app.post('/api/orca/query', async (req, res) => {
  try {
    const { query, userMode = 'scientist', location, timeContext } = req.body;
    if (!query || typeof query !== 'string') {
      res.status(400).json({ error: 'Valid natural language query string is required.' });
      return;
    }

    const result = await executeOrcaPipeline(query, userMode, location, timeContext);
    res.json(result);
  } catch (error: any) {
    console.error('Error executing ORCA pipeline:', error);
    res.status(500).json({
      error: 'Failed to execute ORCA reasoning pipeline',
      message: error?.message || 'Internal reasoning engine error'
    });
  }
});

// List Calibrated Marine Datasets & Regional Boundaries
app.get('/api/marine/datasets', (req, res) => {
  res.json({
    regions: Object.values(REGIONAL_PROFILES).map(r => ({
      id: r.id,
      name: r.name,
      region: r.region,
      lat: r.lat,
      lon: r.lon,
      eezZone: r.eezZone,
      depthMeters: r.depthMeters,
      candidateZoneCount: r.candidateZones.length
    })),
    sensors: [
      { name: 'INSAT-3D TIR', agency: 'ISRO', parameter: 'Sea Surface Temperature (°C)', resolution: '4km' },
      { name: 'Oceansat-3 OCM-3', agency: 'ISRO / NRSC', parameter: 'Chlorophyll-a (mg/m³)', resolution: '360m' },
      { name: 'INCOIS SWAN', agency: 'MoES INCOIS', parameter: 'Significant Wave Height (m)', resolution: '3-hr Forecast' },
      { name: 'SAMUDRA Buoys', agency: 'NIOT', parameter: 'Real-time Wave & Met Observations', resolution: 'In-situ' }
    ]
  });
});

// Predefined Demo Scenarios from Master Specification
app.get('/api/scenarios', (req, res) => {
  res.json([
    {
      id: 'scenario-1',
      title: 'Physical Oceanography Query',
      query: 'What is the SST near Chennai?',
      expectedAgents: ['ocean', 'verification', 'coordinator'],
      category: 'Ocean State'
    },
    {
      id: 'scenario-2',
      title: 'Ecosystem Productivity Query',
      query: 'Why does this region have potentially favorable ecosystem conditions?',
      expectedAgents: ['ecosystem', 'ocean', 'knowledge', 'verification', 'coordinator'],
      category: 'Ecosystem'
    },
    {
      id: 'scenario-3',
      title: 'Full Mission: Fishing Zone & Safe Timing',
      query: 'Where is the most promising and safer fishing area near Chennai tomorrow morning?',
      expectedAgents: ['ocean', 'ecosystem', 'fisheries', 'safety', 'geospatial', 'knowledge', 'verification', 'coordinator'],
      category: 'Fisheries'
    },
    {
      id: 'scenario-4',
      title: 'Maritime Safety Assessment',
      query: 'Is it safe to go fishing tomorrow morning?',
      expectedAgents: ['safety', 'ocean', 'verification', 'coordinator'],
      category: 'Safety'
    },
    {
      id: 'scenario-5',
      title: 'Dynamic Route Planning',
      query: 'Find a promising fishing zone and calculate an outbound and return route.',
      expectedAgents: ['fisheries', 'safety', 'geospatial', 'ocean', 'verification', 'coordinator'],
      category: 'Navigation'
    },
    {
      id: 'scenario-6',
      title: 'Temporal Comparison',
      query: "Compare today's ocean conditions with yesterday.",
      expectedAgents: ['ocean', 'verification', 'coordinator'],
      category: 'Time Series'
    },
    {
      id: 'scenario-7',
      title: 'What-If Climate Scenario',
      query: 'What happens if SST increases by 1.5°C?',
      expectedAgents: ['ocean', 'ecosystem', 'fisheries', 'verification', 'coordinator'],
      category: 'Simulation'
    },
    {
      id: 'scenario-8',
      title: 'Alternative Geographic Sector (Arabian Sea)',
      query: 'Where should I fish tomorrow morning near Kochi and what is the sea state?',
      expectedAgents: ['ocean', 'ecosystem', 'fisheries', 'safety', 'geospatial', 'verification', 'coordinator'],
      category: 'Geographic Shift'
    }
  ]);
});

// Vite Middleware for dev / static for production
async function startServer() {
  if (process.env.NODE_ENV !== 'production') {
    const vite = await createViteServer({
      server: { middlewareMode: true },
      appType: 'spa'
    });
    app.use(vite.middlewares);
  } else {
    const distPath = path.join(process.cwd(), 'dist');
    app.use(express.static(distPath));
    app.get('*', (req, res) => {
      res.sendFile(path.join(distPath, 'index.html'));
    });
  }

  app.listen(PORT, '0.0.0.0', () => {
    console.log(`ORCA Marine Decision Platform running on http://0.0.0.0:${PORT}`);
  });
}

startServer();
