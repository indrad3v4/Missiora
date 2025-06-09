/**
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
}