function toggleSettings() {
    const settingsPopup = document.getElementById('settings');
    settingsPopup.style.display = settingsPopup.style.display === 'block' ? 'none' : 'block';
}

function changeVoice() {
    const voice = document.getElementById('voiceSelect').value;
    console.log(`Voice changed to: ${voice}`);
    // Implement voice change logic here
    updateTextToSpeech(voice);
}

function changeLanguage() {
    const language = document.getElementById('languageSelect').value;
    console.log(`Language changed to: ${language}`);
    // Implement language change logic here
    updateLiveText(language);
    updateSummaryText(language);
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
    const ttsEnabled = document.getElementById('ttsToggle').checked;
    console.log(`Text-to-Speech ${ttsEnabled ? 'enabled' : 'disabled'}`);
    // Implement TTS logic here
    if (ttsEnabled) {
        startAudioTranscription();
    } else {
        stopAudioTranscription();
    }
}

function toggleDarkMode() {
    document.body.classList.toggle('dark-mode');
}

function showDefinition(keyword) {
    const definitions = {
        keyword1: "This is the definition of keyword 1.",
        keyword2: "This is the definition of keyword 2."
    };
    document.getElementById('definitionText').textContent = definitions[keyword];
    document.getElementById('definitionPopup').style.display = 'block';
}

function closeDefinition() {
    document.getElementById('definitionPopup').style.display = 'none';
}

let liveText = '';
let summaryText = '';
let currentLanguage = 'en';

function updateLiveText(language = currentLanguage) {
    const liveTextElement = document.getElementById('liveText');
    if (liveText.length > 3400) {
        liveText = liveText.slice(3000) + translateText(sentences[0], language) + ' ';
    } else {
        liveText += translateText(sentences[0], language) + ' ';
    }
    liveTextElement.innerHTML = liveText;
    sentences.push(sentences.shift());

    // Check if text reached bottom and shift page if necessary
    if (liveTextElement.scrollHeight > liveTextElement.clientHeight) {
        window.scrollBy(0, 20); // Adjust this value as needed
    }
}

function updateSummaryText(language = currentLanguage) {
    const summaryTextElement = document.getElementById('summaryText');
    summaryText += translateText(sentences[0], language) + ' ';
    summaryTextElement.innerHTML = summaryText;
    sentences.push(sentences.shift());

    // Scroll to bottom of summary
    summaryTextElement.scrollTop = summaryTextElement.scrollHeight;
}

// Update live translation every 7 seconds
setInterval(updateLiveText, 7000);

// Update summary every 60 seconds (after a complete cycle of live translation)
setInterval(updateSummaryText, 60000);

// Initialize dark mode
document.body.classList.add('dark-mode');