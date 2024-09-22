let liveText = '';
let summaryText = '';
let currentLanguage = 'en';
let ttsEnabled = false;
let keywords = [];

function toggleSettings() {
    const settingsPopup = document.getElementById('settings');
    settingsPopup.style.display = settingsPopup.style.display === 'block' ? 'none' : 'block';
}

function changeVoice() {
    const voice = document.getElementById('voiceSelect').value;
    console.log(`Voice changed to: ${voice}`);
    // Send voice change to backend
    fetch('/change_voice', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ voice: voice }),
    });
}

function changeLanguage() {
    currentLanguage = document.getElementById('languageSelect').value;
    console.log(`Language changed to: ${currentLanguage}`);
    // Send language change to backend
    fetch('/change_language', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ language: currentLanguage }),
    });
    updateLiveText();
    updateSummaryText();
}

function changeFont() {
    const font = document.getElementById('fontSelect').value;
    document.body.style.fontFamily = font;
}

function changeFontSize() {
    const fontSize = document.getElementById('fontSizeSelect').value;
    document.body.style.fontSize = fontSize === 'small' ? '14px' :
                                   fontSize === 'medium' ? '16px' :
                                   fontSize === 'large' ? '18px' :
                                   fontSize === 'x-large' ? '20px' : '24px';
}

function toggleTTS() {
    ttsEnabled = document.getElementById('ttsToggle').checked;
    console.log(`Text-to-Speech ${ttsEnabled ? 'enabled' : 'disabled'}`);
    // Send TTS toggle to backend
    fetch('/toggle_tts', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ enabled: ttsEnabled }),
    });
}

function toggleDarkMode() {
    document.body.classList.toggle('dark-mode');
}

function showDefinition(keyword) {
    fetch(`/get_definition?keyword=${keyword}&language=${currentLanguage}`)
        .then(response => response.json())
        .then(data => {
            document.getElementById('definitionText').textContent = data.definition;
            document.getElementById('definitionPopup').style.display = 'block';
        });
}

function closeDefinition() {
    document.getElementById('definitionPopup').style.display = 'none';
}

function updateLiveText() {
    fetch(`/get_live_text?language=${currentLanguage}`)
        .then(response => response.json())
        .then(data => {
            const liveTextElement = document.getElementById('liveText');
            liveText = data.text;
            keywords = data.keywords;
            liveTextElement.innerHTML = highlightKeywords(liveText);
            if (liveTextElement.scrollHeight > liveTextElement.clientHeight) {
                liveTextElement.scrollTop = liveTextElement.scrollHeight;
            }
        });
}

function updateSummaryText() {
    fetch(`/get_summary?language=${currentLanguage}`)
        .then(response => response.json())
        .then(data => {
            const summaryTextElement = document.getElementById('summaryText');
            summaryText = data.text;
            keywords = keywords.concat(data.keywords);
            summaryTextElement.innerHTML = highlightKeywords(summaryText);
            summaryTextElement.scrollTop = summaryTextElement.scrollHeight;
        });
}

function highlightKeywords(text) {
    keywords.forEach(keyword => {
        const regex = new RegExp(keyword, 'gi');
        text = text.replace(regex, `<span class="keyword" onclick="showDefinition('${keyword}')">${keyword}</span>`);
    });
    return text;
}

// Update live translation every 7 seconds
setInterval(updateLiveText, 7000);

// Update summary every 60 seconds
setInterval(updateSummaryText, 60000);

// Initialize dark mode
document.body.classList.add('dark-mode');