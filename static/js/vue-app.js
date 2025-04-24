// Vue.js application entry point

import { createApp } from 'vue';
import ChatComponent from './components/ChatComponent.js';

document.addEventListener('DOMContentLoaded', function() {
  // Initialize the chat component when an element with id "chat-app" exists
  const chatContainer = document.getElementById('chat-app');
  if (chatContainer) {
    const app = createApp({
      components: {
        'chat-component': ChatComponent
      },
      template: '<chat-component/>'
    });
    
    app.mount('#chat-app');
  }
  
  // Handle MetaMask connection button clicks
  const connectButton = document.getElementById('connectMetaMaskBtn');
  if (connectButton) {
    connectButton.addEventListener('click', async () => {
      try {
        // Check if MetaMask is installed
        if (typeof window.ethereum === 'undefined') {
          alert('MetaMask is not installed. Please install MetaMask to continue.');
          return;
        }
        
        // Show connecting status
        connectButton.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Connecting...';
        connectButton.disabled = true;
        
        // Request account access
        const accounts = await ethereum.request({ method: 'eth_requestAccounts' });
        const account = accounts[0];
        
        if (!account) {
          connectButton.innerHTML = '<i class="fas fa-wallet me-2"></i>Connect with MetaMask';
          connectButton.disabled = false;
          alert('No account found. Please unlock your MetaMask wallet.');
          return;
        }
        
        // Update button appearance
        connectButton.innerHTML = `<i class="fas fa-check-circle me-2"></i>Connected: ${account.substring(0, 6)}...${account.substring(38)}`;
        connectButton.classList.remove('btn-primary');
        connectButton.classList.add('btn-success');
        connectButton.disabled = false;
        
        // Dispatch event for component to listen for
        window.dispatchEvent(new CustomEvent('metamaskConnected', { 
          detail: { address: account } 
        }));
        
      } catch (error) {
        console.error('MetaMask Error:', error);
        connectButton.innerHTML = '<i class="fas fa-wallet me-2"></i>Connect with MetaMask';
        connectButton.disabled = false;
        alert(`MetaMask Error: ${error.message}`);
      }
    });
  }
});