/**
 * Enhanced Vue Components for Mixed Reality Tamagotchi Experience
 */

import { TamagotchiAgent } from './tamagotchi-agent.js';
import { CameraIntegration } from './camera-integration.js';

// Enhanced Header with MR styling
const HeaderView = {
    props: ['userData', 'agentCompletion'],
    template: `
        <header class="mr-header">
            <div class="header-content">
                <h1 class="brand-title">MISSIORA</h1>
                
                <div v-if="userData" class="user-data-card">
                    <div class="user-info">
                        <span class="user-name">{{ userData.name || 'Indradeva' }}</span>
                        <div class="user-details">
                            <span class="goal">🎯 {{ userData.currentGoal || 'Reach €1K' }}</span>
                            <span class="location">📍 {{ userData.location || 'Krakow' }}</span>
                            <span class="timeline">📅 {{ userData.timeline || 'Q3 2025' }}</span>
                        </div>
                    </div>
                </div>
                
                <div class="agent-status">
                    <div class="completion-ring" :style="completionRingStyle">
                        <span class="completion-text">{{ Math.round(agentCompletion) }}%</span>
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

// Enhanced Identity View with Agent Interaction
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
            completionPercentage: 0
        };
    },
    template: `
        <div class="mr-view identity-view">
            <div class="view-content">
                <div class="section-header">
                    <h2>🧬 Define Your Identity</h2>
                    <p>Help your AI companion understand who you are</p>
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
    },
    methods: {
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

// Enhanced Mission View with Agent Guidance
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
            completionPercentage: 0
        };
    },
    template: `
        <div class="mr-view mission-view">
            <div class="view-content">
                <div class="section-header">
                    <h2>🎯 Craft Your Mission</h2>
                    <p>Define your purpose and goals clearly</p>
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
    },
    methods: {
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

// Enhanced Roadmap View with Milestone Progression
const RoadmapView = {
    emits: ['completion-change'],
    data() {
        return {
            milestones: [],
            completionPercentage: 0
        };
    },
    template: `
        <div class="mr-view roadmap-view">
            <div class="view-content">
                <div class="section-header">
                    <h2>🗺️ Your Smart Roadmap</h2>
                    <p>AI-generated milestones based on your identity and mission</p>
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
    },
    methods: {
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

// Main MR Application
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
            agent: null,
            camera: null,
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
            />
            
            <!-- Main Content -->
            <main class="mr-main">
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
            // Position bubble based on active tab
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
        this.showAgentWelcome();
        
        // Listen for window resize
        window.addEventListener('resize', this.handleResize);
    },
    beforeUnmount() {
        if (this.agent) {
            this.agent.destroy();
        }
        if (this.camera) {
            this.camera.destroy();
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
                
                // Hide bubble after 5 seconds
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
            // Check if tab is unlocked
            if (tab === 'mission' && this.completionData.identity < 80) return;
            if (tab === 'roadmap' && this.completionData.mission < 75) return;
            
            this.activeTab = tab;
            this.updateAgentMessage();
            
            // Trigger agent mood change based on tab
            if (this.agent) {
                const mood = tab === 'identity' ? 'curious' :
                            tab === 'mission' ? 'excited' : 'thinking';
                this.agent.playMoodAnimation(mood);
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
        }
    }
};

export { MainApp, HeaderView, IdentityView, MissionView, RoadmapView };