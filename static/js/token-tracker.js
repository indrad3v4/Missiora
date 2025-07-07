/**
 * Token Tracker with Web3 Crypto Payment Integration
 * Tracks OpenAI API costs and enables crypto payments
 */

export class TokenTracker {
    constructor() {
        this.balance = 0;
        this.totalSpent = 0;
        this.apiCallCount = 0;
        this.sessionStart = Date.now();
        this.onBalanceUpdate = null;
        this.onPaymentRequired = null;
        
        this.loadBalance();
        this.createTrackerUI();
        this.setupEventListeners();
    }
    
    loadBalance() {
        const saved = localStorage.getItem('missiora_token_balance');
        if (saved) {
            const data = JSON.parse(saved);
            this.balance = data.balance || 0;
            this.totalSpent = data.totalSpent || 0;
            this.apiCallCount = data.apiCallCount || 0;
        } else {
            // New users get 10 free tokens
            this.balance = 10;
            this.saveBalance();
        }
    }
    
    saveBalance() {
        const data = {
            balance: this.balance,
            totalSpent: this.totalSpent,
            apiCallCount: this.apiCallCount,
            lastUpdate: Date.now()
        };
        localStorage.setItem('missiora_token_balance', JSON.stringify(data));
    }
    
    createTrackerUI() {
        this.trackerElement = document.createElement('div');
        this.trackerElement.className = 'token-tracker';
        this.trackerElement.innerHTML = `
            <div class="token-balance">
                <span class="token-icon">🪙</span>
                <span class="token-amount">${this.balance.toFixed(2)}</span>
                <span class="token-label">tokens</span>
            </div>
            <div class="api-stats">
                <span class="api-count">${this.apiCallCount} calls</span>
                <span class="spent-amount">€${this.totalSpent.toFixed(2)} spent</span>
            </div>
            <button class="token-refill-btn" onclick="tokenTracker.showPaymentModal()">
                Add Tokens
            </button>
        `;
        
        document.body.appendChild(this.trackerElement);
        
        // Make it globally accessible
        window.tokenTracker = this;
    }
    
    setupEventListeners() {
        // Listen for API calls
        window.addEventListener('api:call-started', (event) => {
            this.trackAPICall(event.detail);
        });
        
        // Listen for vision analysis
        window.addEventListener('vision:analysis-started', () => {
            this.trackVisionAnalysis();
        });
        
        // Listen for agent responses
        window.addEventListener('agent:response-generated', (event) => {
            this.trackAgentResponse(event.detail);
        });
    }
    
    trackAPICall(details) {
        const cost = this.calculateAPICost(details);
        this.deductTokens(cost, 'API Call');
    }
    
    trackVisionAnalysis() {
        // Vision analysis costs more due to image processing
        this.deductTokens(0.1, 'Vision Analysis');
    }
    
    trackAgentResponse(details) {
        const cost = this.calculateResponseCost(details);
        this.deductTokens(cost, 'Agent Response');
    }
    
    calculateAPICost(details) {
        // GPT-4o pricing: $0.005 per 1K input tokens, $0.015 per 1K output tokens
        const inputCost = (details.inputTokens || 1000) / 1000 * 0.005;
        const outputCost = (details.outputTokens || 500) / 1000 * 0.015;
        return inputCost + outputCost;
    }
    
    calculateResponseCost(details) {
        // Estimate based on message length
        const estimatedTokens = Math.max(500, (details.messageLength || 0) * 1.3);
        return estimatedTokens / 1000 * 0.015; // Output token pricing
    }
    
    deductTokens(amount, source) {
        this.balance -= amount;
        this.totalSpent += amount;
        this.apiCallCount++;
        
        this.updateUI();
        this.saveBalance();
        
        if (this.onBalanceUpdate) {
            this.onBalanceUpdate(this.balance, amount, source);
        }
        
        // Check if balance is low
        if (this.balance <= 1) {
            this.showLowBalanceWarning();
        }
        
        if (this.balance <= 0) {
            this.handleInsufficientFunds();
        }
    }
    
    addTokens(amount, source = 'Purchase') {
        this.balance += amount;
        this.updateUI();
        this.saveBalance();
        
        this.showSuccessMessage(`Added ${amount.toFixed(2)} tokens!`);
        
        if (this.onBalanceUpdate) {
            this.onBalanceUpdate(this.balance, amount, source);
        }
    }
    
    updateUI() {
        if (this.trackerElement) {
            const balanceEl = this.trackerElement.querySelector('.token-amount');
            const countEl = this.trackerElement.querySelector('.api-count');
            const spentEl = this.trackerElement.querySelector('.spent-amount');
            
            if (balanceEl) balanceEl.textContent = this.balance.toFixed(2);
            if (countEl) countEl.textContent = `${this.apiCallCount} calls`;
            if (spentEl) spentEl.textContent = `€${this.totalSpent.toFixed(2)} spent`;
            
            // Update color based on balance
            this.trackerElement.className = `token-tracker ${this.getBalanceStatus()}`;
        }
    }
    
    getBalanceStatus() {
        if (this.balance <= 0) return 'empty';
        if (this.balance <= 1) return 'low';
        if (this.balance <= 5) return 'medium';
        return 'good';
    }
    
    showLowBalanceWarning() {
        this.showNotification('⚠️ Low token balance! Consider adding more tokens.', 'warning');
    }
    
    handleInsufficientFunds() {
        this.showNotification('❌ Insufficient tokens! Please add more to continue.', 'error');
        
        if (this.onPaymentRequired) {
            this.onPaymentRequired();
        } else {
            this.showPaymentModal();
        }
    }
    
    showPaymentModal() {
        const modal = document.createElement('div');
        modal.className = 'token-payment-modal';
        modal.innerHTML = `
            <div class="payment-content">
                <div class="payment-header">
                    <h3>Add Tokens</h3>
                    <button class="close-modal" onclick="this.closest('.token-payment-modal').remove()">✕</button>
                </div>
                
                <div class="payment-options">
                    <div class="token-package" data-amount="10" data-price="5">
                        <div class="package-amount">10 Tokens</div>
                        <div class="package-price">€5.00</div>
                        <div class="package-desc">~50 AI interactions</div>
                    </div>
                    
                    <div class="token-package popular" data-amount="50" data-price="20">
                        <div class="package-badge">Popular</div>
                        <div class="package-amount">50 Tokens</div>
                        <div class="package-price">€20.00</div>
                        <div class="package-desc">~250 AI interactions</div>
                    </div>
                    
                    <div class="token-package" data-amount="100" data-price="35">
                        <div class="package-amount">100 Tokens</div>
                        <div class="package-price">€35.00</div>
                        <div class="package-desc">~500 AI interactions</div>
                    </div>
                </div>
                
                <div class="payment-methods">
                    <button class="payment-btn crypto-btn" onclick="tokenTracker.initCryptoPayment()">
                        <span class="payment-icon">₿</span>
                        Pay with Crypto
                    </button>
                    <button class="payment-btn card-btn" onclick="tokenTracker.initCardPayment()">
                        <span class="payment-icon">💳</span>
                        Pay with Card
                    </button>
                </div>
                
                <div class="payment-footer">
                    <p>Secure payments powered by Web3 & Stripe</p>
                </div>
            </div>
        `;
        
        // Add click handlers for packages
        modal.addEventListener('click', (e) => {
            if (e.target.closest('.token-package')) {
                const pkg = e.target.closest('.token-package');
                document.querySelectorAll('.token-package').forEach(p => p.classList.remove('selected'));
                pkg.classList.add('selected');
                
                this.selectedPackage = {
                    tokens: parseInt(pkg.dataset.amount),
                    price: parseFloat(pkg.dataset.price)
                };
            }
        });
        
        document.body.appendChild(modal);
        
        // Auto-select the popular package
        const popularPackage = modal.querySelector('.token-package.popular');
        if (popularPackage) {
            popularPackage.click();
        }
    }
    
    async initCryptoPayment() {
        if (!this.selectedPackage) {
            this.showNotification('Please select a token package first.', 'warning');
            return;
        }
        
        try {
            // Check if MetaMask is available
            if (typeof window.ethereum === 'undefined') {
                this.showNotification('MetaMask not detected. Please install MetaMask to pay with crypto.', 'error');
                return;
            }
            
            // Request account access
            const accounts = await window.ethereum.request({ method: 'eth_requestAccounts' });
            const account = accounts[0];
            
            // Show crypto payment interface
            this.showCryptoPaymentInterface(account);
            
        } catch (error) {
            console.error('Crypto payment initialization failed:', error);
            this.showNotification('Failed to connect to MetaMask. Please try again.', 'error');
        }
    }
    
    showCryptoPaymentInterface(account) {
        const cryptoModal = document.createElement('div');
        cryptoModal.className = 'crypto-payment-modal';
        cryptoModal.innerHTML = `
            <div class="crypto-content">
                <div class="crypto-header">
                    <h3>Crypto Payment</h3>
                    <button class="close-modal" onclick="this.closest('.crypto-payment-modal').remove()">✕</button>
                </div>
                
                <div class="payment-details">
                    <div class="package-summary">
                        <span>${this.selectedPackage.tokens} Tokens</span>
                        <span>€${this.selectedPackage.price}</span>
                    </div>
                    
                    <div class="wallet-info">
                        <span class="wallet-label">Connected Wallet:</span>
                        <span class="wallet-address">${account.substring(0, 6)}...${account.substring(38)}</span>
                    </div>
                    
                    <div class="payment-instruction">
                        Send <strong>€${this.selectedPackage.price} worth of ETH</strong> to:
                    </div>
                    
                    <div class="payment-address">
                        <input type="text" value="0x742d35c5FE8ED7B8D3E93a4Ff5C8E1B3..." readonly>
                        <button onclick="navigator.clipboard.writeText(this.previousElementSibling.value)">Copy</button>
                    </div>
                </div>
                
                <div class="crypto-actions">
                    <button class="confirm-payment-btn" onclick="tokenTracker.confirmCryptoPayment()">
                        Confirm Payment
                    </button>
                    <button class="cancel-payment-btn" onclick="this.closest('.crypto-payment-modal').remove()">
                        Cancel
                    </button>
                </div>
            </div>
        `;
        
        document.body.appendChild(cryptoModal);
    }
    
    async confirmCryptoPayment() {
        // Simulate payment confirmation
        this.showNotification('Processing payment...', 'info');
        
        // In a real implementation, you would:
        // 1. Monitor the blockchain for the transaction
        // 2. Verify the payment amount
        // 3. Add tokens to the user's account
        
        setTimeout(() => {
            this.addTokens(this.selectedPackage.tokens, 'Crypto Payment');
            document.querySelector('.crypto-payment-modal')?.remove();
            document.querySelector('.token-payment-modal')?.remove();
            this.showSuccessMessage(`Successfully added ${this.selectedPackage.tokens} tokens!`);
        }, 2000);
    }
    
    async initCardPayment() {
        if (!this.selectedPackage) {
            this.showNotification('Please select a token package first.', 'warning');
            return;
        }
        
        // Simulate card payment (would integrate with Stripe in production)
        this.showNotification('Redirecting to Stripe...', 'info');
        
        setTimeout(() => {
            this.addTokens(this.selectedPackage.tokens, 'Card Payment');
            document.querySelector('.token-payment-modal')?.remove();
            this.showSuccessMessage(`Successfully added ${this.selectedPackage.tokens} tokens!`);
        }, 1500);
    }
    
    showNotification(message, type = 'info') {
        const notification = document.createElement('div');
        notification.className = `token-notification ${type}`;
        notification.textContent = message;
        notification.style.cssText = `
            position: fixed;
            top: 100px;
            right: 20px;
            background: ${type === 'error' ? '#ef4444' : type === 'warning' ? '#f59e0b' : type === 'success' ? '#10b981' : '#3b82f6'};
            color: white;
            padding: 1rem;
            border-radius: 8px;
            z-index: 1000;
            max-width: 300px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        `;
        
        document.body.appendChild(notification);
        
        setTimeout(() => {
            notification.remove();
        }, 5000);
    }
    
    showSuccessMessage(message) {
        this.showNotification(message, 'success');
    }
    
    getStats() {
        return {
            balance: this.balance,
            totalSpent: this.totalSpent,
            apiCallCount: this.apiCallCount,
            sessionDuration: Date.now() - this.sessionStart,
            averageCostPerCall: this.apiCallCount > 0 ? this.totalSpent / this.apiCallCount : 0
        };
    }
    
    destroy() {
        if (this.trackerElement) {
            this.trackerElement.remove();
        }
        
        // Remove global reference
        if (window.tokenTracker === this) {
            delete window.tokenTracker;
        }
    }
}

// Add CSS for token payment modal
const style = document.createElement('style');
style.textContent = `
    .token-payment-modal, .crypto-payment-modal {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0, 0, 0, 0.7);
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 2000;
    }
    
    .payment-content, .crypto-content {
        background: white;
        border-radius: 16px;
        padding: 2rem;
        max-width: 500px;
        width: 90%;
        max-height: 80vh;
        overflow-y: auto;
    }
    
    .payment-header, .crypto-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 2rem;
        border-bottom: 1px solid #e2e8f0;
        padding-bottom: 1rem;
    }
    
    .close-modal {
        background: none;
        border: none;
        font-size: 1.5rem;
        cursor: pointer;
        color: #6b7280;
    }
    
    .payment-options {
        display: grid;
        gap: 1rem;
        margin-bottom: 2rem;
    }
    
    .token-package {
        border: 2px solid #e2e8f0;
        border-radius: 12px;
        padding: 1.5rem;
        cursor: pointer;
        transition: all 0.2s ease;
        position: relative;
    }
    
    .token-package:hover {
        border-color: #4fd1c7;
        background: rgba(79, 209, 199, 0.05);
    }
    
    .token-package.selected {
        border-color: #4fd1c7;
        background: rgba(79, 209, 199, 0.1);
    }
    
    .token-package.popular {
        border-color: #10b981;
        background: rgba(16, 185, 129, 0.05);
    }
    
    .package-badge {
        position: absolute;
        top: -8px;
        right: 16px;
        background: #10b981;
        color: white;
        padding: 0.25rem 0.75rem;
        border-radius: 12px;
        font-size: 0.8rem;
        font-weight: 600;
    }
    
    .package-amount {
        font-size: 1.25rem;
        font-weight: 700;
        color: #2d3748;
        margin-bottom: 0.5rem;
    }
    
    .package-price {
        font-size: 1.5rem;
        font-weight: 800;
        color: #4fd1c7;
        margin-bottom: 0.25rem;
    }
    
    .package-desc {
        color: #6b7280;
        font-size: 0.9rem;
    }
    
    .payment-methods {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 1rem;
        margin-bottom: 2rem;
    }
    
    .payment-btn {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 0.5rem;
        padding: 1rem;
        border: 2px solid;
        border-radius: 12px;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.2s ease;
        background: transparent;
    }
    
    .crypto-btn {
        border-color: #f59e0b;
        color: #f59e0b;
    }
    
    .crypto-btn:hover {
        background: rgba(245, 158, 11, 0.1);
    }
    
    .card-btn {
        border-color: #3b82f6;
        color: #3b82f6;
    }
    
    .card-btn:hover {
        background: rgba(59, 130, 246, 0.1);
    }
    
    .payment-footer {
        text-align: center;
        color: #6b7280;
        font-size: 0.9rem;
    }
    
    .token-tracker.empty {
        border: 2px solid #ef4444;
        background: rgba(239, 68, 68, 0.1);
    }
    
    .token-tracker.low {
        border: 2px solid #f59e0b;
        background: rgba(245, 158, 11, 0.1);
    }
    
    .token-tracker.medium {
        border: 2px solid #10b981;
        background: rgba(16, 185, 129, 0.1);
    }
    
    .token-tracker.good {
        border: 2px solid #22d3ee;
        background: rgba(34, 211, 238, 0.1);
    }
`;
document.head.appendChild(style);