# Missiora Vue Frontend

A modern Vue 3 + Vite frontend for the Missiora Agency entrepreneurial platform.

## Quick Start

### Prerequisites
- Node.js 18+ 
- npm or yarn

### Development

1. **Install dependencies:**
   ```bash
   cd src/layer3_frameworks/vue_frontend
   npm install
   ```

2. **Start development server:**
   ```bash
   npm run dev
   ```
   
   This starts Vite dev server on `http://localhost:3000` with proxy to Flask API on port 5000.

3. **Build for production:**
   ```bash
   npm run build
   ```
   
   Builds the app to `dist/` directory.

### Integration with Flask

The Flask application serves the built Vue app from the `dist/` directory:

- **Production:** Flask serves `dist/index.html` for all non-API routes
- **Development:** Use Vite dev server with API proxy to Flask

### Project Structure

```
vue_frontend/
├── package.json          # Dependencies and scripts
├── vite.config.js        # Vite configuration
├── index.html           # HTML template
├── src/
│   ├── App.vue          # Main application component
│   ├── main.js          # Application entry point
│   ├── components/      # Vue components
│   │   ├── ChatWidget.vue
│   │   ├── IdentityCard.vue
│   │   ├── MissionCard.vue
│   │   └── RoadmapCard.vue
│   └── assets/          # Static assets
└── dist/               # Built application (generated)
```

## Features

- **Vue 3 Composition API:** Modern reactive framework
- **Tailwind CSS:** Utility-first styling via CDN
- **Responsive Design:** Mobile-first approach
- **API Integration:** Connects to Flask backend endpoints
- **Hot Module Replacement:** Fast development experience

## API Endpoints

The frontend communicates with these Flask API endpoints:

- `GET /api/auth/status` - Authentication status
- `POST /api/agent/interact` - AI agent conversations  
- `GET /api/identity` - Identity data
- `GET /api/mission` - Mission data
- `GET /api/roadmap` - Roadmap data
- `GET /api/milestones` - Milestone data

## Deployment

1. Build the Vue application:
   ```bash
   npm run build
   ```

2. Flask automatically serves the built files from `dist/`

3. Ensure Flask routing includes SPA fallback:
   ```python
   @app.route('/', defaults={'path': ''})
   @app.route('/<path:path>')
   def serve_spa(path):
       if path.startswith('api/'):
           abort(404)
       return send_from_directory(VUE_DIST, 'index.html')
   ```

## Development Notes

- Use `npm run dev` for development with hot reloading
- The Vite dev server proxies API calls to Flask on port 5000
- Tailwind CSS is loaded via CDN for simplicity
- All components use Vue 3 Composition API with `<script setup>`

## Browser Support

- Modern browsers with ES2015+ support
- Mobile Safari 10+
- Chrome 61+
- Firefox 60+
- Edge 79+