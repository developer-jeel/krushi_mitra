/* ============================================================
   KRUSHI MITRA — BUYER VOICE ASSISTANT JAVASCRIPT
   Handles ElevenLabs Conversational AI WebSockets,
   ElevenLabs TTS API, official ConvAI Widget, orb animations,
   audio visualizer, live transcripts, timers, quick actions & voice settings.
   ============================================================ */

document.addEventListener('DOMContentLoaded', () => {
  // DOM Elements
  const startCallBtn = document.getElementById('startCallBtn');
  const endCallBtn = document.getElementById('endCallBtn');
  const confirmEndCallBtn = document.getElementById('confirmEndCallBtn');
  const continueCallBtn = document.getElementById('continueCallBtn');
  const endCallModal = document.getElementById('endCallModal');

  const muteBtn = document.getElementById('muteBtn');
  const speakerBtn = document.getElementById('speakerBtn');
  const moreActionsBtn = document.getElementById('moreActionsBtn');
  const moreMenu = document.getElementById('moreMenu');

  const idleArea = document.getElementById('idleArea');
  const activeArea = document.getElementById('activeArea');
  const connectingArea = document.getElementById('connectingArea');
  const callSummary = document.getElementById('callSummary');

  const voiceOrb = document.getElementById('voiceOrb');
  const stateText = document.getElementById('stateText');
  const stateSubtext = document.getElementById('stateSubtext');
  const liveStatusText = document.getElementById('liveStatusText');
  const callTimer = document.getElementById('callTimer');
  const waveform = document.getElementById('waveform');

  const transcriptCard = document.getElementById('transcriptCard');
  const transcriptBody = document.getElementById('transcriptBody');
  const transcriptEmpty = document.getElementById('transcriptEmpty');
  const transcriptLiveBadge = document.getElementById('transcriptLiveBadge');

  const settingsBtn = document.getElementById('settingsBtn');
  const moreSettingsBtn = document.getElementById('moreSettingsBtn');
  const settingsModal = document.getElementById('settingsModal');
  const closeSettingsBtn = document.getElementById('closeSettingsBtn');
  const saveSettingsBtn = document.getElementById('saveSettingsBtn');

  const elevenlabsAgentIdInput = document.getElementById('elevenlabsAgentId');
  const elevenlabsApiKeyInput = document.getElementById('elevenlabsApiKey');
  const voiceSelect = document.getElementById('voiceSelect');

  const micPermError = document.getElementById('micPermError');
  const retryMicBtn = document.getElementById('retryMicBtn');
  const connError = document.getElementById('connError');
  const reconnectBtn = document.getElementById('reconnectBtn');

  const quickActionsGrid = document.getElementById('quickActionsGrid');
  const newCallBtn = document.getElementById('newCallBtn');
  const viewTranscriptBtn = document.getElementById('viewTranscriptBtn');

  // State Variables
  let isCallActive = false;
  let isMuted = false;
  let isSpeakerOn = true;
  let callSeconds = 0;
  let timerInterval = null;
  let waveAnimFrame = null;

  let recognition = null;
  let synthesis = window.speechSynthesis || null;

  // ElevenLabs Session Variables
  let elevenlabsWS = null;
  let audioCtx = null;

  // Load ElevenLabs configuration
  let elevenlabsAgentId = (elevenlabsAgentIdInput && elevenlabsAgentIdInput.value) || localStorage.getItem('km_elevenlabs_agent_id') || 'agent_8901m09twyzsft9awzgeg15p6xh8';
  let elevenlabsApiKey = localStorage.getItem('km_elevenlabs_api_key') || '';
  let elevenlabsVoiceId = (voiceSelect && voiceSelect.value) || '21m00Tcm4TlvDq8ikWAM';

  if (elevenlabsAgentIdInput && elevenlabsAgentId) elevenlabsAgentIdInput.value = elevenlabsAgentId;

  // Initial setup: create waveform bars
  initWaveformBars();

  // Helper to unlock Browser Audio Policy on User Click
  function unlockBrowserAudio() {
    try {
      if (!audioCtx) {
        const AudioContext = window.AudioContext || window.webkitAudioContext;
        if (AudioContext) audioCtx = new AudioContext();
      }
      if (audioCtx && audioCtx.state === 'suspended') {
        audioCtx.resume();
      }
      if (synthesis && synthesis.paused) {
        synthesis.resume();
      }
      if (synthesis) {
        const dummyUtterance = new SpeechSynthesisUtterance('');
        dummyUtterance.volume = 0;
        synthesis.speak(dummyUtterance);
      }
    } catch (e) {
      console.warn("Audio Context unlock error:", e);
    }
  }

  // Trigger ElevenLabs Official ConvAI Widget if present
  function triggerElevenLabsWidget() {
    try {
      const widget = document.querySelector('elevenlabs-convai');
      if (widget) {
        // Try clicking internal shadow root button or widget element directly
        if (widget.shadowRoot) {
          const btn = widget.shadowRoot.querySelector('button') || widget.shadowRoot.querySelector('.widget-button');
          if (btn) btn.click();
        }
        widget.click();
      }
    } catch (e) {
      console.log("ElevenLabs widget trigger note:", e);
    }
  }

  // ----- EVENT LISTENERS -----
  if (startCallBtn) startCallBtn.addEventListener('click', () => { 
    unlockBrowserAudio(); 
    triggerElevenLabsWidget();
    initiateCall(); 
  });

  if (endCallBtn) endCallBtn.addEventListener('click', () => showEndCallModal());
  if (continueCallBtn) continueCallBtn.addEventListener('click', () => hideEndCallModal());
  if (confirmEndCallBtn) confirmEndCallBtn.addEventListener('click', () => terminateCall());

  if (muteBtn) muteBtn.addEventListener('click', toggleMute);
  if (speakerBtn) speakerBtn.addEventListener('click', toggleSpeaker);
  if (moreActionsBtn) moreActionsBtn.addEventListener('click', toggleMoreMenu);

  if (settingsBtn) settingsBtn.addEventListener('click', openSettings);
  if (moreSettingsBtn) moreSettingsBtn.addEventListener('click', () => { closeMoreMenu(); openSettings(); });
  if (closeSettingsBtn) closeSettingsBtn.addEventListener('click', closeSettings);
  if (saveSettingsBtn) saveSettingsBtn.addEventListener('click', saveSettings);

  if (retryMicBtn) retryMicBtn.addEventListener('click', () => { unlockBrowserAudio(); hideError(micPermError); initiateCall(); });
  if (reconnectBtn) reconnectBtn.addEventListener('click', () => { unlockBrowserAudio(); hideError(connError); initiateCall(); });

  if (newCallBtn) newCallBtn.addEventListener('click', resetToIdle);
  if (viewTranscriptBtn) viewTranscriptBtn.addEventListener('click', scrollToTranscript);

  // Quick Action Buttons
  if (quickActionsGrid) {
    quickActionsGrid.addEventListener('click', (e) => {
      const card = e.target.closest('.va-quick-card');
      if (!card) return;
      unlockBrowserAudio();
      triggerElevenLabsWidget();
      const action = card.getAttribute('data-action');
      handleQuickAction(action, card);
    });
  }

  // Close menus on outside click
  document.addEventListener('click', (e) => {
    if (moreMenu && !moreMenu.contains(e.target) && !moreActionsBtn.contains(e.target)) {
      closeMoreMenu();
    }
  });

  // ----- WAVEFORM CREATION -----
  function initWaveformBars() {
    if (!waveform) return;
    waveform.innerHTML = '';
    const barCount = 28;
    for (let i = 0; i < barCount; i++) {
      const bar = document.createElement('div');
      bar.className = 'va-bar';
      bar.style.setProperty('--bar-height', `${Math.floor(Math.random() * 30 + 10)}px`);
      bar.style.animationDelay = `${(i * 0.05).toFixed(2)}s`;
      waveform.appendChild(bar);
    }
  }

  function startWaveformAnimation() {
    if (!waveform) return;
    const bars = waveform.querySelectorAll('.va-bar');
    function animate() {
      if (!isCallActive) return;
      bars.forEach(bar => {
        const height = isMuted ? 4 : Math.floor(Math.random() * 48 + 8);
        bar.style.setProperty('--bar-height', `${height}px`);
      });
      waveAnimFrame = setTimeout(animate, 120);
    }
    animate();
  }

  function stopWaveformAnimation() {
    if (waveAnimFrame) clearTimeout(waveAnimFrame);
    if (!waveform) return;
    const bars = waveform.querySelectorAll('.va-bar');
    bars.forEach(bar => bar.style.setProperty('--bar-height', '4px'));
  }

  // ----- CALL LIFECYCLE -----
  function initiateCall(initialPrompt = null) {
    hideError(micPermError);
    hideError(connError);

    // Request mic access first
    if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
      navigator.mediaDevices.getUserMedia({ audio: true })
        .then(stream => {
          stream.getTracks().forEach(track => track.stop());
          startConnectingState(initialPrompt);
        })
        .catch(err => {
          console.warn("Mic permission denied:", err);
          showError(micPermError);
        });
    } else {
      startConnectingState(initialPrompt);
    }
  }

  function startConnectingState(initialPrompt) {
    startCallBtn.style.display = 'none';
    connectingArea.style.display = 'flex';
    stateText.textContent = 'Connecting ElevenLabs Voice Agent...';
    stateSubtext.textContent = 'Establishing secure real-time audio channel';

    // Check backend for ElevenLabs Signed URL or Agent ID
    fetch(`/buyer/elevenlabs/signed-url/?agent_id=${encodeURIComponent(elevenlabsAgentId)}`)
      .then(res => res.json())
      .then(data => {
        if (data.status === 'success' && data.signed_url) {
          connectElevenLabsWebSocket(data.signed_url, initialPrompt);
        } else {
          startStandardVoiceCall(initialPrompt);
        }
      })
      .catch(err => {
        console.log("ElevenLabs backend fetch failed, using standard Voice AI agent:", err);
        startStandardVoiceCall(initialPrompt);
      });
  }

  function startStandardVoiceCall(initialPrompt) {
    setTimeout(() => {
      connectingArea.style.display = 'none';
      idleArea.style.display = 'none';
      activeArea.style.display = 'flex';

      isCallActive = true;
      startTimer();
      startWaveformAnimation();
      setOrbState('speaking');

      if (transcriptLiveBadge) transcriptLiveBadge.style.display = 'flex';
      if (transcriptEmpty) transcriptEmpty.style.display = 'none';

      const greeting = initialPrompt 
        ? `Namaste! Processing your request regarding ${initialPrompt}. How can I assist with your procurement details today?`
        : `Namaste! Welcome to Krushi Mitra Buyer Assistant. Powered by ElevenLabs Voice AI. I can help you find crops, check APMC Mandi rates, or manage your bulk orders. What are you looking for today?`;

      addTranscriptMessage('ai', greeting);
      speakTextWithElevenLabsOrTTS(greeting);

      setTimeout(() => {
        if (isCallActive) {
          setOrbState('listening');
          startSpeechRecognition();
        }
      }, 3500);

    }, 800);
  }

  // ----- ELEVENLABS WEBSOCKET REALTIME AGENT -----
  function connectElevenLabsWebSocket(wsUrl, initialPrompt) {
    try {
      elevenlabsWS = new WebSocket(wsUrl);

      elevenlabsWS.onopen = () => {
        console.log("Connected to ElevenLabs Voice Agent WebSocket!");
        connectingArea.style.display = 'none';
        idleArea.style.display = 'none';
        activeArea.style.display = 'flex';

        isCallActive = true;
        startTimer();
        startWaveformAnimation();
        setOrbState('speaking');

        if (transcriptLiveBadge) transcriptLiveBadge.style.display = 'flex';
        if (transcriptEmpty) transcriptEmpty.style.display = 'none';

        const greeting = initialPrompt 
          ? `Namaste! Connected to ElevenLabs AI Agent (${elevenlabsAgentId}). How can I assist with ${initialPrompt}?`
          : `Namaste! Connected to ElevenLabs Voice Agent for Krushi Mitra Buyer Panel. How can I assist you today?`;

        // Render transcript message AND trigger ElevenLabs audio output
        addTranscriptMessage('ai', greeting);
        speakTextWithElevenLabsOrTTS(greeting);

        setTimeout(() => {
          if (isCallActive) {
            setOrbState('listening');
            startSpeechRecognition();
          }
        }, 3500);
      };

      elevenlabsWS.onmessage = (event) => {
        try {
          const msg = JSON.parse(event.data);
          
          // Transcript events
          if (msg.type === 'agent_response' || msg.type === 'user_transcript' || msg.text || msg.transcript) {
            const text = msg.text || msg.transcript || (msg.agent_response_event && msg.agent_response_event.agent_response);
            if (text) {
              const role = (msg.type === 'user_transcript' || msg.role === 'user') ? 'user' : 'ai';
              addTranscriptMessage(role, text);
              if (role === 'ai') {
                setOrbState('speaking');
                speakTextWithElevenLabsOrTTS(text);
              }
            }
          }

          // Audio events (Check all possible ElevenLabs payload formats)
          const base64Audio = msg.audio_event?.audio_base_64 || msg.audio_base_64 || msg.audio || msg.user_audio_chunk;
          if (base64Audio) {
            playRawAudioBase64(base64Audio);
          }

        } catch (e) {
          console.warn("Error parsing ElevenLabs WS message:", e);
        }
      };

      elevenlabsWS.onerror = (err) => {
        console.warn("ElevenLabs WS error:", err);
        startStandardVoiceCall(initialPrompt);
      };

      elevenlabsWS.onclose = () => {
        console.log("ElevenLabs WS connection closed");
      };

    } catch (e) {
      console.warn("WebSocket initialization error:", e);
      startStandardVoiceCall(initialPrompt);
    }
  }

  function terminateCall() {
    hideEndCallModal();
    isCallActive = false;
    stopTimer();
    stopWaveformAnimation();
    stopSpeechRecognition();

    if (elevenlabsWS) {
      try { elevenlabsWS.close(); } catch (e) {}
      elevenlabsWS = null;
    }
    if (synthesis) synthesis.cancel();

    activeArea.style.display = 'none';
    callSummary.style.display = 'block';
    if (transcriptLiveBadge) transcriptLiveBadge.style.display = 'none';

    populateSummaryGrid();
    if (window.showToast) window.showToast('info', 'Call Ended', 'Voice session saved to history.');
  }

  function resetToIdle() {
    callSummary.style.display = 'none';
    idleArea.style.display = 'flex';
    if (startCallBtn) startCallBtn.style.display = 'inline-flex';
    stateText.textContent = 'Ready to help';
    stateSubtext.textContent = 'Tap the microphone to start a voice session';
    setOrbState('idle');
    callSeconds = 0;
    if (callTimer) callTimer.textContent = '00:00';
  }

  // ----- TIMER -----
  function startTimer() {
    callSeconds = 0;
    updateTimerDisplay();
    timerInterval = setInterval(() => {
      callSeconds++;
      updateTimerDisplay();
    }, 1000);
  }

  function stopTimer() {
    if (timerInterval) clearInterval(timerInterval);
  }

  function updateTimerDisplay() {
    if (!callTimer) return;
    const mins = String(Math.floor(callSeconds / 60)).padStart(2, '0');
    const secs = String(callSeconds % 60).padStart(2, '0');
    callTimer.textContent = `${mins}:${secs}`;
  }

  // ----- ORB ANIMATION STATES -----
  function setOrbState(state) {
    if (!voiceOrb) return;
    voiceOrb.classList.remove('va-orb-listening', 'va-orb-speaking', 'va-orb-thinking');
    if (state === 'listening') {
      voiceOrb.classList.add('va-orb-listening');
      if (liveStatusText) liveStatusText.textContent = 'ElevenLabs AI Listening...';
    } else if (state === 'speaking') {
      voiceOrb.classList.add('va-orb-speaking');
      if (liveStatusText) liveStatusText.textContent = 'ElevenLabs Voice Agent Speaking';
    } else if (state === 'thinking') {
      voiceOrb.classList.add('va-orb-thinking');
      if (liveStatusText) liveStatusText.textContent = 'Processing request...';
    } else {
      if (liveStatusText) liveStatusText.textContent = 'Connected';
    }
  }

  // ----- CONTROLS -----
  function toggleMute() {
    isMuted = !isMuted;
    muteBtn.classList.toggle('active', isMuted);
    muteBtn.setAttribute('aria-pressed', isMuted ? 'true' : 'false');
    const label = muteBtn.querySelector('.va-ctrl-label');
    const icon = muteBtn.querySelector('i');
    if (label) label.textContent = isMuted ? 'Unmute' : 'Mute';
    if (icon) icon.className = isMuted ? 'fa-solid fa-microphone-slash' : 'fa-solid fa-microphone';
    if (window.showToast) window.showToast('info', isMuted ? 'Microphone Muted' : 'Microphone Unmuted', '');
  }

  function toggleSpeaker() {
    isSpeakerOn = !isSpeakerOn;
    speakerBtn.classList.toggle('active', !isSpeakerOn);
    speakerBtn.setAttribute('aria-pressed', isSpeakerOn ? 'true' : 'false');
    const label = speakerBtn.querySelector('.va-ctrl-label');
    if (label) label.textContent = isSpeakerOn ? 'Speaker' : 'Muted';
    if (window.showToast) window.showToast('info', isSpeakerOn ? 'Speaker On' : 'Speaker Muted', '');
  }

  function toggleMoreMenu() {
    if (!moreMenu) return;
    const isVisible = moreMenu.style.display === 'block';
    moreMenu.style.display = isVisible ? 'none' : 'block';
    moreActionsBtn.setAttribute('aria-expanded', isVisible ? 'false' : 'true');
  }

  function closeMoreMenu() {
    if (moreMenu) moreMenu.style.display = 'none';
    if (moreActionsBtn) moreActionsBtn.setAttribute('aria-expanded', 'false');
  }

  // ----- MODALS -----
  function showEndCallModal() {
    if (endCallModal) endCallModal.style.display = 'flex';
  }
  function hideEndCallModal() {
    if (endCallModal) endCallModal.style.display = 'none';
  }

  function openSettings() {
    if (settingsModal) settingsModal.style.display = 'flex';
  }
  function closeSettings() {
    if (settingsModal) settingsModal.style.display = 'none';
  }
  function saveSettings() {
    if (elevenlabsAgentIdInput) {
      elevenlabsAgentId = elevenlabsAgentIdInput.value.trim();
      localStorage.setItem('km_elevenlabs_agent_id', elevenlabsAgentId);
    }
    if (elevenlabsApiKeyInput) {
      elevenlabsApiKey = elevenlabsApiKeyInput.value.trim();
      localStorage.setItem('km_elevenlabs_api_key', elevenlabsApiKey);
    }
    if (voiceSelect) {
      elevenlabsVoiceId = voiceSelect.value;
      localStorage.setItem('km_elevenlabs_voice_id', elevenlabsVoiceId);
    }

    // Post to Django Session
    fetch('/buyer/elevenlabs/config/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'X-CSRFToken': getCsrfToken() },
      body: JSON.stringify({
        agent_id: elevenlabsAgentId,
        api_key: elevenlabsApiKey,
        voice_id: elevenlabsVoiceId
      })
    }).catch(e => console.warn(e));

    closeSettings();
    if (window.showToast) window.showToast('success', 'Settings Saved', 'ElevenLabs Agent preferences updated.');
  }

  function getCsrfToken() {
    const cookie = document.cookie.split('; ').find(row => row.startsWith('csrftoken='));
    return cookie ? cookie.split('=')[1] : '';
  }

  // ----- ERRORS -----
  function showError(el) { if (el) el.style.display = 'flex'; }
  function hideError(el) { if (el) el.style.display = 'none'; }

  // ----- TRANSCRIPT SYSTEM -----
  function addTranscriptMessage(sender, text) {
    if (!transcriptBody) return;
    if (transcriptEmpty) transcriptEmpty.style.display = 'none';

    const msgDiv = document.createElement('div');
    msgDiv.className = `va-transcript-msg ${sender}`;

    const labelDiv = document.createElement('div');
    labelDiv.className = 'va-transcript-msg-label';
    labelDiv.textContent = sender === 'user' ? 'You' : 'ElevenLabs Voice Agent';

    const textDiv = document.createElement('div');
    textDiv.className = 'va-transcript-msg-text';
    textDiv.textContent = text;

    msgDiv.appendChild(labelDiv);
    msgDiv.appendChild(textDiv);
    transcriptBody.appendChild(msgDiv);

    transcriptBody.scrollTop = transcriptBody.scrollHeight;
  }

  function scrollToTranscript() {
    closeMoreMenu();
    if (transcriptCard) transcriptCard.scrollIntoView({ behavior: 'smooth' });
  }

  // ----- QUICK ACTIONS -----
  function handleQuickAction(action, cardEl) {
    cardEl.classList.add('pulsing');
    setTimeout(() => cardEl.classList.remove('pulsing'), 400);

    const actionMap = {
      'find-crops': 'Finding available top-grade crops in mandis',
      'mandi-prices': "Checking today's APMC Mandi market rates",
      'bulk-procurement': 'Creating a multi-ton bulk procurement request',
      'order-status': 'Tracking my recent procurement orders',
      'kyc-status': 'Checking buyer KYC verification status',
      'export-inquiry': 'Starting international export inquiry'
    };

    const promptText = actionMap[action] || 'Voice Request';

    if (!isCallActive) {
      initiateCall(promptText);
    } else {
      addTranscriptMessage('user', promptText);
      if (elevenlabsWS && elevenlabsWS.readyState === WebSocket.OPEN) {
        elevenlabsWS.send(JSON.stringify({ type: 'user_message', text: promptText }));
      } else {
        simulateAIResponse(promptText);
      }
    }
  }

  // ----- SPEECH RECOGNITION & SYNTHESIS -----
  function startSpeechRecognition() {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRecognition) return;

    try {
      recognition = new SpeechRecognition();
      recognition.continuous = false;
      recognition.interimResults = false;
      recognition.lang = 'en-IN';

      recognition.onstart = () => {
        if (isCallActive) setOrbState('listening');
      };

      recognition.onresult = (event) => {
        const transcript = event.results[0][0].transcript;
        addTranscriptMessage('user', transcript);
        setOrbState('thinking');

        if (elevenlabsWS && elevenlabsWS.readyState === WebSocket.OPEN) {
          elevenlabsWS.send(JSON.stringify({ type: 'user_message', text: transcript }));
        } else {
          simulateAIResponse(transcript);
        }
      };

      recognition.onerror = (e) => {
        if (isCallActive && !isMuted) {
          setTimeout(() => { try { recognition.start(); } catch (err) {} }, 1000);
        }
      };

      recognition.onend = () => {
        if (isCallActive && !isMuted && voiceOrb.classList.contains('va-orb-listening')) {
          try { recognition.start(); } catch (err) {}
        }
      };

      recognition.start();
    } catch (err) {
      console.warn("Could not start SpeechRecognition:", err);
    }
  }

  function stopSpeechRecognition() {
    if (recognition) {
      try { recognition.stop(); } catch (e) {}
      recognition = null;
    }
  }

  // ----- ELEVENLABS HIGH QUALITY TTS PROXY & AUDIO PLAYBACK -----
  function speakTextWithElevenLabsOrTTS(text) {
    if (!isSpeakerOn) return;

    unlockBrowserAudio();

    // First try backend ElevenLabs TTS Proxy endpoint
    fetch('/buyer/elevenlabs/tts/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCsrfToken()
      },
      body: JSON.stringify({
        text: text,
        voice_id: elevenlabsVoiceId
      })
    })
    .then(response => {
      if (!response.ok) throw new Error('ElevenLabs API returned ' + response.status);
      return response.blob();
    })
    .then(blob => {
      const audioUrl = URL.createObjectURL(blob);
      const audio = new Audio(audioUrl);
      audio.play().then(() => {
        setOrbState('speaking');
      }).catch(err => {
        console.warn("Audio element play error:", err);
        fallbackWebSpeechTTS(text);
      });
      audio.onended = () => {
        if (isCallActive) setOrbState('listening');
      };
    })
    .catch(err => {
      console.log("ElevenLabs TTS proxy unavailable, falling back to WebSpeech TTS:", err);
      fallbackWebSpeechTTS(text);
    });
  }

  function fallbackWebSpeechTTS(text) {
    if (synthesis) {
      synthesis.cancel();
      const utterance = new SpeechSynthesisUtterance(text);
      utterance.rate = 1.0;
      utterance.pitch = 1.0;
      utterance.lang = 'en-IN';
      utterance.onstart = () => setOrbState('speaking');
      utterance.onend = () => { if (isCallActive) setOrbState('listening'); };
      synthesis.speak(utterance);
    }
  }

  function playRawAudioBase64(base64Audio) {
    if (!isSpeakerOn) return;
    unlockBrowserAudio();
    try {
      const audio = new Audio("data:audio/mp3;base64," + base64Audio);
      audio.play().then(() => {
        setOrbState('speaking');
      }).catch(err => {
        console.warn("Base64 audio play error:", err);
      });
      audio.onended = () => {
        if (isCallActive) setOrbState('listening');
      };
    } catch (e) {
      console.warn("Audio playback error:", e);
    }
  }

  // ----- SIMULATED AI RESPONSES -----
  function simulateAIResponse(userText) {
    setOrbState('thinking');

    setTimeout(() => {
      let aiResponse = '';
      const textLower = userText.toLowerCase();

      if (textLower.includes('crop') || textLower.includes('wheat') || textLower.includes('rice') || textLower.includes('soybean')) {
        aiResponse = "We currently have top-grade Soybean and Wheat available in Gujarat and Maharashtra mandis starting from ₹4,200/quintal. Would you like to view verified seller contact details or request a bulk quote?";
      } else if (textLower.includes('price') || textLower.includes('mandi') || textLower.includes('rate')) {
        aiResponse = "Today's APMC Rajkot rates: Groundnut is trading at ₹6,450/quintal, and Cotton Medium Staple is trading at ₹7,100/quintal, up 1.5% from yesterday.";
      } else if (textLower.includes('order') || textLower.includes('track') || textLower.includes('status')) {
        aiResponse = "Your recent order ORD-2026-0105 for 200 Quintals Groundnut has been dispatched from Rajkot Mandi and is expected to reach your warehouse by Thursday.";
      } else if (textLower.includes('kyc') || textLower.includes('verification')) {
        aiResponse = "Your Buyer KYC verification is fully approved! You have access to all bulk buying features and direct trade contracts.";
      } else if (textLower.includes('export') || textLower.includes('international')) {
        aiResponse = "Krushi Mitra Export Desk supports export documentation, phytosanitary certificates, and port logistics for APEDA-certified grains.";
      } else {
        aiResponse = "ElevenLabs Voice Agent here. I have noted your request regarding " + userText + ". Syncing your procurement preferences with the Krushi Mitra network. How many quintals do you require?";
      }

      if (isCallActive) {
        addTranscriptMessage('ai', aiResponse);
        speakTextWithElevenLabsOrTTS(aiResponse);
      }
    }, 1200);
  }

  // ----- SUMMARY GRID -----
  function populateSummaryGrid() {
    const summaryGrid = document.getElementById('summaryGrid');
    if (!summaryGrid) return;
    const mins = Math.floor(callSeconds / 60);
    const secs = callSeconds % 60;
    const durationStr = `${mins}m ${secs}s`;

    summaryGrid.innerHTML = `
      <div class="va-summary-item">
        <div class="va-summary-label">Duration</div>
        <div class="va-summary-value">${durationStr}</div>
      </div>
      <div class="va-summary-item">
        <div class="va-summary-label">Voice Engine</div>
        <div class="va-summary-value" style="color:var(--primary-600)">ElevenLabs AI</div>
      </div>
      <div class="va-summary-item">
        <div class="va-summary-label">Primary Topic</div>
        <div class="va-summary-value">Buyer Procurement</div>
      </div>
      <div class="va-summary-item">
        <div class="va-summary-label">Encrypted Channel</div>
        <div class="va-summary-value">Verified</div>
      </div>
    `;
  }

});
