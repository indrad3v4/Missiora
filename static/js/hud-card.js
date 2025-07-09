/**
 * TRIZ-Structured HUD Card System
 * Progressive Disclosure Onboarding with Token Economy
 * Following Nielsen Norman Group principles & crypto wallet patterns
 */

// TRIZ Su-Field Analysis Implementation
class HUDCardSystem {
    constructor() {
        this.progressStages = {
            GUEST: { level: 0, label: 'Guest', color: '#6b7280' },
            NAME: { level: 1, label: 'Identity', color: '#3b82f6' },
            PLACE: { level: 2, label: 'Location', color: '#10b981' },
            GOAL: { level: 3, label: 'Mission', color: '#f59e0b' },
            INCOME: { level: 4, label: 'Revenue', color: '#8b5cf6' },
            TOKENS: { level: 5, label: 'Activated', color: '#ef4444' }
        };
        
        this.tokenBalance = 100; // Starting balance
        this.currentStage = 'GUEST';
        this.userMetrics = {
            name: '',
            place: '',
            goal: '',
            targetIncome: '',
            currentIncome: 0,
            completedTasks: 0,
            totalTasks: 5
        };
        
        this.init();
    }
    
    init() {
        this.loadUserProgress();
        this.setupEventListeners();
        this.startRealtimeUpdates();
    }
    
    loadUserProgress() {
        const savedProgress = localStorage.getItem('hudCardProgress');
        if (savedProgress) {
            const data = JSON.parse(savedProgress);
            this.currentStage = data.stage || 'GUEST';
            this.userMetrics = { ...this.userMetrics, ...data.metrics };
            this.tokenBalance = data.tokenBalance || 100;
        }
    }
    
    saveProgress() {
        localStorage.setItem('hudCardProgress', JSON.stringify({
            stage: this.currentStage,
            metrics: this.userMetrics,
            tokenBalance: this.tokenBalance
        }));
    }
    
    setupEventListeners() {
        // Listen for form completions
        document.addEventListener('identity-completed', (e) => {
            this.updateMetrics('name', e.detail.name);
            this.updateMetrics('place', e.detail.place);
            this.advanceStage('PLACE');
        });
        
        document.addEventListener('mission-completed', (e) => {
            this.updateMetrics('goal', e.detail.goal);
            this.updateMetrics('targetIncome', e.detail.targetIncome);
            this.advanceStage('INCOME');
        });
        
        document.addEventListener('tokens-purchased', (e) => {
            this.tokenBalance += e.detail.amount;
            this.advanceStage('TOKENS');
        });
        
        document.addEventListener('ai-request-made', (e) => {
            this.consumeTokens(e.detail.cost || 1);
        });
    }
    
    updateMetrics(key, value) {
        this.userMetrics[key] = value;
        this.saveProgress();
        this.renderCard();
    }
    
    advanceStage(targetStage) {
        if (this.progressStages[targetStage].level > this.progressStages[this.currentStage].level) {
            this.currentStage = targetStage;
            this.userMetrics.completedTasks = this.progressStages[targetStage].level;
            this.saveProgress();
            this.renderCard();
            this.triggerStageAnimation();
        }
    }
    
    consumeTokens(amount) {
        this.tokenBalance = Math.max(0, this.tokenBalance - amount);
        this.saveProgress();
        this.renderCard();
        
        if (this.tokenBalance <= 10) {
            this.showTokenWarning();
        }
    }
    
    triggerStageAnimation() {
        const card = document.querySelector('.hud-card');
        if (card) {
            card.classList.add('stage-complete');
            setTimeout(() => card.classList.remove('stage-complete'), 1000);
        }
    }
    
    showTokenWarning() {
        const event = new CustomEvent('show-token-warning', {
            detail: { balance: this.tokenBalance }
        });
        document.dispatchEvent(event);
    }
    
    startRealtimeUpdates() {
        setInterval(() => {
            this.updateIncomeSimulation();
        }, 5000);
    }
    
    updateIncomeSimulation() {
        if (this.currentStage === 'TOKENS' && this.userMetrics.currentIncome > 0) {
            this.userMetrics.currentIncome += Math.random() * 10;
            this.renderCard();
        }
    }
    
    renderCard() {
        const cardData = this.buildCardData();
        const event = new CustomEvent('hud-card-update', { detail: cardData });
        document.dispatchEvent(event);
    }
    
    buildCardData() {
        const stage = this.progressStages[this.currentStage];
        const progressPercentage = (stage.level / Object.keys(this.progressStages).length) * 100;
        
        return {
            stage: this.currentStage,
            level: stage.level,
            label: stage.label,
            color: stage.color,
            progressPercentage,
            tokenBalance: this.tokenBalance,
            metrics: this.userMetrics,
            revealedFields: this.getRevealedFields()
        };
    }
    
    getRevealedFields() {
        const stage = this.progressStages[this.currentStage];
        const fields = ['name', 'place', 'goal', 'income', 'tokens'];
        return fields.slice(0, stage.level);
    }
}

// Progressive Disclosure Vue Component
const HUDCard = {
    data() {
        return {
            isVisible: true,
            isExpanded: false,
            cardData: {
                stage: 'GUEST',
                level: 0,
                label: 'Guest',
                color: '#6b7280',
                progressPercentage: 0,
                tokenBalance: 100,
                metrics: {
                    name: '',
                    place: '',
                    goal: '',
                    targetIncome: '',
                    currentIncome: 0,
                    completedTasks: 0,
                    totalTasks: 5
                },
                revealedFields: []
            }
        };
    },
    mounted() {
        this.hudSystem = new HUDCardSystem();
        
        document.addEventListener('hud-card-update', (e) => {
            this.cardData = e.detail;
        });
        
        document.addEventListener('show-token-warning', (e) => {
            this.showTokenWarning(e.detail.balance);
        });
        
        // Initialize with current data
        this.hudSystem.renderCard();
    },
    template: `
        <div class="hud-card" :class="{ 'expanded': isExpanded, 'hidden': !isVisible }">
            <div class="hud-card-header" @click="toggleExpanded">
                <div class="user-avatar">
                    <div class="avatar-ring" :style="{ borderColor: cardData.color }">
                        <span class="avatar-initials">{{ getInitials() }}</span>
                    </div>
                    <div class="status-indicator" :style="{ backgroundColor: cardData.color }"></div>
                </div>
                
                <div class="user-info">
                    <h3 class="user-name">{{ getUserName() }}</h3>
                    <div class="user-stage">{{ cardData.label }}</div>
                </div>
                
                <div class="hud-controls">
                    <div class="token-balance" :class="{ 'warning': cardData.tokenBalance <= 10 }">
                        <span class="token-icon">🪙</span>
                        <span class="token-amount">{{ cardData.tokenBalance }}</span>
                    </div>
                    <button class="expand-btn" :class="{ 'active': isExpanded }">
                        {{ isExpanded ? '▼' : '▶' }}
                    </button>
                </div>
            </div>
            
            <div class="hud-card-body" v-if="isExpanded">
                <div class="progress-section">
                    <div class="progress-bar">
                        <div class="progress-fill" 
                             :style="{ width: cardData.progressPercentage + '%', backgroundColor: cardData.color }">
                        </div>
                    </div>
                    <span class="progress-text">{{ cardData.level }}/{{ Object.keys(hudSystem?.progressStages || {}).length }} Complete</span>
                </div>
                
                <div class="metrics-grid">
                    <div class="metric-item" v-if="cardData.revealedFields.includes('name')">
                        <div class="metric-label">Who</div>
                        <div class="metric-value">{{ cardData.metrics.name || 'Not set' }}</div>
                    </div>
                    
                    <div class="metric-item" v-if="cardData.revealedFields.includes('place')">
                        <div class="metric-label">Where</div>
                        <div class="metric-value">{{ cardData.metrics.place || 'Not set' }}</div>
                    </div>
                    
                    <div class="metric-item" v-if="cardData.revealedFields.includes('goal')">
                        <div class="metric-label">What</div>
                        <div class="metric-value">{{ cardData.metrics.goal || 'Not set' }}</div>
                    </div>
                    
                    <div class="metric-item" v-if="cardData.revealedFields.includes('income')">
                        <div class="metric-label">Target</div>
                        <div class="metric-value">{{ formatIncome(cardData.metrics.targetIncome) }}</div>
                    </div>
                    
                    <div class="metric-item" v-if="cardData.revealedFields.includes('tokens')">
                        <div class="metric-label">Active</div>
                        <div class="metric-value">{{ formatIncome(cardData.metrics.currentIncome) }}</div>
                    </div>
                </div>
                
                <div class="action-buttons">
                    <button class="hud-btn primary" v-if="cardData.level < 5" @click="continueOnboarding">
                        Continue Setup
                    </button>
                    <button class="hud-btn secondary" v-if="cardData.tokenBalance <= 20" @click="buyTokens">
                        Buy Tokens
                    </button>
                </div>
            </div>
        </div>
    `,
    methods: {
        toggleExpanded() {
            this.isExpanded = !this.isExpanded;
        },
        
        getInitials() {
            const name = this.cardData.metrics.name;
            if (!name) return '?';
            return name.split(' ').map(n => n[0]).join('').toUpperCase();
        },
        
        getUserName() {
            return this.cardData.metrics.name || 'Guest User';
        },
        
        formatIncome(amount) {
            if (!amount) return '€0';
            return new Intl.NumberFormat('en-EU', {
                style: 'currency',
                currency: 'EUR',
                minimumFractionDigits: 0
            }).format(amount);
        },
        
        continueOnboarding() {
            // Emit event to continue onboarding
            const event = new CustomEvent('continue-onboarding', {
                detail: { currentStage: this.cardData.stage }
            });
            document.dispatchEvent(event);
        },
        
        buyTokens() {
            // Emit event to open token purchase
            const event = new CustomEvent('open-token-purchase', {
                detail: { currentBalance: this.cardData.tokenBalance }
            });
            document.dispatchEvent(event);
        },
        
        showTokenWarning(balance) {
            // Show warning animation
            const tokenElement = document.querySelector('.token-balance');
            if (tokenElement) {
                tokenElement.classList.add('warning-pulse');
                setTimeout(() => tokenElement.classList.remove('warning-pulse'), 3000);
            }
        }
    }
};

// Export for use in other modules
window.HUDCard = HUDCard;
window.HUDCardSystem = HUDCardSystem;