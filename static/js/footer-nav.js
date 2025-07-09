/**
 * TRIZ Footer Navigation Component
 * Three-button system: Identity | Mission | Roadmap
 */

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

export { FooterNav };