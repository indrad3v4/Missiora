/**
 * Enhanced Vue Components with CLIP Vision Integration
 * Mixed Reality Tamagotchi Experience with See→Think→Act capabilities
 */

// Browser-compatible version without ES6 imports
// Dependencies will be loaded via script tags in the HTML

// Enhanced Header with AR Toggle and Collapsible Design
const HeaderView = {
    props: ['userData', 'agentCompletion', 'visionStatus', 'isArMode'],
    emits: ['toggle-ar', 'toggle-collapse'],
    data() {
        return {
            isCollapsed: false,
            showPersonaCard: true
        };
    },
    template: `
        <header class="mr-header" :class="{ 'collapsed': isCollapsed || isArMode, 'ar-mode': isArMode }">
            <div class="header-content">
                <div class="header-row">
                    <div class="brand-section">
                        <h1 class="brand-title">MISSIORA</h1>
                        <button 
                            class="ar-toggle-btn" 
                            :class="{ active: isArMode }"
                            @click="$emit('toggle-ar')"
                            title="Toggle AR Mode"
                        >
                            <span class="ar-icon">👁️</span>
                            <span class="ar-label">{{ isArMode ? 'EXIT AR' : 'AR MODE' }}</span>
                        </button>
                    </div>
                    
                    <div class="status-section">
                        <div class="completion-ring" :style="completionRingStyle">
                            <span class="completion-text">{{ Math.round(agentCompletion) }}%</span>
                        </div>
                        <div class="vision-indicator" :class="{ active: visionStatus.active }">
                            <span class="vision-icon">👁️</span>
                            <span class="vision-status">{{ visionStatus.active ? 'Seeing' : 'Offline' }}</span>
                        </div>
                        <button 
                            class="collapse-btn" 
                            @click="toggleCollapse"
                            v-if="!isArMode"
                            title="Collapse Header"
                        >
                            <span :class="isCollapsed ? 'expand-icon' : 'collapse-icon'">{{ isCollapsed ? '▼' : '▲' }}</span>
                        </button>
                    </div>
                </div>
                
                <div class="persona-card" v-if="userData && showPersonaCard && !isCollapsed && !isArMode">
                    <div class="persona-info">
                        <div class="persona-avatar">
                            <span class="persona-initials">{{ getInitials(userData.name) }}</span>
                        </div>
                        <div class="persona-details">
                            <h3 class="persona-name">{{ userData.name || 'Indradeva' }}</h3>
                            <div class="persona-tags">
                                <span class="tag goal">🎯 {{ userData.currentGoal || 'Reach €1K' }}</span>
                                <span class="tag location">📍 {{ userData.location || 'Krakow' }}</span>
                                <span class="tag timeline">📅 {{ userData.timeline || 'Q3 2025' }}</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </header>
    `,
    methods: {
        toggleCollapse() {
            this.isCollapsed = !this.isCollapsed;
            this.$emit('toggle-collapse', this.isCollapsed);
        },
        getInitials(name) {
            if (!name) return 'IN';
            return name.split(' ').map(n => n[0]).join('').toUpperCase();
        }
    },
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

// Export the main app component properly
export const MainApp = {
    template: `
        <div class="mr-main">
            <div class="mr-header">
                <HeaderView 
                    :user-data="userData"
                    @toggle-camera="toggleCamera"
                />
            </div>
            
            <div class="mr-content">
                <div class="mr-views">
                    <IdentityView 
                        v-if="activeView === 'identity'"
                        :key="viewKey"
                        @save="onIdentitySaved"
                        @update-header="updateHeader"
                    />
                    <MissionView 
                        v-if="activeView === 'mission'"
                        :key="viewKey"
                        @save="onMissionSaved"
                        @update-header="updateHeader"
                    />
                    <RoadmapView 
                        v-if="activeView === 'roadmap'"
                        :key="viewKey"
                        @save="onRoadmapSaved"
                        @update-header="updateHeader"
                    />
                </div>
            </div>
            
            <div class="mr-footer">
                <div class="view-tabs">
                    <button 
                        :class="{ active: activeView === 'identity' }"
                        @click="setActiveView('identity')"
                    >
                        Identity
                    </button>
                    <button 
                        :class="{ active: activeView === 'mission' }"
                        @click="setActiveView('mission')"
                    >
                        Mission
                    </button>
                    <button 
                        :class="{ active: activeView === 'roadmap' }"
                        @click="setActiveView('roadmap')"
                    >
                        Roadmap
                    </button>
                </div>
            </div>
        </div>
    `,
    
    data() {
        return {
            activeView: 'identity',
            viewKey: 1,
            userData: {
                name: 'Loading...',
                currentGoal: 'Loading...',
                location: 'Loading...'
            },
            cameraIntegration: null,
            arOverlay: null
        }
    },
    
    async mounted() {
        try {
            await this.initializeVision();
            await this.loadUserData();
        } catch (error) {
            console.error('App initialization error:', error);
            // Continue loading even if vision fails
            await this.loadUserData();
        }
    },
    
    methods: {
        async initializeVision() {
            try {
                // Import vision modules dynamically
                const [CameraModule, ARModule] = await Promise.all([
                    import('/static/js/camera-integration.js'),
                    import('/static/js/ar-overlay.js')
                ]);
                
                this.cameraIntegration = new CameraModule.CameraIntegration();
                this.arOverlay = new ARModule.AROverlay();
            } catch (error) {
                console.warn('Vision system not available:', error);
            }
        },
        
        async loadUserData() {
            try {
                const response = await fetch('/api/user-data');
                if (response.ok) {
                    this.userData = await response.json();
                }
            } catch (error) {
                console.error('Failed to load user data:', error);
            }
        },
        
        setActiveView(view) {
            this.activeView = view;
            this.viewKey++;
        },
        
        toggleCamera() {
            if (this.cameraIntegration) {
                this.cameraIntegration.toggleCamera();
            }
        },
        
        updateHeader(data) {
            Object.assign(this.userData, data);
        },
        
        onIdentitySaved() {
            this.updateHeader({ name: 'Identity Complete' });
        },
        
        onMissionSaved() {
            this.updateHeader({ currentGoal: 'Mission Set' });
        },
        
        onRoadmapSaved() {
            this.updateHeader({ currentGoal: 'Roadmap Ready' });
        }
    },
    
    components: {
        HeaderView,
        IdentityView, 
        MissionView,
        RoadmapView
    }
};

// Export all components
export { HeaderView, IdentityView, MissionView, RoadmapView };ity View with Vision Guidance
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
                    // Emit HUD card event for progressive disclosure
                    const event = new CustomEvent('identity-completed', {
                        detail: {
                            name: this.identity.name,
                            place: this.identity.region,
                            archetype: this.identity.archetype,
                            mood: this.identity.mood,
                            field: this.identity.field,
                            title: this.identity.selfTitle
                        }
                    });
                    document.dispatchEvent(event);
                    
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
                    // Emit HUD card event for progressive disclosure
                    const event = new CustomEvent('mission-completed', {
                        detail: {
                            goal: this.mission.goal,
                            timeline: this.mission.timeline,
                            targetIncome: this.mission.goal.match(/€(\d+)/)?.[1] || '1000'
                        }
                    });
                    document.dispatchEvent(event);
                    
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

// Footer Navigation Component
const FooterNav = {
    props: {
        activeView: {
            type: String,
            default: 'identity'
        },
        completionData: {
            type: Object,
            default: () => ({
                identity: 0,
                mission: 0,
                roadmap: 0
            })
        },
        arMode: {
            type: Boolean,
            default: false
        }
    },
    emits: ['navigate'],
    template: `
        <div class="footer-nav" :class="{ 'ar-mode': arMode }">
            <button 
                @click="navigate('identity')"
                :class="[
                    'footer-nav-button',
                    { 
                        'active': activeView === 'identity',
                        'disabled': false
                    }
                ]"
            >
                <div class="footer-nav-icon">🧠</div>
                <div class="footer-nav-label">Identity</div>
                <div class="footer-nav-dot" :class="{ 'completed': completionData.identity >= 75 }"></div>
            </button>
            
            <button 
                @click="navigate('mission')"
                :class="[
                    'footer-nav-button',
                    { 
                        'active': activeView === 'mission',
                        'disabled': completionData.identity < 75
                    }
                ]"
            >
                <div class="footer-nav-icon">🎯</div>
                <div class="footer-nav-label">Mission</div>
                <div class="footer-nav-dot" :class="{ 'completed': completionData.mission >= 75 }"></div>
            </button>
            
            <button 
                @click="navigate('roadmap')"
                :class="[
                    'footer-nav-button',
                    { 
                        'active': activeView === 'roadmap',
                        'disabled': completionData.mission < 75
                    }
                ]"
            >
                <div class="footer-nav-icon">🗺️</div>
                <div class="footer-nav-label">Roadmap</div>
                <div class="footer-nav-dot" :class="{ 'completed': completionData.roadmap >= 50 }"></div>
            </button>
        </div>
    `,
    methods: {
        navigate(view) {
            // Check if view is unlocked
            if (view === 'mission' && this.completionData.identity < 75) {
                return;
            }
            if (view === 'roadmap' && this.completionData.mission < 75) {
                return;
            }
            
            this.$emit('navigate', view);
        }
    }
};

// Main MR Application with Full CLIP Integration
const MainApp = {
    components: {
        HeaderView,
        IdentityView, 
        MissionView,
        RoadmapView,
        HUDCard,
        FooterNav
    },
    data() {
        return {
            currentView: 'identity',
            userData: {
                name: 'Indradeva',
                currentGoal: 'Reach €1K',
                location: 'Krakow',
                timeline: 'Q3 2025',
                balance: 0
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
            tokenTracker: null,
            agentMessage: '',
            showAgentBubble: false,
            isArMode: false,
            headerCollapsed: false,
            pendingAgentResponses: new Map(),
            agentResponseDebounce: null,
            detectedObjects: [],
            tamagotchiMessages: []
        };
    },
    template: `
        <div class="triz-layout">
            <!-- TRIZ Header Zone: 15vh -->
            <div class="triz-header">
                <HUDCard />
            </div>
            
            <!-- TRIZ Body Zone: 75vh -->
            <div class="triz-body">
                <!-- View Content -->
                <IdentityView 
                    v-if="currentView === 'identity'" 
                    @save="onIdentitySaved"
                    @completion-change="onCompletionChange"
                    @update-header="onHeaderUpdate"
                />
                
                <MissionView 
                    v-if="currentView === 'mission'" 
                    @save="onMissionSaved"
                    @completion-change="onCompletionChange"
                    @update-header="onHeaderUpdate"
                />
                
                <RoadmapView 
                    v-if="currentView === 'roadmap'" 
                    @save="onRoadmapSaved"
                    @completion-change="onCompletionChange"
                />
            </div>
            
            <!-- TRIZ Footer Zone: 10vh -->
            <div class="triz-footer" :class="{ 'ar-mode': isArMode }">
                <FooterNav 
                    :activeView="currentView"
                    :completionData="completionData"
                    :arMode="isArMode"
                    @navigate="onNavigate"
                />
            </div>
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
                'position-top': this.currentView === 'identity',
                'position-center': this.currentView === 'mission',
                'position-bottom': this.currentView === 'roadmap'
            };
        }
    },
    async mounted() {
        this.setupVisionEventListeners();
        this.showAgentWelcome();
        console.log('✓ TRIZ-optimized app initialized');
    },
    methods: {
        setupVisionEventListeners() {
            // Mock vision for demonstration
            setTimeout(() => {
                this.visionStatus.active = true;
                this.visionStatus.analyzing = false;
            }, 1000);
        },
        
        // Navigation Methods
        onNavigate(view) {
            this.currentView = view;
            
            // Enable AR mode only for roadmap view
            if (view === 'roadmap') {
                this.isArMode = true;
            } else {
                this.isArMode = false;
            }
        },
        
        // Component Event Handlers
        onIdentitySaved(identityData) {
            Object.assign(this.userData, identityData);
        },
        
        onMissionSaved(missionData) {
            Object.assign(this.userData, missionData);
        },
        
        onRoadmapSaved(roadmapData) {
            // Handle roadmap data
            console.log('Roadmap saved:', roadmapData);
        },
        
        onCompletionChange(type, percentage) {
            this.completionData[type] = percentage;
            this.updateAgentCompletion();
            this.updateAgentMessage();
        },
        
        onHeaderUpdate(headerData) {
            Object.assign(this.userData, headerData);
        },
        
        toggleArMode() {
            this.isArMode = !this.isArMode;
        },
        
        onVisionDetected(objects) {
            this.detectedObjects = objects;
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
            // TRIZ-optimized: lightweight completion tracking
            const total = this.totalCompletion;
            console.log(`Agent completion: ${total}%`);
        },
        
        updateAgentMessage() {
            // TRIZ-optimized: simple message system
            const messages = {
                'identity': "I'm learning about you! 🌱",
                'mission': "Your mission is taking shape 🎯",
                'roadmap': "Let's build your path forward 🗺️"
            };
            
            this.agentMessage = messages[this.currentView] || "How can I help you today?";
            this.showAgentBubble = true;
            
            setTimeout(() => {
                this.showAgentBubble = false;
            }, 5000);
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
            
            this.currentView = tab;
            this.updateAgentMessage();
            console.log(`Switched to ${tab} view`);
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
        
        toggleArMode() {
            this.isArMode = !this.isArMode;
            
            if (this.isArMode) {
                document.body.classList.add('ar-mode');
                this.showAgentMessage("AR mode activated! Point your camera at objects for smart insights.");
            } else {
                document.body.classList.remove('ar-mode');
                this.showAgentMessage("AR mode deactivated. Continuing with normal view.");
            }
        },
        
        onHeaderCollapse(collapsed) {
            this.headerCollapsed = collapsed;
            console.log(`Header collapsed: ${collapsed}`);
        },
        
        // TRIZ-optimized: simplified agent response system
        async getConsolidatedAgentResponse(userMessage, context) {
            try {
                const response = await fetch('/api/chat', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        message: userMessage,
                        context: context
                    })
                });
                
                if (response.ok) {
                    return await response.json();
                } else {
                    return { reply: "I'm having trouble processing that right now. Please try again." };
                }
            } catch (error) {
                console.error('Agent response error:', error);
                return { reply: "I encountered an error. Please try again." };
            }
        },
        
        handleResize() {
            console.log('Window resized - TRIZ optimized layout handles this automatically');
        }
    }
};

// Simple HUD Card component for TRIZ layout
const HUDCard = {
    template: `
        <div class="hud-card">
            <div class="hud-stage">TRIZ Optimized</div>
            <div class="hud-progress">System Ready</div>
        </div>
    `
};

// Make components available globally for browser usage
window.MainApp = MainApp;
window.HeaderView = HeaderView;
window.IdentityView = IdentityView;
window.MissionView = MissionView;
window.RoadmapView = RoadmapView;
window.HUDCard = HUDCard;
window.FooterNav = FooterNav;