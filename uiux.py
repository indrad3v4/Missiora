#!/usr/bin/env python3
"""
MISSIORA Mixed Reality Tamagotchi Transformation Script
Transforms existing Flask/Vue.js app into immersive MR experience with evolving AI agent
"""

import os
import re
import json
from pathlib import Path

def ensure_directory(path):
    """Create directory if it doesn't exist"""
    Path(path).mkdir(parents=True, exist_ok=True)

def write_file(filepath, content):
    """Write content to file, creating directories if needed"""
    ensure_directory(os.path.dirname(filepath))
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"✓ Created/Updated: {filepath}")

def patch_file(filepath, pattern, replacement, flags=0):
    """Apply regex patch to existing file"""
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        new_content = re.sub(pattern, replacement, content, flags=flags)
        
        if new_content != content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"✓ Patched: {filepath}")
        else:
            print(f"⚠ No changes needed: {filepath}")
    else:
        print(f"✗ File not found: {filepath}")

def main():
    print("🚀 Starting MISSIORA CLIP Vision + Agent Action System...")
    
    # 1. Enhanced Vision Analysis Flask Route
    vision_route = '''
@app.route('/api/vision/analyze', methods=['POST'])
@login_required
def analyze_vision():
    """Analyze camera frame with CLIP + CV for object detection and actions"""
    try:
        data = request.get_json()
        frame_data = data.get('frame')
        
        if not frame_data:
            return jsonify({'error': 'No frame data provided'}), 400
        
        # Decode base64 image
        import base64
        import cv2
        import numpy as np
        from PIL import Image
        import io
        
        # Remove data URL prefix
        image_data = frame_data.split(',')[1]
        image_bytes = base64.b64decode(image_data)
        
        # Convert to OpenCV format
        image = Image.open(io.BytesIO(image_bytes))
        cv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        
        # CLIP Analysis for object recognition
        clip_results = analyze_with_clip(image)
        
        # Computer Vision for actionable objects
        cv_results = detect_actionable_objects(cv_image)
        
        # Agent personality response
        agent_response = generate_agent_response(clip_results, cv_results)
        
        return jsonify({
            'objects': clip_results,
            'actions': cv_results,
            'agent_response': agent_response,
            'timestamp': time.time()
        })
        
    except Exception as e:
        logger.error(f"Vision analysis error: {e}")
        return jsonify({'error': 'Analysis failed'}), 500

def analyze_with_clip(image):
    """Use CLIP to identify objects in image"""
    # Placeholder for CLIP integration
    # In production, this would use OpenAI's CLIP model
    common_objects = [
        'laptop', 'computer', 'phone', 'plant', 'book', 'coffee', 'notebook',
        'business card', 'whiteboard', 'monitor', 'keyboard', 'mouse'
    ]
    
    # Mock CLIP analysis - replace with actual CLIP implementation
    detected_objects = [
        {
            'label': 'laptop',
            'confidence': 0.85,
            'position': {'x': 0.5, 'y': 0.3},
            'emotion': 'excited'
        }
    ]
    
    return detected_objects

def detect_actionable_objects(cv_image):
    """Detect QR codes, text, business cards using OpenCV"""
    actions = []
    
    # QR Code Detection
    qr_detector = cv2.QRCodeDetector()
    data, bbox, _ = qr_detector.detectAndDecode(cv_image)
    
    if data:
        actions.append({
            'type': 'qr_code',
            'data': data,
            'bbox': bbox.tolist() if bbox is not None else None,
            'action': 'scan_qr',
            'description': 'QR code detected - tap to scan'
        })
    
    # Text Detection (simplified)
    gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
    # Add OCR detection here using pytesseract or similar
    
    return actions

def generate_agent_response(clip_results, cv_results):
    """Generate personality response based on detected objects"""
    if not clip_results and not cv_results:
        return {
            'message': "I'm looking around... what should we explore? 👀",
            'mood': 'curious',
            'eye_target': None
        }
    
    # Prioritize actionable objects
    if cv_results:
        action = cv_results[0]
        if action['type'] == 'qr_code':
            return {
                'message': "I see a QR code! Should I help you scan it? 📱",
                'mood': 'excited',
                'eye_target': action.get('bbox')
            }
    
    # React to CLIP objects
    if clip_results:
        obj = clip_results[0]
        responses = {
            'laptop': "A laptop! Ready to build something amazing? 💻✨",
            'plant': "Beautiful plant! Growth takes time, just like your business 🌱",
            'book': "Learning time! What insights are you gaining? 📚",
            'coffee': "Fuel for creativity! What's brewing in your mind? ☕"
        }
        
        return {
            'message': responses.get(obj['label'], f"Interesting {obj['label']}! How does this inspire your mission? 🤔"),
            'mood': obj.get('emotion', 'curious'),
            'eye_target': obj.get('position')
        }
    
    return {
        'message': "I see something new! Tell me about it 👀",
        'mood': 'curious',
        'eye_target': None
    }
'''
    
    write_file('vision_routes.py', vision_route)
    
    # 2. Enhanced Camera Integration with Vision Analysis
    camera_integration_js = '''/**
 * Enhanced Camera Integration with CLIP Vision Analysis
 */

class CameraIntegration {
    constructor() {
        this.videoElement = null;
        this.isActive = false;
        this.analysisInterval = null;
        this.overlayCanvas = null;
        this.overlayContext = null;
    }
    
    async initialize() {
        try {
            const stream = await navigator.mediaDevices.getUserMedia({
                video: { 
                    width: { ideal: 1280 },
                    height: { ideal: 720 },
                    facingMode: 'environment'
                }
            });
            
            this.videoElement = document.getElementById('camera-feed');
            if (this.videoElement) {
                this.videoElement.srcObject = stream;
                this.videoElement.play();
                this.isActive = true;
                
                // Initialize overlay canvas
                this.setupOverlay();
                
                // Start vision analysis
                this.startVisionAnalysis();
            }
            
            return true;
        } catch (error) {
            console.error('Camera access failed:', error);
            return false;
        }
    }
    
    setupOverlay() {
        this.overlayCanvas = document.getElementById('vision-overlay');
        if (this.overlayCanvas && this.videoElement) {
            this.overlayContext = this.overlayCanvas.getContext('2d');
            
            // Match video dimensions
            const resizeOverlay = () => {
                this.overlayCanvas.width = this.videoElement.videoWidth;
                this.overlayCanvas.height = this.videoElement.videoHeight;
            };
            
            this.videoElement.addEventListener('loadedmetadata', resizeOverlay);
            window.addEventListener('resize', resizeOverlay);
        }
    }
    
    startVisionAnalysis() {
        if (this.analysisInterval) {
            clearInterval(this.analysisInterval);
        }
        
        this.analysisInterval = setInterval(() => {
            this.analyzeCurrentFrame();
        }, 2000); // Analyze every 2 seconds
    }
    
    async analyzeCurrentFrame() {
        if (!this.videoElement || !this.isActive) return;
        
        const frameData = this.captureFrame();
        if (!frameData) return;
        
        try {
            const response = await fetch('/api/vision/analyze', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    frame: frameData
                })
            });
            
            if (response.ok) {
                const analysis = await response.json();
                this.displayVisionResults(analysis);
                this.notifyAgent(analysis);
            }
        } catch (error) {
            console.warn('Vision analysis failed:', error);
        }
    }
    
    captureFrame() {
        if (!this.videoElement) return null;
        
        const canvas = document.createElement('canvas');
        const ctx = canvas.getContext('2d');
        
        canvas.width = this.videoElement.videoWidth;
        canvas.height = this.videoElement.videoHeight;
        
        ctx.drawImage(this.videoElement, 0, 0);
        return canvas.toDataURL('image/jpeg', 0.8);
    }
    
    displayVisionResults(analysis) {
        if (!this.overlayContext) return;
        
        // Clear previous overlays
        this.overlayContext.clearRect(0, 0, this.overlayCanvas.width, this.overlayCanvas.height);
        
        // Draw object labels and bounding boxes
        analysis.objects?.forEach(obj => {
            this.drawObjectLabel(obj);
        });
        
        // Draw action indicators
        analysis.actions?.forEach(action => {
            this.drawActionIndicator(action);
        });
    }
    
    drawObjectLabel(obj) {
        const ctx = this.overlayContext;
        const canvas = this.overlayCanvas;
        
        // Convert normalized position to canvas coordinates
        const x = obj.position.x * canvas.width;
        const y = obj.position.y * canvas.height;
        
        // Draw floating label
        ctx.fillStyle = 'rgba(255, 255, 255, 0.9)';
        ctx.strokeStyle = 'rgba(0, 0, 0, 0.5)';
        ctx.lineWidth = 2;
        ctx.font = '16px Arial';
        
        const text = `${obj.label} (${Math.round(obj.confidence * 100)}%)`;
        const textWidth = ctx.measureText(text).width;
        
        // Background
        ctx.fillRect(x - textWidth/2 - 10, y - 30, textWidth + 20, 25);
        ctx.strokeRect(x - textWidth/2 - 10, y - 30, textWidth + 20, 25);
        
        // Text
        ctx.fillStyle = 'black';
        ctx.fillText(text, x - textWidth/2, y - 10);
        
        // Indicator dot
        ctx.fillStyle = this.getMoodColor(obj.emotion);
        ctx.beginPath();
        ctx.arc(x, y, 8, 0, 2 * Math.PI);
        ctx.fill();
    }
    
    drawActionIndicator(action) {
        if (!action.bbox) return;
        
        const ctx = this.overlayContext;
        const bbox = action.bbox[0]; // First bounding box
        
        // Draw bounding box
        ctx.strokeStyle = '#00ff00';
        ctx.lineWidth = 3;
        ctx.strokeRect(bbox[0], bbox[1], bbox[2] - bbox[0], bbox[3] - bbox[1]);
        
        // Draw action button
        const centerX = (bbox[0] + bbox[2]) / 2;
        const centerY = bbox[1] - 20;
        
        ctx.fillStyle = 'rgba(0, 255, 0, 0.8)';
        ctx.fillRect(centerX - 40, centerY - 15, 80, 30);
        
        ctx.fillStyle = 'white';
        ctx.font = '12px Arial';
        ctx.fillText(action.description, centerX - 35, centerY + 5);
    }
    
    getMoodColor(emotion) {
        const colors = {
            'excited': '#ff6b6b',
            'curious': '#4ecdc4',
            'happy': '#ffe66d',
            'thinking': '#a8e6cf'
        };
        return colors[emotion] || '#cccccc';
    }
    
    notifyAgent(analysis) {
        // Notify the Tamagotchi agent about vision results
        const event = new CustomEvent('visionAnalysis', {
            detail: analysis
        });
        window.dispatchEvent(event);
    }
    
    destroy() {
        if (this.analysisInterval) {
            clearInterval(this.analysisInterval);
        }
        
        if (this.videoElement && this.videoElement.srcObject) {
            const tracks = this.videoElement.srcObject.getTracks();
            tracks.forEach(track => track.stop());
        }
        
        this.isActive = false;
    }
}'''
    
    write_file('static/js/camera-integration.js', camera_integration_js)module.js';

export class TamagotchiAgent {
    constructor(container) {
        this.container = container;
        this.stage = 'seed';
        this.completion = 0;
        this.mood = 'neutral';
        this.size = 1.0;
        this.color = '#22d3ee';
        
        this.initThreeJS();
        this.createAgent();
        this.animate();
    }
    
    initThreeJS() {
        // Scene setup
        this.scene = new THREE.Scene();
        this.camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
        this.renderer = new THREE.WebGLRenderer({ 
            alpha: true, 
            antialias: true,
            canvas: this.container
        });
        
        this.renderer.setSize(window.innerWidth, window.innerHeight);
        this.renderer.setClearColor(0x000000, 0);
        
        // Lighting
        const ambientLight = new THREE.AmbientLight(0xffffff, 0.6);
        this.scene.add(ambientLight);
        
        const directionalLight = new THREE.DirectionalLight(0xffffff, 0.8);
        directionalLight.position.set(1, 1, 1);
        this.scene.add(directionalLight);
        
        this.camera.position.z = 5;
    }
    
    createAgent() {
        // Agent geometry based on stage
        const stageConfig = this.getStageConfig();
        
        // Core body
        const bodyGeometry = new THREE.SphereGeometry(stageConfig.size, 32, 32);
        const bodyMaterial = new THREE.MeshPhongMaterial({ 
            color: stageConfig.color,
            transparent: true,
            opacity: 0.8,
            emissive: stageConfig.color,
            emissiveIntensity: 0.2
        });
        
        this.agentBody = new THREE.Mesh(bodyGeometry, bodyMaterial);
        
        // Eyes
        this.createEyes();
        
        // Growth elements based on stage
        this.createGrowthElements();
        
        // Group all parts
        this.agentGroup = new THREE.Group();
        this.agentGroup.add(this.agentBody);
        this.scene.add(this.agentGroup);
        
        // Position in space
        this.updateSpatialPosition();
    }
    
    createEyes() {
        const eyeGeometry = new THREE.SphereGeometry(0.1, 16, 16);
        const eyeMaterial = new THREE.MeshBasicMaterial({ color: 0xffffff });
        
        this.leftEye = new THREE.Mesh(eyeGeometry, eyeMaterial);
        this.rightEye = new THREE.Mesh(eyeGeometry, eyeMaterial);
        
        this.leftEye.position.set(-0.2, 0.2, 0.8);
        this.rightEye.position.set(0.2, 0.2, 0.8);
        
        this.agentGroup.add(this.leftEye);
        this.agentGroup.add(this.rightEye);
    }
    
    createGrowthElements() {
        // Remove existing growth elements
        if (this.growthElements) {
            this.growthElements.forEach(element => {
                this.agentGroup.remove(element);
            });
        }
        
        this.growthElements = [];
        
        switch(this.stage) {
            case 'seed':
                // Simple core form
                break;
            case 'sprout':
                // Add small tendrils
                this.addTendrils(3);
                break;
            case 'bloom':
                // Add larger tendrils and particles
                this.addTendrils(6);
                this.addParticleHalo();
                break;
            case 'master':
                // Full crown and energy field
                this.addTendrils(12);
                this.addParticleHalo();
                this.addEnergyCrown();
                break;
        }
    }
    
    addTendrils(count) {
        for (let i = 0; i < count; i++) {
            const angle = (i / count) * Math.PI * 2;
            const tendrilGeometry = new THREE.CylinderGeometry(0.02, 0.01, 0.5, 8);
            const tendrilMaterial = new THREE.MeshPhongMaterial({ 
                color: this.color,
                transparent: true,
                opacity: 0.6
            });
            
            const tendril = new THREE.Mesh(tendrilGeometry, tendrilMaterial);
            tendril.position.set(
                Math.cos(angle) * 0.8,
                0.3,
                Math.sin(angle) * 0.8
            );
            tendril.rotation.z = angle;
            
            this.growthElements.push(tendril);
            this.agentGroup.add(tendril);
        }
    }
    
    addParticleHalo() {
        const particleCount = 50;
        const particles = new THREE.BufferGeometry();
        const positions = new Float32Array(particleCount * 3);
        
        for (let i = 0; i < particleCount * 3; i += 3) {
            positions[i] = (Math.random() - 0.5) * 4;
            positions[i + 1] = (Math.random() - 0.5) * 4;
            positions[i + 2] = (Math.random() - 0.5) * 4;
        }
        
        particles.setAttribute('position', new THREE.BufferAttribute(positions, 3));
        
        const particleMaterial = new THREE.PointsMaterial({
            color: this.color,
            size: 0.05,
            transparent: true,
            opacity: 0.6
        });
        
        const particleSystem = new THREE.Points(particles, particleMaterial);
        this.growthElements.push(particleSystem);
        this.agentGroup.add(particleSystem);
    }
    
    addEnergyCrown() {
        const crownGeometry = new THREE.RingGeometry(1.2, 1.5, 16);
        const crownMaterial = new THREE.MeshBasicMaterial({
            color: this.color,
            transparent: true,
            opacity: 0.3,
            side: THREE.DoubleSide
        });
        
        const crown = new THREE.Mesh(crownGeometry, crownMaterial);
        crown.position.y = 1.5;
        crown.rotation.x = Math.PI / 2;
        
        this.growthElements.push(crown);
        this.agentGroup.add(crown);
    }
    
    getStageConfig() {
        const stages = {
            seed: { completion: [0, 25], size: 1.0, color: '#22d3ee' },
            sprout: { completion: [26, 50], size: 1.1, color: '#4ade80' },
            bloom: { completion: [51, 80], size: 1.2, color: '#fbbf24' },
            master: { completion: [81, 100], size: 1.3, color: '#9333ea' }
        };
        
        return {
            ...stages[this.stage],
            size: stages[this.stage].size * (1 + (this.completion / 100) * 0.2)
        };
    }
    
    updateCompletion(identityCompletion, missionCompletion, roadmapCompletion) {
        this.completion = Math.round(
            (identityCompletion * 0.33) + 
            (missionCompletion * 0.33) + 
            (roadmapCompletion * 0.34)
        );
        
        // Determine stage
        const newStage = this.completion <= 25 ? 'seed' :
                        this.completion <= 50 ? 'sprout' :
                        this.completion <= 80 ? 'bloom' : 'master';
        
        if (newStage !== this.stage) {
            this.stage = newStage;
            this.evolveAgent();
        }
        
        this.updateAgentSize();
    }
    
    evolveAgent() {
        const stageConfig = this.getStageConfig();
        this.color = stageConfig.color;
        
        // Update materials
        this.agentBody.material.color.setHex(this.color.replace('#', '0x'));
        this.agentBody.material.emissive.setHex(this.color.replace('#', '0x'));
        
        // Recreate growth elements
        this.createGrowthElements();
        
        // Trigger evolution animation
        this.playEvolutionAnimation();
    }
    
    updateAgentSize() {
        const stageConfig = this.getStageConfig();
        const targetScale = stageConfig.size;
        
        // Smooth scaling
        this.agentGroup.scale.lerp(new THREE.Vector3(targetScale, targetScale, targetScale), 0.1);
    }
    
    playEvolutionAnimation() {
        // Flash effect
        const originalIntensity = this.agentBody.material.emissiveIntensity;
        this.agentBody.material.emissiveIntensity = 1.0;
        
        setTimeout(() => {
            this.agentBody.material.emissiveIntensity = originalIntensity;
        }, 500);
        
        // Scale pulse
        const originalScale = this.agentGroup.scale.clone();
        this.agentGroup.scale.multiplyScalar(1.3);
        
        const scaleBack = () => {
            this.agentGroup.scale.lerp(originalScale, 0.1);
            if (this.agentGroup.scale.distanceTo(originalScale) > 0.01) {
                requestAnimationFrame(scaleBack);
            }
        };
        setTimeout(scaleBack, 100);
    }
    
    updateSpatialPosition() {
        // Position agent based on UI focus
        this.agentGroup.position.set(0, 0, 0);
        this.agentGroup.rotation.y += 0.005; // Gentle rotation
    }
    
    playBreathingAnimation() {
        const time = Date.now() * 0.002;
        const breathScale = 1 + Math.sin(time) * 0.05;
        this.agentBody.scale.y = breathScale;
    }
    
    playMoodAnimation(mood) {
        this.mood = mood;
        
        switch(mood) {
            case 'happy':
                this.leftEye.scale.set(1.2, 0.8, 1);
                this.rightEye.scale.set(1.2, 0.8, 1);
                break;
            case 'excited':
                this.leftEye.scale.set(1.5, 1.5, 1);
                this.rightEye.scale.set(1.5, 1.5, 1);
                break;
            case 'thinking':
                this.leftEye.scale.set(0.5, 1.2, 1);
                this.rightEye.scale.set(0.5, 1.2, 1);
                break;
            default:
                this.leftEye.scale.set(1, 1, 1);
                this.rightEye.scale.set(1, 1, 1);
        }
    }
    
    getPersonalityMessage() {
        const messages = {
            seed: [
                "I'm just beginning to understand you! 🌱",
                "Let's plant the seeds of your mission! 🌱",
                "Tell me more about who you are! 🌱"
            ],
            sprout: [
                "I'm growing! Your mission is becoming clearer 🌿",
                "Keep feeding me insights! 🌿", 
                "I can feel your purpose taking shape! 🌿"
            ],
            bloom: [
                "Look how far we've come! 🌸",
                "Your mission is flourishing! 🌸",
                "We're making beautiful progress! 🌸"
            ],
            master: [
                "We've achieved mastery together! 🌟",
                "Ready for the next challenge? 🌟",
                "Your entrepreneurial spirit shines bright! 🌟"
            ]
        };
        
        const stageMessages = messages[this.stage];
        return stageMessages[Math.floor(Math.random() * stageMessages.length)];
    }
    
    animate() {
        requestAnimationFrame(() => this.animate());
        
        this.playBreathingAnimation();
        this.updateSpatialPosition();
        
        // Animate growth elements
        if (this.growthElements) {
            this.growthElements.forEach((element, index) => {
                if (element.type === 'Points') {
                    element.rotation.y += 0.01;
                } else {
                    element.rotation.z += 0.02 * (index + 1);
                }
            });
        }
        
        this.renderer.render(this.scene, this.camera);
    }
    
    handleResize() {
        this.camera.aspect = window.innerWidth / window.innerHeight;
        this.camera.updateProjectionMatrix();
        this.renderer.setSize(window.innerWidth, window.innerHeight);
    }
    
    destroy() {
        if (this.renderer) {
            this.renderer.dispose();
        }
        if (this.agentGroup) {
            this.scene.remove(this.agentGroup);
        }
    }
}'''
    
    write_file('static/js/tamagotchi-agent.js', agent_renderer_js)
    
    # 2. Create Camera Integration Component
    camera_integration_js = '''/**
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
}'''
    
    write_file('static/js/camera-integration.js', camera_integration_js)
    
    # 3. Create Enhanced Vue Components with MR Features
    enhanced_vue_components = '''/**
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

export { MainApp, HeaderView, IdentityView, MissionView, RoadmapView };'''
    
    write_file('static/js/vue-components.js', enhanced_vue_components)
    
    # 4. Create MR Glassmorphism Styles
    mr_styles = '''/**
 * Mixed Reality Glassmorphism Styles for MISSIORA
 * Mobile-first 1080×1920px optimized design
 */

/* Base MR App Structure */
.mr-app {
    position: relative;
    width: 100vw;
    height: 100vh;
    overflow: hidden;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

/* Agent Canvas - Full screen WebGL overlay */
.agent-canvas {
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    z-index: 1;
    pointer-events: none;
}

/* MR Header - Glassmorphism design */
.mr-header {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    height: 190px;
    background: rgba(255, 255, 255, 0.04);
    backdrop-filter: blur(20px);
    border-bottom: 1px solid rgba(255, 255, 255, 0.15);
    z-index: 10;
    padding: 20px;
}

.header-content {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    height: 100%;
}

.brand-title {
    font-size: 64px;
    font-weight: 800;
    color: #ffffff;
    margin: 0;
    text-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
    letter-spacing: 2px;
}

.user-data-card {
    background: rgba(255, 255, 255, 0.15);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.2);
    border-radius: 20px;
    padding: 16px 20px;
    min-width: 280px;
}

.user-info {
    color: white;
}

.user-name {
    font-size: 18px;
    font-weight: 600;
    display: block;
    margin-bottom: 8px;
}

.user-details {
    display: flex;
    flex-direction: column;
    gap: 4px;
    font-size: 14px;
    opacity: 0.9;
}

.agent-status {
    display: flex;
    align-items: center;
}

.completion-ring {
    width: 80px;
    height: 80px;
    border-radius: 50%;
    border: 4px solid rgba(255, 255, 255, 0.2);
    display: flex;
    align-items: center;
    justify-content: center;
    position: relative;
    background: rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(10px);
}

.completion-text {
    color: white;
    font-weight: 700;
    font-size: 16px;
}

/* Agent Speech Bubble */
.agent-speech-bubble {
    position: fixed;
    background: rgba(255, 255, 255, 0.95);
    backdrop-filter: blur(20px);
    border: 1px solid rgba(255, 255, 255, 0.3);
    border-radius: 25px;
    padding: 16px 20px;
    max-width: 320px;
    z-index: 15;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
    animation: bubbleIn 0.3s ease-out;
}

.agent-speech-bubble.position-top {
    top: 220px;
    left: 50%;
    transform: translateX(-50%);
}

.agent-speech-bubble.position-center {
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
}

.agent-speech-bubble.position-bottom {
    bottom: 200px;
    left: 50%;
    transform: translateX(-50%);
}

.agent-speech-bubble p {
    margin: 0;
    color: #2d3748;
    font-size: 16px;
    line-height: 1.4;
}

.bubble-arrow {
    position: absolute;
    bottom: -10px;
    left: 50%;
    transform: translateX(-50%);
    width: 0;
    height: 0;
    border-left: 10px solid transparent;
    border-right: 10px solid transparent;
    border-top: 10px solid rgba(255, 255, 255, 0.95);
}

@keyframes bubbleIn {
    from {
        opacity: 0;
        transform: translateX(-50%) scale(0.8);
    }
    to {
        opacity: 1;
        transform: translateX(-50%) scale(1);
    }
}

/* Main Content Area */
.mr-main {
    position: fixed;
    top: 190px;
    left: 0;
    right: 0;
    bottom: 140px;
    overflow-y: auto;
    z-index: 5;
    padding: 0;
}

.mr-view {
    min-height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 20px;
}

.view-content {
    width: 100%;
    max-width: 480px;
    background: rgba(255, 255, 255, 0.08);
    backdrop-filter: blur(20px);
    border: 1px solid rgba(255, 255, 255, 0.2);
    border-radius: 24px;
    padding: 32px 24px;
    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.2);
}

.section-header {
    text-align: center;
    margin-bottom: 32px;
}

.section-header h2 {
    color: white;
    font-size: 28px;
    font-weight: 700;
    margin: 0 0 8px 0;
    text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
}

.section-header p {
    color: rgba(255, 255, 255, 0.8);
    font-size: 16px;
    margin: 0;
}

/* Form Elements */
.mr-form {
    display: flex;
    flex-direction: column;
    gap: 24px;
}

.form-group {
    display: flex;
    flex-direction: column;
    gap: 8px;
}

.form-label {
    color: white;
    font-size: 14px;
    font-weight: 600;
    text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3);
}

.mr-input, .mr-select, .mr-textarea {
    background: rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.2);
    border-radius: 12px;
    padding: 16px;
    color: white;
    font-size: 16px;
    transition: all 0.3s ease;
}

.mr-input::placeholder,
.mr-textarea::placeholder {
    color: rgba(255, 255, 255, 0.6);
}

.mr-input:focus,
.mr-select:focus,
.mr-textarea:focus {
    outline: none;
    border-color: rgba(255, 255, 255, 0.4);
    background: rgba(255, 255, 255, 0.15);
    box-shadow: 0 0 0 3px rgba(255, 255, 255, 0.1);
}

.mr-textarea {
    min-height: 100px;
    resize: vertical;
    font-family: inherit;
}

.mr-textarea.large {
    min-height: 120px;
}

.mr-select {
    cursor: pointer;
}

.mr-select option {
    background: #2d3748;
    color: white;
}

/* Buttons */
.mr-button {
    background: linear-gradient(135deg, #4fd1c7 0%, #06b6d4 100%);
    color: white;
    border: none;
    border-radius: 12px;
    padding: 16px 24px;
    font-size: 16px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s ease;
    box-shadow: 0 4px 16px rgba(79, 209, 199, 0.3);
}

.mr-button:hover:not(:disabled) {
    transform: translateY(-2px);
    box-shadow: 0 8px 24px rgba(79, 209, 199, 0.4);
}

.mr-button:disabled {
    opacity: 0.5;
    cursor: not-allowed;
    transform: none;
    box-shadow: none;
}

.mr-button.small {
    padding: 8px 16px;
    font-size: 14px;
}

/* Form Actions */
.form-actions {
    display: flex;
    flex-direction: column;
    gap: 16px;
    margin-top: 8px;
}

.completion-indicator {
    text-align: center;
    color: white;
}

.completion-indicator span {
    font-size: 14px;
    font-weight: 600;
    margin-bottom: 8px;
    display: block;
}

.progress-bar {
    width: 100%;
    height: 8px;
    background: rgba(255, 255, 255, 0.2);
    border-radius: 4px;
    overflow: hidden;
}

.progress-fill {
    height: 100%;
    background: linear-gradient(90deg, #4fd1c7 0%, #06b6d4 100%);
    border-radius: 4px;
    transition: width 0.5s ease;
}

/* Milestones Container */
.milestones-container {
    display: flex;
    flex-direction: column;
    gap: 16px;
    margin-bottom: 24px;
}

.milestone-card {
    display: flex;
    align-items: flex-start;
    gap: 16px;
    background: rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.2);
    border-radius: 16px;
    padding: 20px;
    transition: all 0.3s ease;
}

.milestone-card.completed {
    border-color: #4ade80;
    background: rgba(74, 222, 128, 0.1);
}

.milestone-card.active {
    border-color: #fbbf24;
    background: rgba(251, 191, 36, 0.1);
}

.milestone-icon {
    font-size: 24px;
    width: 40px;
    height: 40px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    background: rgba(255, 255, 255, 0.1);
    flex-shrink: 0;
}

.milestone-content {
    flex: 1;
}

.milestone-content h3 {
    color: white;
    font-size: 18px;
    font-weight: 600;
    margin: 0 0 8px 0;
}

.milestone-content p {
    color: rgba(255, 255, 255, 0.8);
    font-size: 14px;
    line-height: 1.5;
    margin: 0 0 12px 0;
}

.milestone-actions {
    margin-top: 12px;
}

/* Footer Navigation */
.mr-footer {
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    height: 140px;
    background: rgba(0, 0, 0, 0.8);
    backdrop-filter: blur(20px);
    border-top: 1px solid rgba(255, 255, 255, 0.1);
    z-index: 10;
    padding: 20px;
}

.tab-navigation {
    display: flex;
    justify-content: space-around;
    height: 100%;
    max-width: 480px;
    margin: 0 auto;
}

.nav-tab {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    background: none;
    border: none;
    color: rgba(255, 255, 255, 0.6);
    cursor: pointer;
    transition: all 0.3s ease;
    padding: 16px;
    border-radius: 16px;
    position: relative;
    min-width: 100px;
}

.nav-tab:disabled {
    opacity: 0.3;
    cursor: not-allowed;
}

.nav-tab.active {
    color: white;
    background: rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.2);
}

.tab-icon {
    font-size: 32px;
    margin-bottom: 4px;
    display: block;
}

.tab-label {
    font-size: 12px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.completion-dot {
    position: absolute;
    top: 8px;
    right: 8px;
    width: 12px;
    height: 12px;
    border-radius: 50%;
    background: rgba(255, 255, 255, 0.3);
    transition: all 0.3s ease;
}

.completion-dot.filled {
    background: #4ade80;
    box-shadow: 0 0 8px rgba(74, 222, 128, 0.5);
}

/* Responsive Adjustments */
@media (max-width: 480px) {
    .brand-title {
        font-size: 48px;
    }
    
    .user-data-card {
        min-width: 200px;
        padding: 12px 16px;
    }
    
    .user-name {
        font-size: 16px;
    }
    
    .user-details {
        font-size: 12px;
    }
    
    .completion-ring {
        width: 60px;
        height: 60px;
    }
    
    .completion-text {
        font-size: 14px;
    }
    
    .view-content {
        padding: 24px 20px;
    }
    
    .section-header h2 {
        font-size: 24px;
    }
    
    .mr-input, .mr-select, .mr-textarea {
        padding: 14px;
        font-size: 16px; /* Prevents zoom on iOS */
    }
    
    .tab-icon {
        font-size: 28px;
    }
    
    .tab-label {
        font-size: 11px;
    }
}

/* Loading State */
.loading {
    position: fixed;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    color: white;
    font-size: 18px;
    font-weight: 600;
    z-index: 20;
}

/* Utility Classes */
.text-center { text-align: center; }
.mb-4 { margin-bottom: 1rem; }
.mt-4 { margin-top: 1rem; }

/* Custom Scrollbar */
.mr-main::-webkit-scrollbar {
    width: 4px;
}

.mr-main::-webkit-scrollbar-track {
    background: rgba(255, 255, 255, 0.1);
}

.mr-main::-webkit-scrollbar-thumb {
    background: rgba(255, 255, 255, 0.3);
    border-radius: 2px;
}

.mr-main::-webkit-scrollbar-thumb:hover {
    background: rgba(255, 255, 255, 0.5);
}'''
    
    write_file('static/css/mr-styles.css', mr_styles)
    
    # 5. Update Main HTML Template
    updated_index_html = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MISSIORA - Mixed Reality AI Companion</title>
    <link rel="stylesheet" href="/static/css/mr-styles.css">
    <style>
        /* Ensure full viewport coverage */
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        html, body {
            width: 100%;
            height: 100%;
            overflow: hidden;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        }
        
        /* Loading state */
        .loading {
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            color: white;
            font-size: 18px;
            font-weight: 600;
            z-index: 20;
            text-shadow: 0 2px 4px rgba(0, 0, 0, 0.5);
        }
    </style>
</head>
<body>
    <div id="app">
        <div class="loading">Loading Missiora...</div>
    </div>
    
    <script type="importmap">
    {
      "imports": {
        "vue": "https://unpkg.com/vue@3/dist/vue.esm-browser.js"
      }
    }
    </script>
    <script type="module">
        import { createApp } from 'vue'
        import { MainApp } from '/static/js/vue-components.js'
        
        createApp(MainApp).mount('#app')
    </script>
</body>
</html>'''
    
    write_file('templates/index.html', updated_index_html)
    
    # 6. Add Backend API Enhancements
    api_enhancements = '''
# Add these routes to routes.py for agent state management

@app.route('/api/agent-state', methods=['GET'])
@login_required
def get_agent_state():
    """Get current agent state and completion data"""
    user = current_user
    
    # Calculate completion percentages
    identity_completion = calculate_identity_completion(user)
    mission_completion = calculate_mission_completion(user)
    roadmap_completion = calculate_roadmap_completion(user)
    
    total_completion = (identity_completion * 0.33) + (mission_completion * 0.33) + (roadmap_completion * 0.34)
    
    # Determine agent stage
    stage = 'seed' if total_completion <= 25 else \
           'sprout' if total_completion <= 50 else \
           'bloom' if total_completion <= 80 else 'master'
    
    return jsonify({
        'completion': {
            'identity': identity_completion,
            'mission': mission_completion,
            'roadmap': roadmap_completion,
            'total': total_completion
        },
        'stage': stage,
        'message': get_agent_message(stage),
        'mood': get_agent_mood(total_completion)
    })

def calculate_identity_completion(user):
    """Calculate identity completion percentage"""
    if not user.identity_data:
        return 0
    
    identity = json.loads(user.identity_data)
    fields = ['name', 'archetype', 'mood', 'region', 'field', 'selfTitle']
    completed = sum(1 for field in fields if identity.get(field, '').strip())
    return (completed / len(fields)) * 100

def calculate_mission_completion(user):
    """Calculate mission completion percentage"""
    if not user.mission_statement:
        return 0
    
    # Check for mission components
    fields = ['mission_statement', 'current_goal']
    completed = sum(1 for field in fields if getattr(user, field, '').strip())
    return (completed / len(fields)) * 100

def calculate_roadmap_completion(user):
    """Calculate roadmap completion percentage"""
    milestones = Milestone.query.filter_by(active=True).all()
    if not milestones:
        return 0
    
    completed_milestones = sum(1 for m in milestones if m.completed)
    return (completed_milestones / len(milestones)) * 100

def get_agent_message(stage):
    """Get personality message based on stage"""
    messages = {
        'seed': [
            "I'm just beginning to understand you! 🌱",
            "Let's plant the seeds of your mission! 🌱",
            "Tell me more about who you are! 🌱"
        ],
        'sprout': [
            "I'm growing! Your mission is becoming clearer 🌿",
            "Keep feeding me insights! 🌿",
            "I can feel your purpose taking shape! 🌿"
        ],
        'bloom': [
            "Look how far we've come! 🌸",
            "Your mission is flourishing! 🌸",
            "We're making beautiful progress! 🌸"
        ],
        'master': [
            "We've achieved mastery together! 🌟",
            "Ready for the next challenge? 🌟",
            "Your entrepreneurial spirit shines bright! 🌟"
        ]
    }
    
    stage_messages = messages.get(stage, messages['seed'])
    import random
    return random.choice(stage_messages)

def get_agent_mood(completion):
    """Determine agent mood based on completion"""
    if completion < 25:
        return 'curious'
    elif completion < 50:
        return 'excited'
    elif completion < 80:
        return 'happy'
    else:
        return 'proud'
'''
    
    # 7. Patch existing routes.py file
    patch_file(
        'routes.py',
        r'(# === NEW API ROUTES FOR 3-VIEW UX ===)',
        r'\1\n' + api_enhancements,
        re.MULTILINE
    )
    
    # 8. Update existing models.py to include agent state fields
    models_patch = '''
# Add these fields to User model for agent state tracking
    agent_stage = db.Column(db.String(20), default='seed')
    completion_data = db.Column(db.Text, nullable=True)  # JSON stored completion data
    last_agent_interaction = db.Column(db.DateTime, default=datetime.utcnow)
'''
    
    patch_file(
        'models.py',
        r'(# Identity and Mission data.*\n.*identity_data.*\n.*mission_statement.*\n.*current_goal.*)',
        r'\1' + models_patch,
        re.MULTILINE | re.DOTALL
    )
    
    # 9. Create Package.json for Three.js dependencies
    package_json = '''{
  "name": "missiora-mr",
  "version": "1.0.0",
  "description": "Mixed Reality Tamagotchi Experience for Solopreneurs",
  "scripts": {
    "dev": "python main.py",
    "build": "echo 'No build process needed'"
  },
  "dependencies": {
    "three": "^0.157.0"
  },
  "devDependencies": {},
  "type": "module"
}'''
    
    write_file('package.json', package_json)
    
    # 10. Create README for MR transformation
    readme_md = '''# MISSIORA Mixed Reality Transformation

This transformation converts the existing MISSIORA Flask/Vue.js application into an immersive Mixed Reality experience with an evolving AI Tamagotchi companion.

## New Features Added

### 1. WebGL Tamagotchi Agent
- Real-time 3D agent rendering with Three.js
- Evolution stages: Seed → Sprout → Bloom → Master
- Mood animations and personality responses
- Completion-driven growth system

### 2. Camera Integration
- Rear camera feed as background
- Fallback gradient for devices without camera
- Brightness adjustment for UI readability
- Permission handling with graceful degradation

### 3. Glassmorphism UI
- Mobile-first 1080×1920px design
- Translucent panels with backdrop blur
- Spatial positioning and depth
- Smooth animations and transitions

### 4. Progressive Disclosure
- Identity completion unlocks Mission (80% threshold)
- Mission completion unlocks Roadmap (75% threshold)
- Visual completion indicators
- Agent-guided progression

### 5. Enhanced Backend
- Agent state tracking APIs
- Completion calculation algorithms
- Personality message system
- Real-time progress synchronization

## Technical Implementation

### Files Created/Modified:
- `static/js/tamagotchi-agent.js` - WebGL agent renderer
- `static/js/camera-integration.js` - Camera/AR handling
- `static/js/vue-components.js` - Enhanced MR components
- `static/css/mr-styles.css` - Glassmorphism styling
- `templates/index.html` - Updated main template
- `routes.py` - Added agent state APIs
- `models.py` - Added agent tracking fields

### Architecture:
```
Camera Feed (Background)
├── WebGL Canvas (Agent Layer)
├── Glassmorphism UI (Overlay)
├── Speech Bubbles (Agent Communication)
└── Progressive Navigation (Footer)
```

## Usage

1. Run the application: `python main.py`
2. Allow camera access for full MR experience
3. Complete Identity form to grow your agent
4. Progress through Mission and Roadmap stages
5. Watch your Tamagotchi companion evolve!

The agent serves as both motivation and visual representation of entrepreneurial progress, creating an emotionally engaging experience that encourages completion and growth.
'''
    
    write_file('README_MR.md', readme_md)
    
    print("\n🎉 MISSIORA Mixed Reality Transformation Complete!")
    print("\n✨ Summary of Changes:")
    print("- WebGL Tamagotchi Agent with 4 evolution stages")
    print("- Camera integration with AR overlay")
    print("- Glassmorphism UI with spatial positioning")
    print("- Progressive disclosure system")
    print("- Agent personality and mood system")
    print("- Enhanced completion tracking")
    print("- Mobile-optimized MR interface")
    print("\n🚀 Your AI companion awaits! Run the app to begin the journey.")

if __name__ == '__main__':
    main()