/**
 * Enhanced Vue Components with CLIP Vision Integration
 * Mixed Reality Tamagotchi Experience with See→Think→Act capabilities
 */

import { TamagotchiAgent } from './tamagotchi-agent.js';
import { CameraIntegration } from './camera-integration.js';
import { AROverlay } from './ar-overlay.js';

// Enhanced Header with Vision Status and AR Mode
const HeaderView = {
    props: ['userData', 'agentCompletion', 'visionStatus', 'arMode', 'tokenData'],
    template: `
        <header class="mr-header" :class="{ 'ar-mode': arMode, 'minimized': arMode }">
            <!-- Minimal header for AR mode -->
            <div v-if="arMode" class="header-content-minimal">
                <div class="mini-brand">M</div>
                <div class="mini-user-info">
                    <span class="mini-name">{{ userData.name || userData.username || 'User' }}</span>
                    <span class="mini-status">{{ Math.round(agentCompletion) }}%</span>
                    <span class="mini-tokens">💎 {{ tokenData?.balance || 0 }}</span>
                </div>
                <div class="mini-vision-indicator" :class="{ active: visionStatus.active }">
                    <span class="vision-icon">👁️</span>
                </div>
            </div>
            
            <!-- Full header for normal mode -->
            <div v-else class="header-content">
                <h1 class="brand-title">MISSIORA</h1>
                
                <div v-if="userData" class="user-data-card">
                    <div class="user-info">
                        <span class="user-name">{{ userData.name || userData.username || 'New User' }}</span>
                        <div class="user-details">
                            <span class="goal">🎯 {{ userData.mission?.goal || 'Define your goal' }}</span>
                            <span class="location">📍 {{ userData.identity?.region || 'Set location' }}</span>
                            <span class="timeline">📅 {{ userData.identity?.timeline || 'Set timeline' }}</span>
                            <span class="tokens">💎 {{ tokenData?.balance || 0 }} tokens</span>
                        </div>
                    </div>
                </div>
                
                <div class="agent-status">
                    <div class="completion-ring" :style="completionRingStyle">
                        <span class="completion-text">{{ Math.round(agentCompletion) }}%</span>
                    </div>
                    <div class="vision-indicator" :class="{ active: visionStatus.active }">
                        <span class="vision-icon">👁️</span>
                        <span class="vision-status">{{ visionStatus.active ? 'Seeing' : 'Offline' }}</span>
                    </div>
                </div>
            </div>
        </header>
    `,
    computed: {
        completionRingStyle() {
            const percentage = this.agentCompletion || 0;
            const color = percentage <= 25 ? '#22d3ee' :
                         percentage <= 50 ? '#4ade80' :
                         percentage <= 80 ? '#fbbf24' : '#9333ea';
            
            return {
                background: `conic-gradient(${color} ${percentage * 3.6}deg, rgba(255,255,255,0.2) 0deg)`,
                borderColor: color
            };
        }
    }
};

// Enhanced Identity View with Vision Guidance
const IdentityView = {
    emits: ['save', 'update-header', 'completion-change'],
    data() {
        return {
            identity: {
                name: '',
                archetype: '',
                mood: '',
                region: '',
                field: '',
                selfTitle: ''
            },
            completionPercentage: 0,
            visionGuidance: ''
        };
    },
    template: `
        <div class="mr-view identity-view">
            <div class="view-content">
                <div class="section-header">
                    <h2>🧬 Define Your Identity</h2>
                    <p>Help your AI companion understand who you are</p>
                    <div v-if="visionGuidance" class="vision-guidance">
                        {{ visionGuidance }}
                    </div>
                </div>
                
                <form @submit.prevent="saveIdentity" class="mr-form">
                    <div class="form-group">
                        <label class="form-label">Your Name</label>
                        <input 
                            v-model="identity.name" 
                            @input="updateCompletion"
                            placeholder="Enter your full name" 
                            class="mr-input" 
                        />
                    </div>
                    
                    <div class="form-group">
                        <label class="form-label">Entrepreneurial Archetype</label>
                        <select v-model="identity.archetype" @change="updateCompletion" class="mr-select">
                            <option value="">Select your archetype</option>
                            <option value="builder">🏗️ Builder - Create and construct</option>
                            <option value="guide">🧭 Guide - Teach and mentor</option>
                            <option value="rebel">⚡ Rebel - Disrupt and innovate</option>
                            <option value="creator">🎨 Creator - Design and imagine</option>
                            <option value="connector">🤝 Connector - Network and unite</option>
                        </select>
                    </div>
                    
                    <div class="form-group">
                        <label class="form-label">Current Energy & Mood</label>
                        <textarea 
                            v-model="identity.mood" 
                            @input="updateCompletion"
                            placeholder="How are you feeling about your entrepreneurial journey right now?"
                            class="mr-textarea"
                        ></textarea>
                    </div>
                    
                    <div class="form-group">
                        <label class="form-label">Location</label>
                        <input 
                            v-model="identity.region" 
                            @input="updateCompletion"
                            placeholder="Where are you based? (e.g., Krakow, Poland)" 
                            class="mr-input" 
                        />
                    </div>
                    
                    <div class="form-group">
                        <label class="form-label">Industry/Field</label>
                        <input 
                            v-model="identity.field" 
                            @input="updateCompletion"
                            placeholder="What industry or field do you work in?" 
                            class="mr-input" 
                        />
                    </div>
                    
                    <div class="form-group">
                        <label class="form-label">Professional Title</label>
                        <input 
                            v-model="identity.selfTitle" 
                            @input="updateCompletion"
                            placeholder="How do you describe yourself professionally?" 
                            class="mr-input" 
                        />
                    </div>
                    
                    <div class="form-actions">
                        <button type="submit" class="mr-button primary" :disabled="completionPercentage < 80">
                            Save Identity & Continue
                        </button>
                        <div class="completion-indicator">
                            <span>Completion: {{ Math.round(completionPercentage) }}%</span>
                            <div class="progress-bar">
                                <div class="progress-fill" :style="{ width: completionPercentage + '%' }"></div>
                            </div>
                        </div>
                    </div>
                </form>
            </div>
        </div>
    `,
    async mounted() {
        await this.loadIdentity();
        this.setupVisionGuidance();
    },
    methods: {
        setupVisionGuidance() {
            window.addEventListener('vision:objects-detected', (event) => {
                const objects = event.detail.objects || [];
                if (objects.length > 0) {
                    this.visionGuidance = `I see ${objects[0].label}! This might inspire your identity.`;
                    setTimeout(() => {
                        this.visionGuidance = '';
                    }, 5000);
                }
            });
        },
        
        async loadIdentity() {
            try {
                const response = await fetch('/api/identity');
                if (response.ok) {
                    const data = await response.json();
                    Object.assign(this.identity, data);
                    this.updateCompletion();
                }
            } catch (error) {
                console.log('No existing identity data');
            }
        },
        
        updateCompletion() {
            const fields = ['name', 'archetype', 'mood', 'region', 'field', 'selfTitle'];
            const completed = fields.filter(field => this.identity[field]?.trim()).length;
            this.completionPercentage = (completed / fields.length) * 100;
            
            this.$emit('completion-change', 'identity', this.completionPercentage);
        },
        
        async saveIdentity() {
            try {
                const response = await fetch('/api/identity', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(this.identity)
                });
                
                if (response.ok) {
                    this.$emit('save', this.identity);
                    this.$emit('update-header', {
                        name: this.identity.name,
                        location: this.identity.region
                    });
                }
            } catch (error) {
                console.error('Failed to save identity:', error);
            }
        }
    }
};

// Enhanced Mission View with Vision Integration
const MissionView = {
    emits: ['save', 'update-header', 'completion-change'],
    data() {
        return {
            mission: {
                statement: '',
                goal: '',
                timeline: '',
                emotionalBlocks: ''
            },
            completionPercentage: 0,
            visionInsights: []
        };
    },
    template: `
        <div class="mr-view mission-view">
            <div class="view-content">
                <div class="section-header">
                    <h2>🎯 Craft Your Mission</h2>
                    <p>Define your purpose and goals clearly</p>
                </div>
                
                <div v-if="visionInsights.length > 0" class="vision-insights">
                    <h3>Vision Insights</h3>
                    <div v-for="insight in visionInsights" :key="insight.id" class="insight-item">
                        {{ insight.message }}
                    </div>
                </div>
                
                <form @submit.prevent="saveMission" class="mr-form">
                    <div class="form-group">
                        <label class="form-label">Mission Statement</label>
                        <textarea 
                            v-model="mission.statement"
                            @input="updateCompletion"
                            placeholder="What is your core mission as an entrepreneur? What change do you want to create?"
                            class="mr-textarea large"
                        ></textarea>
                    </div>
                    
                    <div class="form-group">
                        <label class="form-label">Current Goal</label>
                        <input 
                            v-model="mission.goal"
                            @input="updateCompletion"
                            placeholder="What's your immediate goal? (e.g., Reach €1K monthly revenue)"
                            class="mr-input"
                        />
                    </div>
                    
                    <div class="form-group">
                        <label class="form-label">Timeline</label>
                        <select v-model="mission.timeline" @change="updateCompletion" class="mr-select">
                            <option value="">Select timeline</option>
                            <option value="Q1 2025">Q1 2025</option>
                            <option value="Q2 2025">Q2 2025</option>
                            <option value="Q3 2025">Q3 2025</option>
                            <option value="Q4 2025">Q4 2025</option>
                            <option value="2026">2026</option>
                        </select>
                    </div>
                    
                    <div class="form-group">
                        <label class="form-label">Emotional Blocks</label>
                        <textarea 
                            v-model="mission.emotionalBlocks"
                            @input="updateCompletion"
                            placeholder="What fears or limiting beliefs are holding you back?"
                            class="mr-textarea"
                        ></textarea>
                    </div>
                    
                    <div class="form-actions">
                        <button type="submit" class="mr-button primary" :disabled="completionPercentage < 75">
                            Save Mission & Continue
                        </button>
                        <div class="completion-indicator">
                            <span>Completion: {{ Math.round(completionPercentage) }}%</span>
                            <div class="progress-bar">
                                <div class="progress-fill" :style="{ width: completionPercentage + '%' }"></div>
                            </div>
                        </div>
                    </div>
                </form>
            </div>
        </div>
    `,
    async mounted() {
        await this.loadMission();
        this.setupVisionInsights();
    },
    methods: {
        setupVisionInsights() {
            window.addEventListener('vision:objects-detected', (event) => {
                const objects = event.detail.objects || [];
                objects.forEach(object => {
                    if (this.isRelevantToMission(object.label)) {
                        this.addVisionInsight(object);
                    }
                });
            });
        },
        
        isRelevantToMission(label) {
            const relevantObjects = ['laptop', 'computer', 'book', 'paper', 'whiteboard', 'person'];
            return relevantObjects.some(obj => label.toLowerCase().includes(obj));
        },
        
        addVisionInsight(object) {
            const insight = {
                id: Date.now(),
                message: this.getInsightMessage(object.label),
                timestamp: new Date()
            };
            
            this.visionInsights.unshift(insight);
            
            // Keep only last 3 insights
            if (this.visionInsights.length > 3) {
                this.visionInsights = this.visionInsights.slice(0, 3);
            }
            
            // Auto-remove after 30 seconds
            setTimeout(() => {
                this.visionInsights = this.visionInsights.filter(i => i.id !== insight.id);
            }, 30000);
        },
        
        getInsightMessage(label) {
            const messages = {
                laptop: "I see your workspace! Your mission should reflect how you create value digitally.",
                book: "Knowledge is power! What you're learning can shape your mission statement.",
                whiteboard: "I see planning in progress! Let me help you clarify your mission.",
                person: "People are central to every mission. How do you serve others?"
            };
            
            const key = Object.keys(messages).find(k => label.toLowerCase().includes(k));
            return messages[key] || "This environment element could inspire your mission!";
        },
        
        async loadMission() {
            try {
                const response = await fetch('/api/mission');
                if (response.ok) {
                    const data = await response.json();
                    Object.assign(this.mission, data);
                    this.updateCompletion();
                }
            } catch (error) {
                console.log('No existing mission data');
            }
        },
        
        updateCompletion() {
            const fields = ['statement', 'goal', 'timeline', 'emotionalBlocks'];
            const completed = fields.filter(field => this.mission[field]?.trim()).length;
            this.completionPercentage = (completed / fields.length) * 100;
            
            this.$emit('completion-change', 'mission', this.completionPercentage);
        },
        
        async saveMission() {
            try {
                const response = await fetch('/api/mission', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(this.mission)
                });
                
                if (response.ok) {
                    this.$emit('save', this.mission);
                    this.$emit('update-header', {
                        currentGoal: this.mission.goal,
                        timeline: this.mission.timeline
                    });
                }
            } catch (error) {
                console.error('Failed to save mission:', error);
            }
        }
    }
};

// Enhanced Roadmap View with Smart Milestone Generation
const RoadmapView = {
    emits: ['completion-change'],
    data() {
        return {
            milestones: [],
            completionPercentage: 0,
            smartSuggestions: []
        };
    },
    template: `
        <div class="mr-view roadmap-view">
            <div class="view-content">
                <div class="section-header">
                    <h2>🗺️ Your Smart Roadmap</h2>
                    <p>AI-generated milestones based on your identity and mission</p>
                </div>
                
                <div v-if="smartSuggestions.length > 0" class="smart-suggestions">
                    <h3>Vision-Based Suggestions</h3>
                    <div v-for="suggestion in smartSuggestions" :key="suggestion.id" class="suggestion-item">
                        <span class="suggestion-text">{{ suggestion.text }}</span>
                        <button @click="addSuggestionToRoadmap(suggestion)" class="add-button">Add</button>
                    </div>
                </div>
                
                <div class="milestones-container">
                    <div 
                        v-for="milestone in milestones" 
                        :key="milestone.id"
                        :class="['milestone-card', milestone.status]"
                    >
                        <div class="milestone-icon">
                            <span v-if="milestone.status === 'completed'">✅</span>
                            <span v-else-if="milestone.status === 'active'">🎯</span>
                            <span v-else>⭕</span>
                        </div>
                        
                        <div class="milestone-content">
                            <h3>{{ milestone.title }}</h3>
                            <p>{{ milestone.description }}</p>
                            
                            <div v-if="milestone.status === 'active'" class="milestone-actions">
                                <button @click="completeMilestone(milestone.id)" class="mr-button small">
                                    Mark Complete
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
                
                <div class="completion-indicator">
                    <span>Roadmap Progress: {{ Math.round(completionPercentage) }}%</span>
                    <div class="progress-bar">
                        <div class="progress-fill" :style="{ width: completionPercentage + '%' }"></div>
                    </div>
                </div>
            </div>
        </div>
    `,
    async mounted() {
        await this.loadMilestones();
        this.setupVisionSuggestions();
    },
    methods: {
        setupVisionSuggestions() {
            window.addEventListener('vision:objects-detected', (event) => {
                const objects = event.detail.objects || [];
                objects.forEach(object => {
                    const suggestion = this.generateSmartSuggestion(object);
                    if (suggestion) {
                        this.addSmartSuggestion(suggestion);
                    }
                });
            });
        },
        
        generateSmartSuggestion(object) {
            const label = object.label.toLowerCase();
            const suggestions = {
                'business card': 'Follow up with new contact within 48 hours',
                'laptop': 'Optimize your digital workspace for productivity',
                'whiteboard': 'Document and implement the ideas from this session',
                'book': 'Schedule learning time based on this knowledge',
                'person': 'Plan networking follow-up or collaboration opportunity'
            };
            
            const key = Object.keys(suggestions).find(k => label.includes(k));
            return key ? {
                id: Date.now() + Math.random(),
                text: suggestions[key],
                source: object.label,
                confidence: object.confidence
            } : null;
        },
        
        addSmartSuggestion(suggestion) {
            // Check if similar suggestion already exists
            const exists = this.smartSuggestions.some(s => s.text === suggestion.text);
            if (!exists) {
                this.smartSuggestions.unshift(suggestion);
                
                // Keep only last 5 suggestions
                if (this.smartSuggestions.length > 5) {
                    this.smartSuggestions = this.smartSuggestions.slice(0, 5);
                }
                
                // Auto-remove after 60 seconds
                setTimeout(() => {
                    this.smartSuggestions = this.smartSuggestions.filter(s => s.id !== suggestion.id);
                }, 60000);
            }
        },
        
        async addSuggestionToRoadmap(suggestion) {
            try {
                const response = await fetch('/api/milestones/from-suggestion', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        suggestion: suggestion.text,
                        source: suggestion.source
                    })
                });
                
                if (response.ok) {
                    await this.loadMilestones();
                    this.smartSuggestions = this.smartSuggestions.filter(s => s.id !== suggestion.id);
                }
            } catch (error) {
                console.error('Failed to add suggestion to roadmap:', error);
            }
        },
        
        async loadMilestones() {
            try {
                const response = await fetch('/api/milestones');
                if (response.ok) {
                    this.milestones = await response.json();
                    this.updateCompletion();
                }
            } catch (error) {
                console.error('Failed to load milestones:', error);
            }
        },
        
        updateCompletion() {
            if (this.milestones.length === 0) {
                this.completionPercentage = 0;
                return;
            }
            
            const completed = this.milestones.filter(m => m.status === 'completed').length;
            this.completionPercentage = (completed / this.milestones.length) * 100;
            
            this.$emit('completion-change', 'roadmap', this.completionPercentage);
        },
        
        async completeMilestone(milestoneId) {
            try {
                const response = await fetch(`/api/milestones/${milestoneId}/complete`, {
                    method: 'POST'
                });
                
                if (response.ok) {
                    await this.loadMilestones();
                }
            } catch (error) {
                console.error('Failed to complete milestone:', error);
            }
        }
    }
};

// Main MR Application with Full CLIP Integration
const MainApp = {
    components: {
        HeaderView,
        IdentityView, 
        MissionView,
        RoadmapView
    },
    data() {
        return {
            activeTab: 'identity',
            arMode: false,
            userData: {
                name: '',
                username: '',
                identity: null,
                mission: null,
                balance: 0
            },
            tokenData: {
                balance: 100,
                tier: 'free',
                shouldUpgrade: false
            },
            completionData: {
                identity: 0,
                mission: 0,
                roadmap: 0
            },
            visionStatus: {
                active: false,
                analyzing: false,
                lastDetection: null
            },
            agent: null,
            camera: null,
            arOverlay: null,
            agentMessage: '',
            showAgentBubble: false
        };
    },
    template: `
        <div class="mr-app">
            <!-- Agent Canvas -->
            <canvas ref="agentCanvas" class="agent-canvas"></canvas>
            
            <!-- Agent Speech Bubble -->
            <div v-if="showAgentBubble" class="agent-speech-bubble" :class="agentBubblePosition">
                <p>{{ agentMessage }}</p>
                <div class="bubble-arrow"></div>
            </div>
            
            <!-- Header -->
            <HeaderView 
                :user-data="userData" 
                :agent-completion="totalCompletion"
                :vision-status="visionStatus"
                :ar-mode="arMode"
                :token-data="tokenData"
            />
            
            <!-- Main Content -->
            <main class="mr-main" v-if="!arMode">
                <IdentityView 
                    v-if="activeTab === 'identity'"
                    @save="onIdentitySaved"
                    @update-header="updateHeader"
                    @completion-change="updateCompletion"
                />
                <MissionView 
                    v-if="activeTab === 'mission'"
                    @save="onMissionSaved"
                    @update-header="updateHeader"
                    @completion-change="updateCompletion"
                />
                <RoadmapView 
                    v-if="activeTab === 'roadmap'"
                    @completion-change="updateCompletion"
                />
            </main>
            
            <!-- Enhanced Footer Navigation -->
            <footer class="mr-footer">
                <div class="tab-navigation">
                    <button 
                        @click="switchTab('identity')"
                        :class="['nav-tab', { active: activeTab === 'identity' }]"
                        :disabled="false"
                    >
                        <span class="tab-icon">🧬</span>
                        <span class="tab-label">Identity</span>
                        <div class="completion-dot" :class="{ filled: completionData.identity >= 80 }"></div>
                    </button>
                    
                    <button 
                        @click="switchTab('mission')"
                        :class="['nav-tab', { active: activeTab === 'mission' }]"
                        :disabled="completionData.identity < 80"
                    >
                        <span class="tab-icon">🎯</span>
                        <span class="tab-label">Mission</span>
                        <div class="completion-dot" :class="{ filled: completionData.mission >= 75 }"></div>
                    </button>
                    
                    <button 
                        @click="switchTab('roadmap')"
                        :class="['nav-tab', { active: activeTab === 'roadmap' }]"
                        :disabled="completionData.mission < 75"
                    >
                        <span class="tab-icon">🗺️</span>
                        <span class="tab-label">Roadmap</span>
                        <div class="completion-dot" :class="{ filled: completionData.roadmap >= 50 }"></div>
                    </button>
                    
                    <button 
                        @click="toggleARMode"
                        :class="['nav-tab ar-toggle', { active: arMode }]"
                    >
                        <span class="tab-icon">📷</span>
                        <span class="tab-label">{{ arMode ? 'Exit AR' : 'AR Mode' }}</span>
                    </button>
                </div>
            </footer>
        </div>
    `,
    computed: {
        totalCompletion() {
            return (this.completionData.identity * 0.33) + 
                   (this.completionData.mission * 0.33) + 
                   (this.completionData.roadmap * 0.34);
        },
        
        agentBubblePosition() {
            return {
                'position-top': this.activeTab === 'identity',
                'position-center': this.activeTab === 'mission',
                'position-bottom': this.activeTab === 'roadmap'
            };
        }
    },
    async mounted() {
        this.initializeCamera();
        this.initializeAgent();
        this.initializeAROverlay();
        this.showAgentWelcome();
        this.setupVisionEventListeners();
        await this.loadUserData();
        
        window.addEventListener('resize', this.handleResize);
    },
    beforeUnmount() {
        if (this.agent) {
            this.agent.destroy();
        }
        if (this.camera) {
            this.camera.destroy();
        }
        if (this.arOverlay) {
            this.arOverlay.destroy();
        }
        window.removeEventListener('resize', this.handleResize);
    },
    methods: {
        initializeCamera() {
            this.camera = new CameraIntegration();
        },
        
        initializeAgent() {
            this.agent = new TamagotchiAgent(this.$refs.agentCanvas);
            this.updateAgentCompletion();
        },
        
        initializeAROverlay() {
            this.arOverlay = new AROverlay();
            this.arOverlay.onActionSelected = this.handleActionSelected;
        },
        
        setupVisionEventListeners() {
            window.addEventListener('camera:ready', () => {
                this.visionStatus.active = true;
            });
            
            window.addEventListener('camera:stopped', () => {
                this.visionStatus.active = false;
            });
            
            window.addEventListener('vision:objects-detected', (event) => {
                this.visionStatus.lastDetection = new Date();
                this.visionStatus.analyzing = true;
                
                setTimeout(() => {
                    this.visionStatus.analyzing = false;
                }, 1000);
                
                // Update agent message based on detected objects
                const objects = event.detail.objects || [];
                if (objects.length > 0 && this.agent) {
                    const message = this.agent.getObjectReactionMessage(objects[0].label);
                    this.showAgentMessage(message);
                }
            });
        },
        
        handleActionSelected(action, object) {
            // Show agent reaction to action
            const reactionMessages = {
                'scan_card': "Great! I'll help you process this business card.",
                'scan_qr': "Let me decode that QR code for you!",
                'ocr_text': "I'll extract the text from what you're showing me.",
                'networking_tips': "Here are some networking insights based on what I see!"
            };
            
            const message = reactionMessages[action.id] || "I'll help you with that!";
            this.showAgentMessage(message);
        },
        
        showAgentMessage(message) {
            this.agentMessage = message;
            this.showAgentBubble = true;
            
            setTimeout(() => {
                this.showAgentBubble = false;
            }, 5000);
        },
        
        updateCompletion(type, percentage) {
            this.completionData[type] = percentage;
            this.updateAgentCompletion();
            this.updateAgentMessage();
        },
        
        updateAgentCompletion() {
            if (this.agent) {
                this.agent.updateCompletion(
                    this.completionData.identity,
                    this.completionData.mission,
                    this.completionData.roadmap
                );
            }
        },
        
        updateAgentMessage() {
            if (this.agent) {
                this.agentMessage = this.agent.getPersonalityMessage();
                this.showAgentBubble = true;
                
                setTimeout(() => {
                    this.showAgentBubble = false;
                }, 5000);
            }
        },
        
        showAgentWelcome() {
            this.agentMessage = "Tell me: what lights you up today?";
            this.showAgentBubble = true;
            
            setTimeout(() => {
                this.showAgentBubble = false;
            }, 8000);
        },
        
        switchTab(tab) {
            if (tab === 'mission' && this.completionData.identity < 80) return;
            if (tab === 'roadmap' && this.completionData.mission < 75) return;
            
            this.activeTab = tab;
            this.updateAgentMessage();
            
            if (this.agent) {
                const mood = tab === 'identity' ? 'curious' :
                            tab === 'mission' ? 'excited' : 'thinking';
                this.agent.playEmotionalReaction(mood);
            }
        },
        
        updateHeader(data) {
            Object.assign(this.userData, data);
        },
        
        onIdentitySaved(identityData) {
            if (this.completionData.identity >= 80) {
                setTimeout(() => {
                    this.switchTab('mission');
                }, 1500);
            }
        },
        
        onMissionSaved(missionData) {
            if (this.completionData.mission >= 75) {
                setTimeout(() => {
                    this.switchTab('roadmap');
                }, 1500);
            }
        },
        
        handleResize() {
            if (this.agent) {
                this.agent.handleResize();
            }
        },
        
        toggleARMode() {
            this.arMode = !this.arMode;
            
            if (this.arMode) {
                // Start camera and show AR overlay
                if (this.camera) {
                    this.camera.requestCameraAccess();
                }
                // Hide main content tabs when in AR mode
                this.activeTab = null;
            } else {
                // Stop camera and hide AR overlay
                if (this.camera) {
                    this.camera.stopCamera();
                }
                // Restore previous tab or default to identity
                this.activeTab = this.activeTab || 'identity';
            }
        },
        
        async loadUserData() {
            try {
                // Load user profile data
                const profileResponse = await fetch('/api/profile');
                if (profileResponse.ok) {
                    const profileData = await profileResponse.json();
                    this.userData.name = profileData.first_name || profileData.username || 'User';
                    this.userData.username = profileData.username;
                }
                
                // Load identity data
                const identityResponse = await fetch('/api/identity');
                if (identityResponse.ok) {
                    this.userData.identity = await identityResponse.json();
                }
                
                // Load mission data
                const missionResponse = await fetch('/api/mission');
                if (missionResponse.ok) {
                    this.userData.mission = await missionResponse.json();
                }
                
                // Load token status
                await this.loadTokenStatus();
            } catch (error) {
                console.log('Error loading user data:', error);
            }
        },
        
        async loadTokenStatus() {
            try {
                const response = await fetch('/api/token/status');
                if (response.ok) {
                    const data = await response.json();
                    this.tokenData = data;
                }
            } catch (error) {
                console.log('Error loading token status:', error);
            }
        },
        
        async consumeTokens(action, model = null) {
            try {
                const response = await fetch('/api/token/consume', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ action, model })
                });
                
                const result = await response.json();
                
                if (result.success) {
                    this.tokenData.balance = result.balance;
                } else if (result.should_upgrade) {
                    // Show upgrade prompt
                    this.showUpgradePrompt(result);
                }
                
                return result;
            } catch (error) {
                console.log('Error consuming tokens:', error);
                return { success: false, error: 'network_error' };
            }
        },
        
        showUpgradePrompt(tokenResult) {
            this.agentMessage = `You're running low on tokens! Upgrade to continue using advanced features. Current balance: ${tokenResult.balance}`;
            this.showAgentBubble = true;
            
            // TODO: Show upgrade modal with package options
            
            setTimeout(() => {
                this.showAgentBubble = false;
            }, 8000);
        }
    }
};

export { MainApp, HeaderView, IdentityView, MissionView, RoadmapView };