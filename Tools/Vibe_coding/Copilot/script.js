// 설정 모달 및 말투 모드 관리
let politeMode = localStorage.getItem('chatbot-polite-mode') || 'polite';

const settingsBtn = document.getElementById('settings-btn');
const settingsModal = document.getElementById('settings-modal');
const settingsCloseBtn = document.getElementById('settings-close-btn');
const politeRadios = document.getElementsByName('polite-mode');

function openSettingsModal() {
    settingsModal.classList.add('active');
    // 현재 모드 반영
    for (const radio of politeRadios) {
        radio.checked = (radio.value === politeMode);
    }
}
function closeSettingsModal() {
    settingsModal.classList.remove('active');
}
settingsBtn.addEventListener('click', openSettingsModal);
settingsCloseBtn.addEventListener('click', closeSettingsModal);
settingsModal.addEventListener('click', function(e) {
    if (e.target === settingsModal) closeSettingsModal();
});
for (const radio of politeRadios) {
    radio.addEventListener('change', function() {
        politeMode = this.value;
        localStorage.setItem('chatbot-polite-mode', politeMode);
    });
}
// 다크/라이트 모드 전환 스크립트
const modeSwitch = document.getElementById('mode-switch');
modeSwitch.addEventListener('change', function() {
    document.body.classList.toggle('dark', this.checked);
    localStorage.setItem('chatbot-darkmode', this.checked ? '1' : '0');
});

// 페이지 로드시 이전 모드 적용
window.addEventListener('DOMContentLoaded', function() {
    const isDark = localStorage.getItem('chatbot-darkmode') === '1';
    modeSwitch.checked = isDark;
    document.body.classList.toggle('dark', isDark);
});

const chatWindow = document.getElementById('chat-window');
const chatForm = document.getElementById('chat-form');
const userInput = document.getElementById('user-input');

// 오늘의 명언 리스트
const quotes = [
    '성공은 준비와 기회의 만남이다. - 세네카',
    '포기하지 마라. 큰일도 작은 용기에서 시작된다. - 라오쯔',
    '노력은 배신하지 않는다. - 손흥민',
    '실패는 성공의 어머니이다. - 속담',
    '오늘 걷지 않으면 내일은 뛰어야 한다. - 속담',
    '할 수 있다고 믿는 사람이 해낸다. - 베르길리우스',
    '작은 성취가 큰 변화를 만든다. - 속담',
    '시작이 반이다. - 속담',
    '행동이 모든 성공의 기초다. - 파블로 피카소',
    '꿈을 꾸는 자만이 미래를 본다. - 엘리노어 루즈벨트'
];

function showWelcomeMessage() {
    // 인사 메시지
    appendMessage('안녕하세요! 챗봇입니다.', 'bot');
    // 오늘의 명언을 플로팅 배너로 표시
    const randomIdx = Math.floor(Math.random() * quotes.length);
    const quote = quotes[randomIdx];
    const quoteDiv = document.getElementById('floating-quote');
    quoteDiv.innerHTML = `오늘의 명언: \"${quote}\"`;
}


function appendMessage(text, sender, isHtml = false) {
    const msgRow = document.createElement('div');
    msgRow.className = `msg-row ${sender}`;
    const avatar = document.createElement('div');
    avatar.className = 'avatar';
    avatar.innerHTML = sender === 'user' ? '<img src="https://cdn-icons-png.flaticon.com/512/1946/1946429.png" width="32" height="32"/>' : '<img src="https://cdn-icons-png.flaticon.com/512/4712/4712035.png" width="32" height="32"/>';
    const msgDiv = document.createElement('div');
    msgDiv.className = `message-bubble ${sender}`;
    if (isHtml) {
        msgDiv.innerHTML = text;
    } else {
        msgDiv.textContent = text;
    }
    if(sender === 'user') {
        msgRow.appendChild(msgDiv);
        msgRow.appendChild(avatar);
    } else {
        msgRow.appendChild(avatar);
        msgRow.appendChild(msgDiv);
    }
    chatWindow.appendChild(msgRow);
    chatWindow.scrollTop = chatWindow.scrollHeight;
}



// 대화 이력 저장 (택시 호출 서비스 챗봇 시스템 프롬프트 적용)
const chatHistory = [
    { role: 'system', content: `당신은 호출형 택시 서비스의 음성 안내 챗봇입니다.\n\n대화 시작 시 반드시 다음과 같이 인사하세요:\n\"안녕하세요! 택시 호출 서비스입니다. 먼저 출발지를 알려주시겠어요?\"\n\n그 다음 목표는 사용자의 \"출발지\"와 \"도착지\" 정보를 자연스럽고 정확하게 파악하는 것입니다.\n\n규칙:\n- 사용자가 명확히 대답하지 않으면 다시 한번 친절하게 질문하세요.\n- 지명, 건물 이름, 병원, 역, 아파트, 회사 등 어떤 표현도 이해하고 받아들이세요.\n- 사용자가 \"여기\" 또는 \"내 위치\"라고 말하면 \"정확한 위치를 알기 위해 주소나 근처 건물 이름을 알려달라\"고 답하세요.\n- 출발지와 도착지를 모두 확인하면 \"이제 택시를 배차해드릴게요. 잠시만 기다려주세요.\"라고 마무리하세요.\n- 한 번에 하나의 질문만 하세요.\n- 톤은 공손하고 자연스러우며 부담스럽지 않게 유지하세요.\n- 항상 한국어로 대답하세요.` }
];

// OpenAI GPT-4o-mini API로 답변 요청 (이전 대화 이력 포함, 말투 반영)
async function botReply(userText) {
    const apiKey = ''; // 여기에 본인의 OpenAI API 키를 입력하세요
    const endpoint = 'https://api.openai.com/v1/chat/completions';
    const headers = {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${apiKey}`
    };
    // 대화 이력에 사용자 메시지 추가
    chatHistory.push({ role: 'user', content: userText });
    // 시스템 프롬프트에 말투 옵션 추가
    let systemPrompt = chatHistory[0].content;
    if (politeMode === 'casual') {
        systemPrompt += '\n\n추가 규칙: 반드시 반말로만 대답하세요.';
    } else {
        systemPrompt += '\n\n추가 규칙: 반드시 존댓말로만 대답하세요.';
    }
    const messages = [
        { role: 'system', content: systemPrompt },
        ...chatHistory.slice(1).slice(-20)
    ];
    const body = {
        model: 'gpt-4o-mini',
        messages: messages,
        max_tokens: 100
    };
    try {
        const res = await fetch(endpoint, {
            method: 'POST',
            headers,
            body: JSON.stringify(body)
        });
        if (!res.ok) throw new Error('API 오류');
        const data = await res.json();
        const reply = data.choices[0].message.content.trim();
        // 대화 이력에 챗봇 답변 추가
        chatHistory.push({ role: 'assistant', content: reply });
        return reply;
    } catch (e) {
        return '죄송해요, 답변을 가져오지 못했어요.';
    }
}



async function sendMessage() {
    const text = userInput.value.trim();
    if (!text) return;
    appendMessage(text, 'user');
    userInput.value = '';
    appendMessage('답변 생성 중...', 'bot');
    const botMsgDivs = chatWindow.querySelectorAll('.msg-row.bot .message-bubble');
    const loadingDiv = botMsgDivs[botMsgDivs.length - 1];
    const reply = await botReply(text);
    loadingDiv.textContent = reply;
}


// 페이지 로드 시 인사 및 명언 출력
window.addEventListener('DOMContentLoaded', showWelcomeMessage);

chatForm.addEventListener('submit', function(e) {
    e.preventDefault();
    sendMessage();
});

userInput.addEventListener('keydown', function(e) {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
    }
});
