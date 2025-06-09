/**
 * Camera Integration for Mixed Reality Experience
 * Handles camera feed, AR overlay, and spatial UI positioning
 */

export class CameraIntegration {
    constructor() {
        this.stream = null;
        this.videoElement = null;
        this.isActive = false;
        this.hasPermission = false;
        
        this.init();
    }
    
    async init() {
        this.createVideoElement();
        await this.requestCameraAccess();
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
        // Gradient fallback when camera unavailable
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
    
    dispatchCameraEvent(eventType) {
        window.dispatchEvent(new CustomEvent(eventType, {
            detail: {
                hasCamera: this.hasPermission,
                isActive: this.isActive
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
    }
}