// ChatComponent.js - Vue 3 Component for Narrative Chat Experience

export default {
  name: 'ChatComponent',
  template: /* html */`
    <div class="chat-container">
      <!-- Chat messages -->
      <div class="messages-container" ref="messagesContainer">
        <div v-for="msg in messages" 
             :key="msg.id" 
             class="message" 
             :class="msg.role"
             :data-agent="msg.agent">
          <div class="message-header" v-if="msg.agent && msg.agent !== 'user'">
            <span class="agent-badge">{{ formatAgentName(msg.agent) }}</span>
          </div>
          <div class="message-text" v-html="formatMessage(msg.text)"></div>
        </div>
        <div v-if="isTyping" class="message agent typing-indicator">
          <div class="dots"><span>.</span><span>.</span><span>.</span></div>
        </div>
      </div>
      
      <!-- Input area for user's reply -->
      <div class="input-area">
        <form @submit.prevent="sendMessage">
          <div class="input-group">
            <input 
              type="text" 
              v-model="userInput" 
              :disabled="isTyping || requireMetaMask"
              class="form-control" 
              placeholder="Type your response..." 
              ref="inputField"
            />
            <button 
              type="submit" 
              class="btn btn-primary" 
              :disabled="isTyping || !userInput || requireMetaMask"
            >
              <i class="fas fa-paper-plane"></i>
            </button>
          </div>
        </form>
        
        <!-- Free message counter -->
        <div v-if="freeMessagesRemaining !== null && freeMessagesRemaining <= 2" class="message-limit-warning">
          <span v-if="freeMessagesRemaining === 0">
            You've reached the free message limit.
            <button @click="connectMetaMask" class="btn btn-sm btn-outline-primary">Connect with MetaMask</button>
            to continue.
          </span>
          <span v-else>
            You have {{ freeMessagesRemaining }} free {{ freeMessagesRemaining === 1 ? 'message' : 'messages' }} remaining.
            <button @click="connectMetaMask" class="btn btn-sm btn-outline-primary">Connect with MetaMask</button>
            for unlimited access.
          </span>
        </div>
        
        <!-- MetaMask connection required message -->
        <div v-if="requireMetaMask" class="metamask-required-message">
          <p>Free message limit reached. Please connect with MetaMask to continue.</p>
          <button @click="connectMetaMask" class="btn btn-primary">Connect with MetaMask</button>
        </div>
      </div>
    </div>
  `,
  
  data() {
    return {
      messages: [],
      userInput: '',
      isTyping: false,
      freeMessagesRemaining: null,
      requireMetaMask: false,
      isAuthenticated: false,
      userAddress: null
    }
  },
  
  mounted() {
    this.startConversation();
    // Check if MetaMask is already connected
    this.checkMetaMaskConnection();
    
    // Listen for MetaMask connection events
    window.addEventListener('metamaskConnected', (event) => {
      this.isAuthenticated = true;
      this.userAddress = event.detail.address;
      // Add authentication success message
      this.addMessage({
        id: Date.now(),
        role: 'agent',
        agent: 'OrchestratorAgent',
        text: "Great! You're now connected with MetaMask. You have unlimited access to the AI agency. How else can I help you today?"
      });
    });
  },
  
  methods: {
    async startConversation() {
      this.isTyping = true;
      try {
        console.log("Starting conversation...");
        const response = await fetch('/api/chat', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ 
            start: true,
            address: this.userAddress 
          })
        });
        
        if (response.ok) {
          const data = await response.json();
          console.log("Greeting received:", data);
          this.addMessage({
            id: Date.now(),
            role: 'agent',
            agent: data.agent || 'OrchestratorAgent',
            text: data.reply
          });
        } else {
          const errorData = await response.json();
          console.error("Failed to start conversation:", errorData);
          throw new Error(errorData.error || 'Failed to start conversation');
        }
      } catch (error) {
        console.error('Error starting conversation:', error);
        this.addMessage({
          id: Date.now(),
          role: 'agent',
          text: "I apologize, but I'm having trouble connecting. Please try again in a moment." + 
                (error.message ? " Error: " + error.message : "")
        });
      } finally {
        this.isTyping = false;
      }
    },
    
    async sendMessage() {
      if (!this.userInput.trim() || this.requireMetaMask) return;
            
      const userMessage = this.userInput.trim();
      this.userInput = '';
      
      // Add user message to chat
      this.addMessage({
        id: Date.now(),
        role: 'user',
        text: userMessage
      });
      
      this.isTyping = true;
      
      try {
        console.log("Sending message:", userMessage);
        const response = await fetch('/api/chat', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            user_message: userMessage,
            address: this.userAddress
          })
        });
        
        if (response.ok) {
          const data = await response.json();
          console.log("Received response:", data);
          
          // Update free messages remaining (for non-authenticated users)
          if (data.free_messages_remaining !== undefined && data.free_messages_remaining !== null) {
            this.freeMessagesRemaining = data.free_messages_remaining;
          }
          
          this.addMessage({
            id: Date.now(),
            role: 'agent',
            agent: data.agent || 'OrchestratorAgent',
            text: data.reply
          });
        } else if (response.status === 403 && response.statusText.includes("MetaMask")) {
          // Handle case where server requires MetaMask auth
          const errorData = await response.json();
          console.log("Authentication required:", errorData);
          this.requireMetaMask = true;
          
          this.addMessage({
            id: Date.now(),
            role: 'agent',
            agent: 'OrchestratorAgent',
            text: "You've reached your free message limit. Please connect with MetaMask to continue using the AI agency."
          });
        } else {
          const errorData = await response.json();
          console.error("API error:", errorData);
          throw new Error(errorData.error || 'Failed to get response');
        }
      } catch (error) {
        console.error('Error sending message:', error);
        this.addMessage({
          id: Date.now(),
          role: 'agent',
          text: "I apologize, but I encountered an error. Please try again."
        });
      } finally {
        this.isTyping = false;
        // Focus the input field for next message
        this.$nextTick(() => {
          this.$refs.inputField.focus();
        });
      }
    },
    
    connectMetaMask() {
      // If MetaMask is available, request account access
      if (window.ethereum) {
        window.ethereum
          .request({ method: 'eth_requestAccounts' })
          .then(accounts => {
            if (accounts.length > 0) {
              this.userAddress = accounts[0];
              this.isAuthenticated = true;
              this.requireMetaMask = false;
              
              // Dispatch an event for other components
              window.dispatchEvent(
                new CustomEvent('metamaskConnected', { 
                  detail: { 
                    address: accounts[0] 
                  }
                })
              );
            }
          })
          .catch(error => {
            console.error('MetaMask connection error:', error);
            alert('Could not connect to MetaMask. Please try again.');
          });
      } else {
        // MetaMask is not installed
        if (this.isMobileBrowser()) {
          // On mobile, open MetaMask app or app store
          window.location.href = `https://metamask.app.link/dapp/${window.location.host}${window.location.pathname}`;
        } else {
          // On desktop, open MetaMask download page
          window.open('https://metamask.io/download/', '_blank');
        }
      }
    },
    
    isMobileBrowser() {
      return /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
    },
    
    addMessage(message) {
      this.messages.push(message);
      // Scroll to the bottom
      this.$nextTick(() => {
        if (this.$refs.messagesContainer) {
          this.$refs.messagesContainer.scrollTop = this.$refs.messagesContainer.scrollHeight;
        }
      });
    },
    
    formatMessage(text) {
      // Convert line breaks to <br> tags and format bullet points
      if (!text) return '';
      
      return text
        .replace(/\n/g, '<br>')
        .replace(/• (.*?)(?=<br>|$)/g, '<li>$1</li>') // Convert bullet points to list items
        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>'); // Bold markdown
    },
    
    formatAgentName(agentName) {
      // Add emoji based on agent type
      if (!agentName) return '🤖 AI Assistant';
      
      switch (agentName) {
        case 'OrchestratorAgent':
          return '🧠 Orchestrator';
        case 'StrategyAgent':
          return '📊 Strategy';
        case 'CreativeAgent':
          return '🎨 Creative';
        case 'ProductionAgent':
          return '⚙️ Production';
        case 'MediaAgent':
          return '📣 Media';
        default:
          return `🤖 ${agentName}`;
      }
    },
    
    checkMetaMaskConnection() {
      // Check if already authenticated in the page context
      if (window.ethereum && window.ethereum.selectedAddress) {
        this.isAuthenticated = true;
        this.userAddress = window.ethereum.selectedAddress;
      }
    }
  }
};