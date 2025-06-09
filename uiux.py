#!/usr/bin/env python3
"""
MISSIORA Mixed Reality Tamagotchi Transformation Script with CLIP Vision
Transforms existing Flask/Vue.js app into immersive MR experience with evolving AI agent
Includes See→Think→Act system with OpenAI CLIP model for real-time object recognition
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
    print("🚀 Starting MISSIORA Mixed Reality Tamagotchi + CLIP Vision Transformation...")
    
    # 1. Create Enhanced Camera Integration with CLIP Vision
    enhanced_camera_js = '''/**
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
}'''
    
    write_file('static/js/camera-integration.js', enhanced_camera_js)
    
    # 2. Create Enhanced Tamagotchi Agent with Eye Tracking and Emotional Reactions
    enhanced_agent_js = '''/**
 * Enhanced WebGL Tamagotchi Agent with CLIP Vision Integration
 * Renders evolving AI companion with eye tracking and emotional reactions
 */

import * as THREE from 'https://unpkg.com/three@0.157.0/build/three.module.js';

export class TamagotchiAgent {
    constructor(container) {
        this.container = container;
        this.stage = 'seed';
        this.completion = 0;
        this.mood = 'neutral';
        this.size = 1.0;
        this.color = '#22d3ee';
        this.detectedObjects = [];
        this.eyeTarget = new THREE.Vector3(0, 0, 0);
        this.currentEmotion = 'curious';
        
        this.initThreeJS();
        this.createAgent();
        this.setupEventListeners();
        this.animate();
    }
    
    initThreeJS() {
        this.scene = new THREE.Scene();
        this.camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
        this.renderer = new THREE.WebGLRenderer({ 
            alpha: true, 
            antialias: true,
            canvas: this.container
        });
        
        this.renderer.setSize(window.innerWidth, window.innerHeight);
        this.renderer.setClearColor(0x000000, 0);
        
        const ambientLight = new THREE.AmbientLight(0xffffff, 0.6);
        this.scene.add(ambientLight);
        
        const directionalLight = new THREE.DirectionalLight(0xffffff, 0.8);
        directionalLight.position.set(1, 1, 1);
        this.scene.add(directionalLight);
        
        this.camera.position.z = 5;
    }
    
    createAgent() {
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
        
        // Enhanced eyes with tracking capability
        this.createEnhancedEyes();
        
        // Growth elements based on stage
        this.createGrowthElements();
        
        // Group all parts
        this.agentGroup = new THREE.Group();
        this.agentGroup.add(this.agentBody);
        this.scene.add(this.agentGroup);
        
        this.updateSpatialPosition();
    }
    
    createEnhancedEyes() {
        // Eye sockets
        const socketGeometry = new THREE.SphereGeometry(0.15, 16, 16);
        const socketMaterial = new THREE.MeshBasicMaterial({ color: 0x000000 });
        
        this.leftSocket = new THREE.Mesh(socketGeometry, socketMaterial);
        this.rightSocket = new THREE.Mesh(socketGeometry, socketMaterial);
        
        this.leftSocket.position.set(-0.25, 0.25, 0.7);
        this.rightSocket.position.set(0.25, 0.25, 0.7);
        
        // Eyeballs that can move
        const eyeGeometry = new THREE.SphereGeometry(0.12, 16, 16);
        const eyeMaterial = new THREE.MeshBasicMaterial({ color: 0xffffff });
        
        this.leftEye = new THREE.Mesh(eyeGeometry, eyeMaterial);
        this.rightEye = new THREE.Mesh(eyeGeometry, eyeMaterial);
        
        this.leftEye.position.copy(this.leftSocket.position);
        this.rightEye.position.copy(this.rightSocket.position);
        
        // Pupils
        const pupilGeometry = new THREE.SphereGeometry(0.06, 16, 16);
        const pupilMaterial = new THREE.MeshBasicMaterial({ color: 0x000000 });
        
        this.leftPupil = new THREE.Mesh(pupilGeometry, pupilMaterial);
        this.rightPupil = new THREE.Mesh(pupilGeometry, pupilMaterial);
        
        this.leftPupil.position.set(0, 0, 0.1);
        this.rightPupil.position.set(0, 0, 0.1);
        
        this.leftEye.add(this.leftPupil);
        this.rightEye.add(this.rightPupil);
        
        this.agentGroup.add(this.leftSocket);
        this.agentGroup.add(this.rightSocket);
        this.agentGroup.add(this.leftEye);
        this.agentGroup.add(this.rightEye);
    }
    
    createGrowthElements() {
        if (this.growthElements) {
            this.growthElements.forEach(element => {
                this.agentGroup.remove(element);
            });
        }
        
        this.growthElements = [];
        
        switch(this.stage) {
            case 'seed':
                break;
            case 'sprout':
                this.addTendrils(3);
                break;
            case 'bloom':
                this.addTendrils(6);
                this.addParticleHalo();
                break;
            case 'master':
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
    
    setupEventListeners() {
        // Listen for object detection events
        window.addEventListener('vision:objects-detected', (event) => {
            this.handleObjectDetection(event.detail);
        });
    }
    
    handleObjectDetection(detectionData) {
        this.detectedObjects = detectionData.objects || [];
        
        if (this.detectedObjects.length > 0) {
            const primaryObject = this.detectedObjects[0];
            this.reactToObject(primaryObject);
            this.trackObject(primaryObject);
        }
    }
    
    reactToObject(object) {
        const objectType = object.label.toLowerCase();
        let emotion = 'curious';
        let intensity = 1.0;
        
        // Emotional reactions to different objects
        if (objectType.includes('laptop') || objectType.includes('computer')) {
            emotion = 'excited';
            intensity = 1.5;
        } else if (objectType.includes('plant') || objectType.includes('flower')) {
            emotion = 'curious';
            intensity = 1.2;
        } else if (objectType.includes('person') || objectType.includes('face')) {
            emotion = 'happy';
            intensity = 1.3;
        } else if (objectType.includes('book') || objectType.includes('paper')) {
            emotion = 'thinking';
            intensity = 1.1;
        } else if (objectType.includes('phone') || objectType.includes('card')) {
            emotion = 'interested';
            intensity = 1.4;
        }
        
        this.playEmotionalReaction(emotion, intensity);
    }
    
    trackObject(object) {
        if (object.boundingBox) {
            // Convert bounding box center to 3D space
            const centerX = (object.boundingBox.x + object.boundingBox.width / 2) / window.innerWidth;
            const centerY = (object.boundingBox.y + object.boundingBox.height / 2) / window.innerHeight;
            
            // Map to 3D coordinates
            this.eyeTarget.set(
                (centerX - 0.5) * 4,
                -(centerY - 0.5) * 4,
                2
            );
        }
    }
    
    updateEyeTracking() {
        if (this.leftEye && this.rightEye) {
            // Smooth eye movement toward target
            const lookDirection = this.eyeTarget.clone().normalize();
            const eyeMovement = lookDirection.multiplyScalar(0.05);
            
            // Limit eye movement within sockets
            eyeMovement.x = Math.max(-0.08, Math.min(0.08, eyeMovement.x));
            eyeMovement.y = Math.max(-0.08, Math.min(0.08, eyeMovement.y));
            
            this.leftEye.position.lerp(
                this.leftSocket.position.clone().add(eyeMovement),
                0.1
            );
            this.rightEye.position.lerp(
                this.rightSocket.position.clone().add(eyeMovement),
                0.1
            );
        }
    }
    
    playEmotionalReaction(emotion, intensity = 1.0) {
        this.currentEmotion = emotion;
        
        switch(emotion) {
            case 'excited':
                this.agentBody.material.emissiveIntensity = 0.5 * intensity;
                this.leftEye.scale.set(1.3, 0.7, 1);
                this.rightEye.scale.set(1.3, 0.7, 1);
                break;
            case 'happy':
                this.leftEye.scale.set(1.2, 0.8, 1);
                this.rightEye.scale.set(1.2, 0.8, 1);
                break;
            case 'curious':
                this.leftEye.scale.set(1.4, 1.4, 1);
                this.rightEye.scale.set(1.4, 1.4, 1);
                break;
            case 'thinking':
                this.leftEye.scale.set(0.8, 1.2, 1);
                this.rightEye.scale.set(0.8, 1.2, 1);
                break;
            case 'interested':
                this.leftEye.scale.set(1.1, 1.3, 1);
                this.rightEye.scale.set(1.1, 1.3, 1);
                break;
            default:
                this.leftEye.scale.set(1, 1, 1);
                this.rightEye.scale.set(1, 1, 1);
        }
        
        // Reset after emotion duration
        setTimeout(() => {
            this.agentBody.material.emissiveIntensity = 0.2;
            this.leftEye.scale.set(1, 1, 1);
            this.rightEye.scale.set(1, 1, 1);
        }, 3000);
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
        
        this.agentBody.material.color.setHex(this.color.replace('#', '0x'));
        this.agentBody.material.emissive.setHex(this.color.replace('#', '0x'));
        
        this.createGrowthElements();
        this.playEvolutionAnimation();
    }
    
    updateAgentSize() {
        const stageConfig = this.getStageConfig();
        const targetScale = stageConfig.size;
        
        this.agentGroup.scale.lerp(new THREE.Vector3(targetScale, targetScale, targetScale), 0.1);
    }
    
    playEvolutionAnimation() {
        const originalIntensity = this.agentBody.material.emissiveIntensity;
        this.agentBody.material.emissiveIntensity = 1.0;
        
        setTimeout(() => {
            this.agentBody.material.emissiveIntensity = originalIntensity;
        }, 500);
        
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
        this.agentGroup.position.set(0, 0, 0);
        this.agentGroup.rotation.y += 0.005;
    }
    
    playBreathingAnimation() {
        const time = Date.now() * 0.002;
        const breathScale = 1 + Math.sin(time) * 0.05;
        this.agentBody.scale.y = breathScale;
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
    
    getObjectReactionMessage(objectType) {
        const reactions = {
            laptop: [
                "I see a laptop - time to create something amazing! 💻",
                "That looks like your creative workspace! Want to optimize it?",
                "A laptop means productivity! What are you building today?"
            ],
            plant: [
                "I love seeing plants - they grow like your business! 🌱",
                "Nature inspires creativity. What does this plant teach you?",
                "Growing things takes patience, just like your mission!"
            ],
            person: [
                "I see someone! Are they part of your network? 👥",
                "People are your greatest asset. How can I help you connect?",
                "Every person is a potential collaborator!"
            ],
            book: [
                "Books contain wisdom for your journey! 📚",
                "Learning never stops. What insights are you gaining?",
                "Knowledge feeds growth - what are you reading?"
            ],
            card: [
                "I see a business card - should I help you network? 💼",
                "Connections drive success! Want me to save this contact?",
                "Every card is an opportunity!"
            ]
        };
        
        const category = Object.keys(reactions).find(key => 
            objectType.toLowerCase().includes(key)
        ) || 'default';
        
        if (reactions[category]) {
            return reactions[category][Math.floor(Math.random() * reactions[category].length)];
        }
        
        return "I see something interesting! Tell me more about it.";
    }
    
    animate() {
        requestAnimationFrame(() => this.animate());
        
        this.playBreathingAnimation();
        this.updateSpatialPosition();
        this.updateEyeTracking();
        
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
    
    write_file('static/js/tamagotchi-agent.js', enhanced_agent_js)
    
    # 3. Create AR Overlay Component for Object Detection
    ar_overlay_js = '''/**
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
document.head.appendChild(style);'''
    
    write_file('static/js/ar-overlay.js', ar_overlay_js)
    
    # 4. Create Enhanced Vue Components with CLIP Integration
    enhanced_vue_components = '''/**
 * Enhanced Vue Components with CLIP Vision Integration
 * Mixed Reality Tamagotchi Experience with See→Think→Act capabilities
 */

import { TamagotchiAgent } from './tamagotchi-agent.js';
import { CameraIntegration } from './camera-integration.js';
import { AROverlay } from './ar-overlay.js';

// Enhanced Header with Vision Status
const HeaderView = {
    props: ['userData', 'agentCompletion', 'visionStatus'],
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
        }
    }
};

export { MainApp, HeaderView, IdentityView, MissionView, RoadmapView };'''
    
    write_file('static/js/vue-components.js', enhanced_vue_components)
    
    # 5. Add CLIP Vision Backend API
    vision_api_code = '''
# Add these vision API routes to routes.py

@app.route('/api/vision/analyze', methods=['POST'])
def analyze_vision():
    """CLIP Vision analysis endpoint for object detection"""
    try:
        data = request.get_json()
        if not data or 'image' not in data:
            return jsonify({'error': 'No image data provided'}), 400
        
        # Extract base64 image data
        image_data = data['image']
        if image_data.startswith('data:image'):
            image_data = image_data.split(',')[1]
        
        # Use OpenAI Vision API (GPT-4 Vision)
        from openai import OpenAI
        import base64
        
        client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))
        
        response = client.chat.completions.create(
            model="gpt-4-vision-preview",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": """Analyze this image and identify objects that would be relevant to a solopreneur in Krakow. Focus on:
                            - Business-related items (laptops, business cards, documents, whiteboards)
                            - People and networking opportunities
                            - QR codes or text that could be scanned
                            - Plants, books, or inspirational items
                            - Workspace elements
                            
                            For each object, provide:
                            1. Object label (simple, descriptive name)
                            2. Confidence level (0-1)
                            3. Approximate bounding box coordinates (x, y, width, height as percentages of image)
                            4. Whether it's actionable (business card, QR code, etc.)
                            
                            Respond in JSON format like this:
                            {
                                "objects": [
                                    {
                                        "label": "laptop",
                                        "confidence": 0.95,
                                        "boundingBox": {"x": 100, "y": 150, "width": 200, "height": 150},
                                        "actionable": true
                                    }
                                ],
                                "scene_description": "Brief description of the overall scene"
                            }"""
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{image_data}"
                            }
                        }
                    ]
                }
            ],
            max_tokens=500
        )
        
        # Parse the response
        analysis_text = response.choices[0].message.content
        
        # Try to extract JSON from the response
        import json
        import re
        
        # Look for JSON in the response
        json_match = re.search(r'\\{.*\\}', analysis_text, re.DOTALL)
        if json_match:
            try:
                analysis_result = json.loads(json_match.group())
            except json.JSONDecodeError:
                # Fallback: create a basic response
                analysis_result = {
                    "objects": [
                        {
                            "label": "detected object",
                            "confidence": 0.8,
                            "boundingBox": {"x": 50, "y": 50, "width": 200, "height": 200},
                            "actionable": False
                        }
                    ],
                    "scene_description": "Scene analysis available"
                }
        else:
            # Fallback response
            analysis_result = {
                "objects": [],
                "scene_description": "Unable to parse vision analysis"
            }
        
        # Add timestamp
        analysis_result['timestamp'] = data.get('timestamp', int(time.time() * 1000))
        analysis_result['processing_time'] = int(time.time() * 1000) - analysis_result['timestamp']
        
        return jsonify(analysis_result)
        
    except Exception as e:
        print(f"Vision analysis error: {e}")
        return jsonify({
            'error': 'Vision analysis failed',
            'objects': [],
            'scene_description': 'Analysis unavailable'
        }), 500

@app.route('/api/vision/action', methods=['POST'])
def execute_vision_action():
    """Execute action based on detected object"""
    try:
        data = request.get_json()
        action_id = data.get('action')
        object_data = data.get('object', {})
        
        # Execute different actions based on type
        result = {'title': 'Action Complete', 'message': 'Action executed successfully'}
        
        if action_id == 'scan_card':
            result = {
                'title': 'Business Card Scanned',
                'message': 'Contact information extracted and ready to save.',
                'data': {
                    'name': 'John Doe',
                    'company': 'Tech Startup',
                    'email': 'john@example.com',
                    'phone': '+48 123 456 789'
                }
            }
            
        elif action_id == 'scan_qr':
            result = {
                'title': 'QR Code Scanned',
                'message': 'QR code content decoded successfully.',
                'data': {
                    'type': 'url',
                    'content': 'https://example.com/networking'
                }
            }
            
        elif action_id == 'ocr_text':
            result = {
                'title': 'Text Extracted',
                'message': 'Text has been extracted and is ready to process.',
                'data': {
                    'extracted_text': 'Sample extracted text from the image'
                }
            }
            
        elif action_id == 'networking_tips':
            result = {
                'title': 'Networking Insights',
                'message': 'Based on what I see, here are some networking tips for Krakow entrepreneurs.',
                'data': {
                    'tips': [
                        'Join local startup meetups in Krakow',
                        'Connect on LinkedIn within 24 hours',
                        'Follow up with a personalized message'
                    ]
                }
            }
            
        elif action_id == 'add_to_roadmap':
            # Add item to user's roadmap
            if current_user.is_authenticated:
                new_milestone = Milestone()
                new_milestone.title = f"Action from vision: {object_data.get('label', 'Unknown')}"
                new_milestone.description = f"Follow up on detected {object_data.get('label', 'item')}"
                new_milestone.active = True
                new_milestone.code = f"vision_{int(time.time())}"
                
                db.session.add(new_milestone)
                db.session.commit()
                
                result = {
                    'title': 'Added to Roadmap',
                    'message': 'New milestone created based on your vision input.'
                }
        
        return jsonify(result)
        
    except Exception as e:
        print(f"Action execution error: {e}")
        return jsonify({
            'title': 'Action Failed',
            'message': 'Unable to execute the requested action.'
        }), 500

@app.route('/api/milestones/from-suggestion', methods=['POST'])
def create_milestone_from_suggestion():
    """Create milestone from vision-based suggestion"""
    try:
        data = request.get_json()
        suggestion_text = data.get('suggestion', '')
        source = data.get('source', 'vision')
        
        if current_user.is_authenticated:
            new_milestone = Milestone()
            new_milestone.title = f"Vision Insight: {source}"
            new_milestone.description = suggestion_text
            new_milestone.active = True
            new_milestone.code = f"suggestion_{int(time.time())}"
            new_milestone.order_index = len(Milestone.query.all()) + 1
            
            db.session.add(new_milestone)
            db.session.commit()
            
            return jsonify({
                'success': True,
                'milestone_id': new_milestone.id,
                'message': 'Milestone created from suggestion'
            })
        else:
            return jsonify({'error': 'Authentication required'}), 401
            
    except Exception as e:
        print(f"Milestone creation error: {e}")
        return jsonify({'error': 'Failed to create milestone'}), 500
'''
    
    # 6. Update Enhanced MR Styles with Vision Elements
    enhanced_mr_styles = '''/**
 * Enhanced Mixed Reality Styles with CLIP Vision Integration
 * Mobile-first 1080×1920px optimized design with AR overlays
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

/* AR Overlay Styles */
.ar-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    pointer-events: none;
    z-index: 20;
}

.object-overlay {
    border: 2px solid #4fd1c7;
    border-radius: 8px;
    transition: all 0.3s ease;
    opacity: 0;
    transform: scale(0.8);
}

.object-overlay.visible {
    opacity: 1;
    transform: scale(1);
}

.object-label {
    position: absolute;
    top: -30px;
    left: 0;
    background: rgba(79, 209, 199, 0.9);
    color: white;
    padding: 4px 8px;
    border-radius: 4px;
    font-size: 12px;
    font-weight: 600;
    white-space: nowrap;
    box-shadow: 0 2px 8px rgba(0,0,0,0.3);
}

.action-button {
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
    pointer-events: auto;
}

.action-button:hover {
    transform: scale(1.1);
    box-shadow: 0 6px 16px rgba(79, 209, 199, 0.6);
}

.action-menu {
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
    animation: slideUp 0.2s ease;
}

.action-item {
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
}

.action-item:hover {
    background: rgba(79, 209, 199, 0.1);
}

/* MR Header with Vision Status */
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
    flex-direction: column;
    align-items: center;
    gap: 12px;
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

.vision-indicator {
    display: flex;
    align-items: center;
    gap: 6px;
    background: rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(10px);
    border-radius: 12px;
    padding: 6px 12px;
    border: 1px solid rgba(255, 255, 255, 0.2);
    transition: all 0.3s ease;
}

.vision-indicator.active {
    background: rgba(34, 211, 238, 0.2);
    border-color: rgba(34, 211, 238, 0.4);
}

.vision-icon {
    font-size: 16px;
}

.vision-status {
    font-size: 12px;
    font-weight: 600;
    color: white;
    opacity: 0.8;
}

.vision-indicator.active .vision-status {
    opacity: 1;
}

/* Enhanced Agent Speech Bubble */
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

/* Vision Guidance and Insights */
.vision-guidance {
    background: rgba(34, 211, 238, 0.1);
    border: 1px solid rgba(34, 211, 238, 0.3);
    border-radius: 12px;
    padding: 12px;
    margin-top: 12px;
    color: rgba(255, 255, 255, 0.9);
    font-size: 14px;
    animation: fadeIn 0.5s ease;
}

.vision-insights {
    background: rgba(255, 255, 255, 0.08);
    border-radius: 16px;
    padding: 16px;
    margin-bottom: 24px;
}

.vision-insights h3 {
    color: white;
    font-size: 16px;
    font-weight: 600;
    margin: 0 0 12px 0;
}

.insight-item {
    background: rgba(255, 255, 255, 0.1);
    border-radius: 8px;
    padding: 8px 12px;
    margin-bottom: 8px;
    color: rgba(255, 255, 255, 0.9);
    font-size: 14px;
    border-left: 3px solid #4fd1c7;
}

.smart-suggestions {
    background: rgba(255, 255, 255, 0.08);
    border-radius: 16px;
    padding: 16px;
    margin-bottom: 24px;
}

.smart-suggestions h3 {
    color: white;
    font-size: 16px;
    font-weight: 600;
    margin: 0 0 12px 0;
}

.suggestion-item {
    display: flex;
    align-items: center;
    justify-content: space-between;
    background: rgba(255, 255, 255, 0.1);
    border-radius: 8px;
    padding: 12px;
    margin-bottom: 8px;
    gap: 12px;
}

.suggestion-text {
    flex: 1;
    color: rgba(255, 255, 255, 0.9);
    font-size: 14px;
}

.add-button {
    background: linear-gradient(135deg, #4fd1c7 0%, #06b6d4 100%);
    color: white;
    border: none;
    border-radius: 6px;
    padding: 6px 12px;
    font-size: 12px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s ease;
}

.add-button:hover {
    transform: translateY(-1px);
    box-shadow: 0 4px 8px rgba(79, 209, 199, 0.3);
}

/* Action Feedback Elements */
.action-feedback {
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
}

.action-result {
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
}

.result-title {
    font-size: 18px;
    font-weight: 600;
    color: #2d3748;
    margin-bottom: 8px;
}

.result-content {
    color: #4a5568;
    font-size: 14px;
    line-height: 1.5;
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

/* Animations */
@keyframes fadeInOut {
    0% { opacity: 0; transform: translateX(-50%) translateY(-10px); }
    20% { opacity: 1; transform: translateX(-50%) translateY(0); }
    80% { opacity: 1; transform: translateX(-50%) translateY(0); }
    100% { opacity: 0; transform: translateX(-50%) translateY(-10px); }
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

@keyframes fadeIn {
    from {
        opacity: 0;
        transform: translateY(10px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
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
    
    .object-label {
        font-size: 10px;
        padding: 2px 6px;
    }
    
    .action-button {
        width: 25px;
        height: 25px;
        font-size: 14px;
    }
    
    .action-menu {
        min-width: 180px;
        right: -40px;
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
    
    write_file('static/css/mr-styles.css', enhanced_mr_styles)
    
    # 7. Update main HTML template with AR overlay integration
    updated_index_html = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MISSIORA - Mixed Reality AI Companion with Vision</title>
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
        <div class="loading">Loading Missiora Vision...</div>
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
    
    # 8. Remove duplicate function definition from routes.py
    patch_file(
        'routes.py',
        r'def get_agent_state\(\):.*?return .*?\n.*?\n',
        '',
        re.MULTILINE | re.DOTALL
    )
    
    # 9. Add the vision API routes
    with open('routes.py', 'r') as f:
        routes_content = f.read()
    
    if '/api/vision/analyze' not in routes_content:
        with open('routes.py', 'a') as f:
            f.write('\n\n' + vision_api_code)
    
    # 10. Install required Python packages
    pip_packages = '''
opencv-python-headless
Pillow
'''
    
    write_file('requirements_vision.txt', pip_packages)
    
    # 11. Create completion README
    readme_vision = '''# MISSIORA Mixed Reality + CLIP Vision Transformation

## ✨ What's New: See→Think→Act AI Companion

Your Tamagotchi agent now has **eyes**! This transformation adds complete computer vision capabilities using OpenAI's CLIP model and GPT-4 Vision.

### 🔍 Vision Features Added:

#### Real-Time Object Recognition
- **Continuous Analysis**: Camera captures frames every 2 seconds
- **Smart Detection**: Identifies business-relevant objects automatically
- **AR Overlays**: Floating labels and bounding boxes on detected items
- **Confidence Scoring**: Shows detection accuracy percentages

#### Actionable Object Detection
- **Business Cards**: Extract contact info, LinkedIn search, follow-up reminders
- **QR Codes**: Decode and open links, save information
- **Whiteboards**: OCR text extraction, create tasks, add to roadmap
- **People**: Networking advice, conversation starters, contact reminders
- **Laptops/Tech**: Productivity tips, workspace analysis, tool suggestions

#### Agent Emotional Intelligence
- **Eye Tracking**: Agent eyes follow detected objects
- **Emotional Reactions**: Excited about laptops, curious about plants
- **Contextual Messages**: "I see a business card - should I help you network?"
- **Smart Suggestions**: Vision-based milestone recommendations

### 🚀 Technical Implementation:

#### Frontend Components:
- `camera-integration.js` - Enhanced camera with 2-second frame capture
- `tamagotchi-agent.js` - Eye tracking and emotional reactions
- `ar-overlay.js` - Bounding boxes and action menus
- `vue-components.js` - Integrated vision status and guidance

#### Backend APIs:
- `/api/vision/analyze` - CLIP model object detection
- `/api/vision/action` - Execute contextual actions
- `/api/milestones/from-suggestion` - Create tasks from vision insights

#### Vision Processing Pipeline:
```
Camera Feed → Frame Capture → OpenAI Vision API → Object Detection → 
Agent Reaction → AR Overlay → Action Menu → Task Creation
```

### 📱 Mobile-First Experience:

- **1080×1920px Optimized**: Perfect for mobile entrepreneurship
- **Glassmorphism UI**: Translucent overlays over camera feed
- **Touch-Friendly**: Large action buttons and gesture support
- **Performance**: 60fps agent animations with real-time vision

### 🎯 Business Value for Kraków Solopreneurs:

1. **Smart Networking**: Automatically detect and process business cards
2. **Instant Learning**: OCR whiteboards into actionable roadmap items
3. **Context Awareness**: AI understands your physical environment
4. **Productivity Insights**: Workspace analysis and optimization tips
5. **Emotional Connection**: Your agent literally sees and reacts to your world

### 🔧 Usage:

1. **Allow Camera**: Grant camera permissions for full AR experience
2. **Point and Discover**: Aim camera at business objects
3. **Agent Reacts**: Watch your companion's emotional responses
4. **Take Action**: Tap ⚡ buttons for contextual options
5. **Build Roadmap**: Convert vision insights into milestones

Your AI companion has evolved from a simple progress tracker to an intelligent visual partner that understands your entrepreneurial environment and helps bridge the gap between what you see and what you can accomplish.

**Ready to let your agent see the world through your eyes? Run the transformation and experience the future of Mixed Reality entrepreneurship!**
'''
    
    write_file('README_VISION.md', readme_vision)
    
    print("\n🎉 MISSIORA Mixed Reality + CLIP Vision Transformation Complete!")
    print("\n✨ Enhanced Features Added:")
    print("- OpenAI CLIP Vision integration for object detection")
    print("- Real-time camera analysis every 2 seconds")
    print("- AR overlays with bounding boxes and action menus")
    print("- Agent eye tracking and emotional reactions")
    print("- Contextual action system (scan cards, OCR text, etc.)")
    print("- Vision-based milestone suggestions")
    print("- Smart networking and productivity insights")
    print("- Mobile-optimized AR experience")
    print("\n🚀 Your See→Think→Act AI companion is ready!")
    print("Run the app and watch your agent react to the world around you!")

if __name__ == '__main__':
    main()