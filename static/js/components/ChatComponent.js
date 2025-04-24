// ChatComponent.js - Vue 3 Component for Narrative Chat Experience

export default {
  name: 'ChatComponent',
  template: `
    <div class="chat-container">
      <!-- Chat messages -->
      <div class="messages-container" ref="messagesContainer">
        <div v-for="msg in messages" :key="msg.id" class="message" :class="msg.role">
          <div class="message-text" v-html="formatMessage(msg.text)"></div>
          <div v-if="msg.agent && msg.agent !== 'user'" class="agent-badge">{{ msg.agent }}</div>
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
              :disabled="isTyping || messageCount >= MAX_FREE_MESSAGES && !isAuthenticated"
              class="form-control" 
              placeholder="Type your response..." 
              ref="inputField"
            />
            <button 
              type="submit" 
              class="btn btn-primary" 
              :disabled="isTyping || !userInput || (messageCount >= MAX_FREE_MESSAGES && !isAuthenticated)"
            >
              <i class="fas fa-paper-plane"></i>
            </button>
          </div>
        </form>
        <div v-if="messageCount >= MAX_FREE_MESSAGES - 2 && !isAuthenticated" class="message-limit-warning">
          {{ messageCount === MAX_FREE_MESSAGES - 1 ? 
            "This is your last free message. Connect with MetaMask for unlimited access." : 
            `You have ${MAX_FREE_MESSAGES - messageCount} more free messages. Connect with MetaMask for unlimited access.` 
          }}
        </div>
      </div>
    </div>
  `,
  
  data() {
    return {
      messages: [],
      userInput: '',
      isTyping: false,
      messageCount: 0,
      isAuthenticated: false,
      userAddress: null,
      MAX_FREE_MESSAGES: 10
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
          this.addMessage({
            id: Date.now(),
            role: 'agent',
            agent: data.agent || 'OrchestratorAgent',
            text: data.reply
          });
        } else {
          throw new Error('Failed to start conversation');
        }
      } catch (error) {
        console.error('Error starting conversation:', error);
        this.addMessage({
          id: Date.now(),
          role: 'agent',
          text: "I apologize, but I'm having trouble connecting. Please try again in a moment."
        });
      } finally {
        this.isTyping = false;
      }
    },
    
    async sendMessage() {
      if (!this.userInput.trim()) return;
      
      // Check for message limit
      if (this.messageCount >= this.MAX_FREE_MESSAGES && !this.isAuthenticated) {
        this.addMessage({
          id: Date.now(),
          role: 'agent',
          agent: 'OrchestratorAgent',
          text: "You've reached the message limit. Please connect with MetaMask to continue chatting with the AI agent."
        });
        return;
      }
      
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
          this.addMessage({
            id: Date.now(),
            role: 'agent',
            agent: data.agent || 'OrchestratorAgent',
            text: data.reply
          });
          
          // Increment message count for non-authenticated users
          if (!this.isAuthenticated) {
            this.messageCount++;
          }
        } else {
          throw new Error('Failed to get response');
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
      return text
        .replace(/\n/g, '<br>')
        .replace(/• (.*?)(?=<br>|$)/g, '<li>$1</li>') // Convert bullet points to list items
        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>'); // Bold markdown
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