/**
 * AR Overlay Component for Object Detection Visualization
 * Displays bounding boxes, labels, and action menus for detected objects
 */

export class AROverlay {
    constructor() {
        this.overlayContainer = null;
        this.detectedObjects = [];
        this.activeActions = new Map();
        this.onActionSelected = null;
        
        this.init();
    }
    
    init() {
        this.createOverlayContainer();
        this.setupEventListeners();
    }
    
    createOverlayContainer() {
        this.overlayContainer = document.createElement('div');
        this.overlayContainer.className = 'ar-overlay';
        this.overlayContainer.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 100vw;
            height: 100vh;
            pointer-events: none;
            z-index: 20;
        `;
        
        document.body.appendChild(this.overlayContainer);
    }
    
    setupEventListeners() {
        window.addEventListener('vision:objects-detected', (event) => {
            this.updateOverlay(event.detail);
        });
    }
    
    updateOverlay(detectionData) {
        this.detectedObjects = detectionData.objects || [];
        this.clearOverlay();
        
        this.detectedObjects.forEach((object, index) => {
            this.createObjectOverlay(object, index);
        });
    }
    
    clearOverlay() {
        this.overlayContainer.innerHTML = '';
        this.activeActions.clear();
    }
    
    createObjectOverlay(object, index) {
        const objectElement = document.createElement('div');
        objectElement.className = `object-overlay object-${index}`;
        objectElement.style.cssText = `
            position: absolute;
            left: ${object.boundingBox.x}px;
            top: ${object.boundingBox.y}px;
            width: ${object.boundingBox.width}px;
            height: ${object.boundingBox.height}px;
            border: 2px solid ${this.getObjectColor(object.label)};
            border-radius: 8px;
            pointer-events: auto;
            transition: all 0.3s ease;
        `;
        
        // Create label
        const label = document.createElement('div');
        label.className = 'object-label';
        label.textContent = `${object.label} (${Math.round(object.confidence * 100)}%)`;
        label.style.cssText = `
            position: absolute;
            top: -30px;
            left: 0;
            background: ${this.getObjectColor(object.label)};
            color: white;
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 12px;
            font-weight: 600;
            white-space: nowrap;
            box-shadow: 0 2px 8px rgba(0,0,0,0.3);
        `;
        
        objectElement.appendChild(label);
        
        // Add action button for actionable objects
        if (this.isActionableObject(object.label)) {
            const actionButton = this.createActionButton(object, index);
            objectElement.appendChild(actionButton);
        }
        
        this.overlayContainer.appendChild(objectElement);
        
        // Animate in
        setTimeout(() => {
            objectElement.style.opacity = '1';
            objectElement.style.transform = 'scale(1)';
        }, index * 100);
    }
    
    createActionButton(object, index) {
        const button = document.createElement('button');
        button.className = 'action-button';
        button.textContent = '⚡';
        button.style.cssText = `
            position: absolute;
            bottom: -15px;
            right: -15px;
            width: 30px;
            height: 30px;
            border-radius: 50%;
            border: none;
            background: linear-gradient(135deg, #4fd1c7 0%, #06b6d4 100%);
            color: white;
            font-size: 16px;
            cursor: pointer;
            box-shadow: 0 4px 12px rgba(79, 209, 199, 0.4);
            transition: all 0.2s ease;
        `;
        
        button.addEventListener('click', (e) => {
            e.stopPropagation();
            this.showActionMenu(object, index, e.target);
        });
        
        button.addEventListener('mouseenter', () => {
            button.style.transform = 'scale(1.1)';
            button.style.boxShadow = '0 6px 16px rgba(79, 209, 199, 0.6)';
        });
        
        button.addEventListener('mouseleave', () => {
            button.style.transform = 'scale(1)';
            button.style.boxShadow = '0 4px 12px rgba(79, 209, 199, 0.4)';
        });
        
        return button;
    }
    
    showActionMenu(object, index, buttonElement) {
        // Remove existing action menus
        this.hideAllActionMenus();
        
        const menu = document.createElement('div');
        menu.className = 'action-menu';
        menu.style.cssText = `
            position: absolute;
            bottom: 40px;
            right: -50px;
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(20px);
            border: 1px solid rgba(255, 255, 255, 0.3);
            border-radius: 12px;
            padding: 8px;
            min-width: 200px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
            z-index: 100;
        `;
        
        const actions = this.getActionsForObject(object.label);
        
        actions.forEach(action => {
            const actionItem = document.createElement('button');
            actionItem.className = 'action-item';
            actionItem.textContent = action.label;
            actionItem.style.cssText = `
                display: block;
                width: 100%;
                padding: 8px 12px;
                margin: 2px 0;
                border: none;
                border-radius: 6px;
                background: transparent;
                color: #2d3748;
                font-size: 14px;
                text-align: left;
                cursor: pointer;
                transition: background 0.2s ease;
            `;
            
            actionItem.addEventListener('mouseenter', () => {
                actionItem.style.background = 'rgba(79, 209, 199, 0.1)';
            });
            
            actionItem.addEventListener('mouseleave', () => {
                actionItem.style.background = 'transparent';
            });
            
            actionItem.addEventListener('click', () => {
                this.executeAction(action, object);
                this.hideAllActionMenus();
            });
            
            menu.appendChild(actionItem);
        });
        
        buttonElement.appendChild(menu);
        this.activeActions.set(index, menu);
        
        // Auto-hide after 5 seconds
        setTimeout(() => {
            if (this.activeActions.has(index)) {
                this.hideActionMenu(index);
            }
        }, 5000);
    }
    
    hideAllActionMenus() {
        this.activeActions.forEach((menu, index) => {
            this.hideActionMenu(index);
        });
    }
    
    hideActionMenu(index) {
        const menu = this.activeActions.get(index);
        if (menu) {
            menu.remove();
            this.activeActions.delete(index);
        }
    }
    
    isActionableObject(label) {
        const actionableTypes = [
            'business card', 'card', 'qr code', 'whiteboard', 'board', 
            'text', 'document', 'paper', 'book', 'laptop', 'computer',
            'phone', 'person', 'face'
        ];
        
        return actionableTypes.some(type => 
            label.toLowerCase().includes(type)
        );
    }
    
    getActionsForObject(label) {
        const objectType = label.toLowerCase();
        
        if (objectType.includes('card') || objectType.includes('business')) {
            return [
                { id: 'scan_card', label: '📇 Extract Contact Info' },
                { id: 'save_contact', label: '💾 Save to Contacts' },
                { id: 'linkedin_search', label: '🔍 Find on LinkedIn' },
                { id: 'add_reminder', label: '⏰ Set Follow-up Reminder' }
            ];
        }
        
        if (objectType.includes('qr')) {
            return [
                { id: 'scan_qr', label: '📱 Scan QR Code' },
                { id: 'open_url', label: '🌐 Open Link' },
                { id: 'save_info', label: '💾 Save Information' }
            ];
        }
        
        if (objectType.includes('whiteboard') || objectType.includes('board')) {
            return [
                { id: 'ocr_text', label: '📝 Extract Text (OCR)' },
                { id: 'save_notes', label: '📋 Save as Notes' },
                { id: 'create_tasks', label: '✅ Create Tasks' },
                { id: 'add_to_roadmap', label: '🗺️ Add to Roadmap' }
            ];
        }
        
        if (objectType.includes('laptop') || objectType.includes('computer')) {
            return [
                { id: 'productivity_tips', label: '💡 Productivity Tips' },
                { id: 'workspace_analysis', label: '🏢 Analyze Workspace' },
                { id: 'tool_suggestions', label: '🛠️ Tool Recommendations' }
            ];
        }
        
        if (objectType.includes('person') || objectType.includes('face')) {
            return [
                { id: 'networking_tips', label: '🤝 Networking Advice' },
                { id: 'conversation_starters', label: '💬 Conversation Ideas' },
                { id: 'contact_reminder', label: '📱 Set Contact Reminder' }
            ];
        }
        
        // Default actions for text/documents
        return [
            { id: 'read_text', label: '👀 Read Text' },
            { id: 'translate', label: '🌍 Translate' },
            { id: 'summarize', label: '📄 Summarize' }
        ];
    }
    
    async executeAction(action, object) {
        if (this.onActionSelected) {
            this.onActionSelected(action, object);
        }
        
        // Show execution feedback
        this.showActionFeedback(action.label);
        
        try {
            const response = await fetch('/api/vision/action', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    action: action.id,
                    object: object,
                    timestamp: Date.now()
                })
            });
            
            if (response.ok) {
                const result = await response.json();
                this.showActionResult(result);
            }
        } catch (error) {
            console.error('Action execution failed:', error);
            this.showActionError('Action failed. Please try again.');
        }
    }
    
    showActionFeedback(actionLabel) {
        const feedback = document.createElement('div');
        feedback.className = 'action-feedback';
        feedback.textContent = `Executing: ${actionLabel}...`;
        feedback.style.cssText = `
            position: fixed;
            top: 220px;
            left: 50%;
            transform: translateX(-50%);
            background: rgba(79, 209, 199, 0.9);
            color: white;
            padding: 12px 20px;
            border-radius: 20px;
            font-size: 14px;
            font-weight: 600;
            z-index: 1000;
            animation: fadeInOut 3s ease;
        `;
        
        document.body.appendChild(feedback);
        
        setTimeout(() => {
            if (feedback.parentNode) {
                feedback.remove();
            }
        }, 3000);
    }
    
    showActionResult(result) {
        const resultElement = document.createElement('div');
        resultElement.className = 'action-result';
        resultElement.innerHTML = `
            <div class="result-title">${result.title || 'Action Complete'}</div>
            <div class="result-content">${result.message || 'Action executed successfully'}</div>
        `;
        resultElement.style.cssText = `
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(20px);
            border: 1px solid rgba(255, 255, 255, 0.3);
            border-radius: 16px;
            padding: 20px;
            max-width: 400px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
            z-index: 1000;
            pointer-events: auto;
        `;
        
        // Add close button
        const closeButton = document.createElement('button');
        closeButton.textContent = '✕';
        closeButton.style.cssText = `
            position: absolute;
            top: 8px;
            right: 8px;
            background: none;
            border: none;
            font-size: 18px;
            cursor: pointer;
            color: #666;
        `;
        
        closeButton.addEventListener('click', () => {
            resultElement.remove();
        });
        
        resultElement.appendChild(closeButton);
        document.body.appendChild(resultElement);
        
        // Auto-remove after 10 seconds
        setTimeout(() => {
            if (resultElement.parentNode) {
                resultElement.remove();
            }
        }, 10000);
    }
    
    showActionError(message) {
        const errorElement = document.createElement('div');
        errorElement.textContent = message;
        errorElement.style.cssText = `
            position: fixed;
            top: 220px;
            left: 50%;
            transform: translateX(-50%);
            background: rgba(239, 68, 68, 0.9);
            color: white;
            padding: 12px 20px;
            border-radius: 20px;
            font-size: 14px;
            font-weight: 600;
            z-index: 1000;
        `;
        
        document.body.appendChild(errorElement);
        
        setTimeout(() => {
            if (errorElement.parentNode) {
                errorElement.remove();
            }
        }, 3000);
    }
    
    getObjectColor(label) {
        const colorMap = {
            'laptop': '#3b82f6',
            'computer': '#3b82f6',
            'card': '#10b981',
            'business': '#10b981',
            'qr': '#8b5cf6',
            'person': '#f59e0b',
            'face': '#f59e0b',
            'plant': '#22c55e',
            'book': '#ef4444',
            'paper': '#6b7280',
            'whiteboard': '#06b6d4'
        };
        
        const objectType = Object.keys(colorMap).find(key => 
            label.toLowerCase().includes(key)
        );
        
        return colorMap[objectType] || '#64748b';
    }
    
    destroy() {
        if (this.overlayContainer) {
            this.overlayContainer.remove();
        }
        this.activeActions.clear();
    }
}

// Add CSS animations
const style = document.createElement('style');
style.textContent = `
    @keyframes fadeInOut {
        0% { opacity: 0; transform: translateX(-50%) translateY(-10px); }
        20% { opacity: 1; transform: translateX(-50%) translateY(0); }
        80% { opacity: 1; transform: translateX(-50%) translateY(0); }
        100% { opacity: 0; transform: translateX(-50%) translateY(-10px); }
    }
    
    .object-overlay {
        opacity: 0;
        transform: scale(0.8);
    }
    
    .action-menu {
        animation: slideUp 0.2s ease;
    }
    
    @keyframes slideUp {
        from {
            opacity: 0;
            transform: translateY(10px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
`;
document.head.appendChild(style);