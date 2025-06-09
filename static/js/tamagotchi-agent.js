/**
 * WebGL Tamagotchi Agent Renderer
 * Renders evolving AI companion with Three.js
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
}