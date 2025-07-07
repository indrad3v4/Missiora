# Missiora Agency - Clean Architecture Implementation

## Overview

Missiora Agency is a mixed reality AI-powered platform designed for solopreneurs in Kraków, implementing Uncle Bob's Clean Architecture principles. The system features a mobile-first Tamagotchi-style interface with an evolving AI companion that helps users through identity definition, mission clarification, and roadmap generation.

## System Architecture

### 4-Layer Clean Architecture

The system strictly follows Clean Architecture with zero dependency violations:

```
src/
├── layer0_entities/        # Enterprise Business Rules
│   ├── identity.py         # Core identity data model
│   ├── mission.py          # Mission statements and goals
│   ├── roadmap.py          # Roadmap with milestones
│   └── user.py             # User account entity
├── layer1_use_cases/       # Application Business Rules
│   ├── agent_orchestrator.py    # AI agent coordination
│   ├── identity_analysis.py     # Identity processing
│   ├── mission_service.py       # Mission validation
│   └── roadmap_generator.py     # Roadmap creation
├── layer2_interfaces/      # Interface Adapters
│   ├── controllers/        # REST API endpoints
│   ├── gateways/           # External service interfaces
│   └── presenters/         # UI data formatting
└── layer3_frameworks/      # Frameworks & Drivers
    ├── flask_app/          # Flask WSGI application
    ├── gradio_app/         # Computer vision tools
    └── vue_frontend/       # Vue.js SPA
```

### Technology Stack

- **Backend**: Python Flask with SQLAlchemy ORM
- **Frontend**: Vue 3 with Composition API and Pinia state management
- **AI**: OpenAI GPT-4o with specialized agent orchestration
- **Computer Vision**: Gradio-based CV tools with HuggingFace transformers
- **Database**: SQLite with optional PostgreSQL support
- **Authentication**: Flask-Login with OAuth2 integration

## Key Components

### Agent Orchestration System

The system implements specialized AI agents following the practical guide patterns:

1. **Strategy Agent**: Business strategy for Kraków-based solopreneurs
2. **Creative Agent**: Brand and messaging optimization
3. **Production Agent**: Technical implementation guidance
4. **Media Agent**: Content creation and marketing

Each agent uses the GPT-4o model with specialized prompts and follows a structured response format.

### Mixed Reality Interface

The frontend features a mobile-first (1080×1920px) design with:

- **Tamagotchi Avatar**: Animated AI companion with evolution stages
- **Camera Integration**: Real-time video feed with AR overlays
- **Glassmorphism UI**: Translucent panels with backdrop blur
- **Progressive Disclosure**: Identity → Mission → Roadmap unlock flow

### Computer Vision Pipeline

Integrated CV capabilities include:

- **Object Detection**: Real-time business-relevant object recognition
- **Image Captioning**: Contextual scene analysis
- **AR Overlays**: Floating labels and action menus
- **Business Card Recognition**: Contact extraction and networking suggestions

## Data Flow

1. **User Input**: Identity, mission, or roadmap data via Vue frontend
2. **API Layer**: Flask controllers validate and route requests
3. **Use Cases**: Business logic processes data through appropriate services
4. **Entities**: Core domain objects maintain business rules
5. **Gateways**: External services (OpenAI, CV models) provide analysis
6. **Presenters**: Format responses for optimal UI consumption

### API Endpoints

- `GET/POST /api/identity` - Identity management
- `GET/POST /api/mission` - Mission statement handling
- `GET/POST /api/roadmap` - Roadmap and milestone tracking
- `POST /api/agent/interact` - AI agent communication
- `POST /api/cv/analyse` - Computer vision analysis
- `GET /api/auth/status` - Authentication status

## External Dependencies

### Core Dependencies

- **OpenAI API**: GPT-4o for agent responses and analysis
- **HuggingFace Transformers**: Lightweight CV models
- **Flask Ecosystem**: Web framework with extensions
- **Vue 3**: Frontend framework with CDN delivery

### Optional Dependencies

- **PostgreSQL**: Production database (fallback to SQLite)
- **Replit OAuth**: Authentication integration
- **Gradio**: Computer vision interface
- **Web3**: Blockchain integration for payments

## Deployment Strategy

### Development Mode

```bash
python main.py  # Flask server on port 5000
# Vue development via CDN - no build required
```

### Production Deployment

The system is optimized for Replit deployment with:

- **Single Process**: Flask serves both API and static files
- **Lightweight Models**: <100MB CV models with on-demand loading
- **CDN Assets**: Vue.js delivered via CDN to minimize bundle size
- **Graceful Degradation**: Fallbacks for missing dependencies

### Size Optimization

- **Disk Usage**: Successfully reduced from 6.2GB to <1GB
- **No Build Dependencies**: Vue development uses CDN
- **Mock Implementations**: Graceful fallbacks for optional features
- **Smart Caching**: Session data persisted in JSON files

## Changelog

- July 07, 2025. Initial setup

## User Preferences

Preferred communication style: Simple, everyday language.