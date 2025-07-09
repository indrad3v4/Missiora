# replit.md

## Overview

MISSIORA is an AI-powered platform for solopreneurs that combines traditional Flask web application architecture with cutting-edge Mixed Reality (MR) features. The application provides an evolving AI Tamagotchi companion that helps users unify their personal identity with professional growth through three core modules: Identity, Mission, and Roadmap.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture
- **Framework**: Vue 3 with component-based architecture
- **MR Experience**: WebGL-powered Three.js rendering for 3D Tamagotchi agent
- **Mobile-First Design**: 1080×1920px optimized for mobile devices
- **Styling**: Glassmorphism UI with CSS backdrop filters and translucent panels
- **Camera Integration**: getUserMedia() API for AR background with fallback gradients

### Backend Architecture
- **Framework**: Flask 3.11 with Blueprint-based routing
- **Database**: SQLAlchemy with SQLite (configurable for PostgreSQL)
- **Authentication**: Multi-modal support (traditional, MetaMask Web3, Replit OAuth)
- **AI Integration**: OpenAI GPT-4o with specialized agent orchestration
- **Vision Processing**: OpenAI CLIP model for real-time object detection

### Database Schema
- **Users**: Identity data, mission statements, profile information
- **Conversations**: Chat history and agent interactions
- **Milestones**: Progress tracking and roadmap management
- **Messages**: Agent communication logs
- **UserGoals/UserInsights**: Personal development tracking

## Key Components

### 1. Agent Orchestration System
- **Model Selection**: GPT-4o for complex reasoning, smaller models for classification
- **Tool Categories**: Data retrieval, Action execution, Agent orchestration
- **Specialized Agents**: Strategy, Creative, and Mission-focused sub-agents
- **Personality System**: Mood animations and contextual responses

### 2. Tamagotchi Agent Evolution
- **Four Growth Stages**: Seed (0-25%) → Sprout (26-50%) → Bloom (51-80%) → Master (81-100%)
- **Completion Metrics**: Identity (33%), Mission (33%), Roadmap (34%)
- **Visual Evolution**: Size, color, and animation changes based on progress
- **Eye Tracking**: Agent eyes follow detected objects for enhanced interaction

### 3. CLIP Vision Integration
- **Real-time Analysis**: Camera captures frames every 2 seconds
- **Object Recognition**: Business cards, QR codes, whiteboards, people, tech equipment
- **AR Overlays**: Bounding boxes, labels, and contextual action menus
- **Actionable Intelligence**: Extract contacts, decode QR codes, OCR text, networking advice

### 4. Progressive Disclosure System
- **Identity Completion**: Unlocks Mission module at 80% threshold
- **Mission Completion**: Unlocks Roadmap module at 75% threshold
- **Milestone Progression**: Only one active milestone at a time
- **Visual Indicators**: Completion rings and progress bars

## Data Flow

1. **User Input** → Vue components capture interactions
2. **Agent Processing** → Flask routes handle requests via agent orchestration
3. **AI Analysis** → OpenAI models process context and generate responses
4. **Vision Processing** → CLIP analyzes camera frames for object detection
5. **State Updates** → Database stores progress and agent evolution data
6. **UI Rendering** → Three.js updates agent visuals and AR overlays
7. **Feedback Loop** → Completion metrics drive agent growth and feature unlocks

## External Dependencies

### AI Services
- **OpenAI API**: GPT-4o for agent responses, CLIP for vision processing
- **OpenAI Agents SDK**: Advanced agent orchestration capabilities

### Web3 Integration
- **MetaMask**: Ethereum wallet authentication
- **Web3.py**: Blockchain interaction utilities

### Frontend Libraries
- **Three.js**: WebGL 3D rendering for Tamagotchi agent
- **Vue 3**: Reactive component framework
- **Bootstrap 5**: Responsive UI components

### Backend Services
- **Flask-Login**: Session management
- **Flask-Dance**: OAuth integration
- **Gunicorn**: WSGI server for production

## Deployment Strategy

### Development Environment
- **Platform**: Replit with integrated development workflow
- **Database**: SQLite for rapid prototyping
- **Hot Reload**: Flask development server with Vue component updates

### Production Considerations
- **Database Migration**: Prepared for PostgreSQL with Drizzle ORM compatibility
- **WSGI Server**: Gunicorn with multi-worker configuration
- **Static Assets**: CDN delivery for Three.js and Vue components
- **Health Monitoring**: `/healthz` endpoint for regression testing
- **Performance**: 95% Lighthouse score target with <1MB bundle size

### Security Features
- **CSRF Protection**: Form token validation
- **Input Sanitization**: HTML escaping in chat messages
- **Session Management**: Permanent sessions with secure cookie handling
- **Multi-auth Support**: Traditional, Web3, and OAuth flows

### Activation Metrics
- **Key Metric**: Users who reach Milestone 1 / total sign-ups
- **Target**: 70% activation rate
- **Instant Wins**: Quick value delivery within first 5 minutes
- **Progressive Onboarding**: 30-minute completion target for first milestone