/**
 * Enhanced Camera Integration with CLIP Vision Analysis
 * Handles camera feed, object detection, and AR overlays
 */

export class CameraIntegration {
    constructor() {
        this.stream = null;
        this.videoElement = null;
        this.canvasElement = null;
        this.isActive = false;
        this.hasPermission = false;
        this.analysisInterval = null;
        this.detectedObjects = [];
        this.onObjectDetection = null;
        
        this.init();
    }
    
    async init() {
        this.createVideoElement();
        this.createCanvasElement();
        await this.requestCameraAccess();
        this.startObjectDetection();
    }
    
    createVideoElement() {
        this.videoElement = document.createElement('video');
        this.videoElement.setAttribute('playsinline', '');
        this.videoElement.setAttribute('autoplay', '');
        this.videoElement.setAttribute('muted', '');
        this.videoElement.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 100vw;
            height: 100vh;
            object-fit: cover;
            z-index: -1;
            filter: brightness(0.65) contrast(1.1);
            transform: scaleX(-1);
        `;
        
        document.body.appendChild(this.videoElement);
    }
    
    createCanvasElement() {
        this.canvasElement = document.createElement('canvas');
        this.canvasElement.style.display = 'none';
        document.body.appendChild(this.canvasElement);
    }
    
    async requestCameraAccess() {
        try {
            const constraints = {
                video: {
                    facingMode: 'environment', // Rear camera
                    width: { ideal: 1920 },
                    height: { ideal: 1080 }
                },
                audio: false
            };
            
            this.stream = await navigator.mediaDevices.getUserMedia(constraints);
            this.videoElement.srcObject = this.stream;
            this.hasPermission = true;
            this.isActive = true;
            
            console.log('✓ Camera access granted');
            this.dispatchCameraEvent('camera:ready');
            
        } catch (error) {
            console.warn('Camera access denied or unavailable:', error);
            this.showFallbackBackground();
            this.dispatchCameraEvent('camera:fallback');
        }
    }
    
    showFallbackBackground() {
        document.body.style.background = `
            linear-gradient(135deg, 
                #667eea 0%, 
                #764ba2 25%,
                #f093fb 50%,
                #f5576c 75%,
                #4facfe 100%
            )
        `;
        
        if (this.videoElement) {
            this.videoElement.remove();
        }
    }
    
    captureFrame() {
        if (!this.videoElement || !this.canvasElement) return null;
        
        const canvas = this.canvasElement;
        const context = canvas.getContext('2d');
        
        canvas.width = this.videoElement.videoWidth;
        canvas.height = this.videoElement.videoHeight;
        
        context.drawImage(this.videoElement, 0, 0);
        
        return canvas.toDataURL('image/jpeg', 0.8);
    }
    
    async analyzeFrame() {
        if (!this.hasPermission || !this.isActive) return;
        
        const frameData = this.captureFrame();
        if (!frameData) return;
        
        try {
            const response = await fetch('/api/vision/analyze', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    image: frameData,
                    timestamp: Date.now()
                })
            });
            
            if (response.ok) {
                const analysisResult = await response.json();
                this.handleDetectionResult(analysisResult);
            }
        } catch (error) {
            console.error('Vision analysis failed:', error);
        }
    }
    
    handleDetectionResult(result) {
        this.detectedObjects = result.objects || [];
        
        if (this.onObjectDetection) {
            this.onObjectDetection(result);
        }
        
        this.dispatchCameraEvent('vision:objects-detected', result);
    }
    
    startObjectDetection() {
        // Capture and analyze frame every 2 seconds
        this.analysisInterval = setInterval(() => {
            this.analyzeFrame();
        }, 2000);
    }
    
    stopObjectDetection() {
        if (this.analysisInterval) {
            clearInterval(this.analysisInterval);
            this.analysisInterval = null;
        }
    }
    
    dispatchCameraEvent(eventType, data = {}) {
        window.dispatchEvent(new CustomEvent(eventType, {
            detail: {
                hasCamera: this.hasPermission,
                isActive: this.isActive,
                detectedObjects: this.detectedObjects,
                ...data
            }
        }));
    }
    
    toggleCamera() {
        if (this.isActive) {
            this.stopCamera();
        } else {
            this.requestCameraAccess();
        }
    }
    
    stopCamera() {
        this.stopObjectDetection();
        
        if (this.stream) {
            this.stream.getTracks().forEach(track => track.stop());
            this.stream = null;
        }
        
        if (this.videoElement) {
            this.videoElement.srcObject = null;
        }
        
        this.isActive = false;
        this.showFallbackBackground();
        this.dispatchCameraEvent('camera:stopped');
    }
    
    adjustBrightness(level) {
        if (this.videoElement) {
            this.videoElement.style.filter = `brightness(${level}) contrast(1.1)`;
        }
    }
    
    destroy() {
        this.stopCamera();
        if (this.videoElement) {
            this.videoElement.remove();
        }
        if (this.canvasElement) {
            this.canvasElement.remove();
        }
    }
}