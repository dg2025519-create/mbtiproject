import streamlit as st
import random

# 페이지 설정
st.set_page_config(
    page_title="MBTI 포켓몬 테스트 ✨",
    page_icon="⚡",
    layout="centered"
)

# 커스텀 CSS
st.markdown("""
<style>
    .main {
        background: linear-gradient(135deg, #ffeef8 0%, #e0f7ff 100%);
    }
    .stButton>button {
        background: linear-gradient(90deg, #ff9a9e 0%, #fad0c4 100%);
        color: white;
        border: none;
        border-radius: 20px;
        padding: 10px 24px;
        font-weight: bold;
        font-size: 16px;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        transform: scale(1.05);
        box-shadow: 0 4px 15px rgba(255, 154, 158, 0.4);
    }
    h1 {
        text-align: center;
        color: #ff6b9d;
        font-size: 40px;
    }
</style>
""", unsafe_allow_html=True)

# 세션 상태 초기화
if "page" not in st.session_state:
    st.session_state.page = "intro"
if "answers" not in st.session_state:
    st.session_state.answers = {}
if "current_q" not in st.session_state:
    st.session_state.current_q = 0

# 10문항 MBTI 질문
questions = [
    {
        "q": "1️⃣ 주말에 친구가 갑자기 놀자고 한다면?",
        "a1": "🎉 좋아! 당장 나가자!", "a1_type": "E",
        "a2": "🏠 음... 집에서 쉬는게 더 좋아", "a2_type": "I"
    },
    {
        "q": "2️⃣ 새로운 모임에 갔을 때 나는?",
        "a1": "💬 먼저 다가가서 말을 건다", "a1_type": "E",
        "a2": "👀 조용히 분위기를 살핀다", "a2_type": "I"
    },
    {
        "q": "3️⃣ 여행 갈 때 나는?",
        "a1": "📋 계획표를 꼼꼼하게 짠다", "a1_type": "S",
        "a2": "✨ 상상의 나래를 펼친다", "a2_type": "N"
    },
    {
        "q": "4️⃣ 공부할 때 나는?",
        "a1": "📚 사실과 디테일을 외운다", "a1_type": "S",
        "a2": "💡 큰 그림과 원리를 이해한다", "a2_type": "N"
    },
    {
        "q": "5️⃣ 영화를 볼 때 나는?",
        "a1": "🎬 현실적인 스토리가 좋다", "a1_type": "S",
        "a2": "🦄 판타지/SF가 좋다", "a2_type": "N"
    },
    {
        "q": "6️⃣ 친구가 고민을 털어놓을 때?",
        "a1": "🔍 해결 방법을 분석해준다", "a1_type": "T",
        "a2": "🤗 공감하고 위로해준다", "a2_type": "F"
    },
    {
        "q": "7️⃣ 결정을 내릴 때 나는?",
        "a1": "⚖️ 논리적으로 판단한다", "a1_type": "T",
        "a2": "💖 마음이 가는대로 한다", "a2_type": "F"
    },
    {
        "q": "8️⃣ 칭찬과 비판 중 더 신경 쓰이는 건?",
        "a1": "📊 비판 (개선점이 중요)", "a1_type": "T",
        "a2": "🌸 칭찬 (감정이 중요)", "a2_type": "F"
    },
    {
        "q": "9️⃣ 방학이 시작되면 나는?",
        "a1": "📅 계획표부터 만든다", "a1_type": "J",
        "a2": "🌊 일단 흘러가는대로 본다", "a2_type": "P"
    },
    {
        "q": "🔟 과제가 주어지면 나는?",
        "a1": "✅ 미리미리 끝낸다", "a1_type": "J",
        "a2": "🔥 마감 직전에 몰아서 한다", "a2_type": "P"
    }
]

# MBTI별 포켓몬 데이터
mbti_pokemon = {
    "INTJ": {
        "name": "뮤츠", "emoji": "🔮", "type": "사이코", "id": 150,
        "desc": "전략가이자 천재! 강력한 정신력으로 모든 걸 계획하는 너에게 딱! 🧠✨",
        "personality": "차갑지만 깊이 있는 지적인 매력의 소유자"
    },
    "INTP": {
        "name": "메타몽", "emoji": "🟣", "type": "노말", "id": 132,
        "desc": "무엇이든 될 수 있는 변신의 귀재! 호기심 많은 너처럼 다재다능해! 🌈",
        "personality": "유연한 사고와 무한한 가능성의 소유자"
    },
    "ENTJ": {
        "name": "리자몽", "emoji": "🔥", "type": "불꽃/비행", "id": 6,
        "desc": "타고난 리더! 카리스마 넘치는 불꽃의 지배자야! 👑🔥",
        "personality": "당당하고 강력한 카리스마의 소유자"
    },
    "ENTP": {
        "name": "피카츄", "emoji": "⚡", "type": "전기", "id": 25,
        "desc": "번뜩이는 아이디어! 활발하고 재치있는 너의 매력 그 자체! ⚡💛",
        "personality": "재치있고 에너지 넘치는 분위기 메이커"
    },
    "INFJ": {
        "name": "뮤", "emoji": "🌸", "type": "사이코", "id": 151,
        "desc": "신비롭고 따뜻한 마음! 모든 포켓몬의 시작이자 특별한 존재야! 💖",
        "personality": "신비롭고 통찰력 있는 이상주의자"
    },
    "INFP": {
        "name": "이브이", "emoji": "🦊", "type": "노말", "id": 133,
        "desc": "무한한 가능성을 품은 순수한 영혼! 너만의 색깔로 진화할 거야! 🌟",
        "personality": "꿈 많고 감수성 풍부한 자유로운 영혼"
    },
    "ENFJ": {
        "name": "샤미드", "emoji": "💧", "type": "물", "id": 134,
        "desc": "따뜻한 카리스마! 사람들을 이끄는 우아한 리더야! 🌊✨",
        "personality": "따뜻하고 영감을 주는 멘토"
    },
    "ENFP": {
        "name": "잠만보", "emoji": "🌙", "type": "노말", "id": 143,
        "desc": "낙천적이고 사랑스러운 존재! 자유로운 영혼의 너와 닮았어! 💕",
        "personality": "긍정 에너지 가득한 자유로운 영혼"
    },
    "ISTJ": {
        "name": "꼬부기", "emoji": "🐢", "type": "물", "id": 7,
        "desc": "성실하고 든든한 너! 단단한 등껍질처럼 믿음직스러워! 🛡️",
        "personality": "책임감 강하고 신뢰할 수 있는 든든이"
    },
    "ISFJ": {
        "name": "이상해씨", "emoji": "🌱", "type": "풀/독", "id": 1,
        "desc": "따뜻하고 헌신적인 너! 모두를 챙기는 다정한 마음! 🌿💚",
        "personality": "다정하고 헌신적인 보호자"
    },
    "ESTJ": {
        "name": "근육몬", "emoji": "💪", "type": "격투", "id": 67,
        "desc": "강력한 추진력! 목표를 향해 거침없이 나아가는 리더! 🏆",
        "personality": "체계적이고 결단력 있는 실행가"
    },
    "ESFJ": {
        "name": "푸린", "emoji": "🎤", "type": "노말/페어리", "id": 39,
        "desc": "사랑스럽고 사교적인 너! 모두를 행복하게 하는 매력쟁이! 🎵💖",
        "personality": "사랑스럽고 사교적인 분위기 메이커"
    },
    "ISTP": {
        "name": "고라파덕", "emoji": "🦆", "type": "물", "id": 54,
        "desc": "조용하지만 알고보면 천재! 위기에서 빛나는 해결사! 🧩",
        "personality": "쿨하고 실용적인 문제 해결사"
    },
    "ISFP": {
        "name": "님피아", "emoji": "🎨", "type": "페어리", "id": 700,
        "desc": "예술적 감성의 소유자! 부드럽고 아름다운 영혼이야! 🌸✨",
        "personality": "예술적이고 감성적인 자유 영혼"
    },
    "ESTP": {
        "name": "파이리", "emoji": "🔥", "type": "불꽃", "id": 4,
        "desc": "에너지 넘치는 모험가! 도전을 즐기는 열정의 화신! 🔥⚡",
        "personality": "활동적이고 모험을 즐기는 행동파"
    },
    "ESFP": {
        "name": "이상해꽃", "emoji": "🌺", "type": "풀/독", "id": 3,
        "desc": "화려하고 사랑스러운 너! 어디서든 빛나는 스타! 🌟🎉",
        "personality": "활발하고 매력 넘치는 인기쟁이"
    }
}

# 상호작용 메시지
interactions = {
    "쓰다듬기 🤚": [
        "기분 좋아 보여요! 골골골~ 😊",
        "행복해하며 비비적거려요! 💕",
        "꼬리를 살랑살랑 흔들어요! ✨",
        "눈을 게슴츠레 뜨고 좋아해요! 😴"
    ],
    "먹이주기 🍎": [
        "냠냠! 맛있게 먹어요! 🍴",
        "와앙! 더 달라고 졸라요! 😋",
        "포만감에 행복한 표정이에요! 🥰",
        "맛있다며 점프해요! 🎵"
    ],
    "놀아주기 🎾": [
        "신나게 뛰어다녀요! 🏃‍♂️💨",
        "공을 물고 자랑해요! 🎾✨",
        "흥분해서 기술을 보여줘요! ⚡",
        "재미있다며 깡총깡총! 🌟"
    ],
    "대화하기 💬": [
        "고개를 갸웃거리며 듣고 있어요! 🤔",
        "친근하게 울음소리를 내요! 🎵",
        "당신의 말을 이해한 것 같아요! 💖",
        "행복한 표정으로 바라봐요! 😍"
    ],
    "배틀신청 ⚔️": [
        "전투 자세를 취해요! 💪🔥",
        "기술을 시전할 준비 완료! ⚡",
        "눈빛이 반짝거려요! ✨😤",
        "용감하게 포효해요! 🦁"
    ]
}

# MBTI 계산 함수
def calculate_mbti(answers):
    counts = {"E": 0, "I": 0, "S": 0, "N": 0, "T": 0, "F": 0, "J": 0, "P": 0}
    for ans in answers.values():
        counts[ans] += 1
    
    mbti = ""
    mbti += "E" if counts["E"] >= counts["I"] else "I"
    mbti += "S" if counts["S"] >= counts["N"] else "N"
    mbti += "T" if counts["T"] >= counts["F"] else "F"
    mbti += "J" if counts["J"] >= counts["P"] else "P"
    return mbti

# ===== 메인 타이틀 =====
st.markdown("# ⚡ MBTI 포켓몬 테스트 🌟")

# 제작자 배지
st.markdown("""
<div style='text-align: center; margin: 10px 0;'>
    <span style='background: linear-gradient(90deg, #ff9a9e 0%, #fad0c4 50%, #a8edea 100%); 
                 padding: 8px 20px; border-radius: 30px; color: white; 
                 font-weight: bold; font-size: 16px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);'>
        🦈 Created by 이유리 💕
    </span>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ===== 사이드바 =====
with st.sidebar:
    st.markdown("## 🌈 사용 방법")
    st.info("""
    1️⃣ 10개의 질문에 답해주세요  
    2️⃣ 당신의 MBTI가 분석돼요  
    3️⃣ 어울리는 포켓몬을 만나요!  
    4️⃣ 포켓몬과 놀아보세요 🎮
    """)
    
    if st.button("🔄 처음부터 다시 하기"):
        st.session_state.page = "intro"
        st.session_state.answers = {}
        st.session_state.current_q = 0
        st.rerun()
    
    st.markdown("---")
    st.markdown("### 🦈 제작자")
    st.markdown("""
    <div style='background: linear-gradient(135deg, #fbc2eb 0%, #a6c1ee 100%); 
                padding: 15px; border-radius: 15px; text-align: center;'>
        <h3 style='color: white; margin: 0;'>✨ 이유리 ✨</h3>
        <p style='color: white; margin: 5px 0 0 0;'>🦈 with love 💕</p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("<div style='text-align:center; font-size:50px; margin-top:15px;'>🦈💙🦈</div>", unsafe_allow_html=True)

# ===== 인트로 페이지 =====
if st.session_state.page == "intro":
    st.markdown("### 🎀 당신의 성격에 딱 맞는 포켓몬 친구를 찾아드려요! 🎀")
    st.markdown("")
    st.markdown("""
    <div style='background: linear-gradient(135deg, #fff5f7 0%, #e0f7ff 100%); 
                padding: 25px; border-radius: 20px; text-align: center;'>
        <h2 style='color: #ff6b9d;'>🌟 어떤 포켓몬이 나올까요? 🌟</h2>
        <p style='font-size: 18px; color: #555;'>
            10개의 간단한 질문에 답하고<br>
            당신만의 포켓몬 친구를 만나보세요! 💕
        </p>
        <p style='font-size: 30px;'>⚡🔥💧🌱🌟</p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("")
    
    if st.button("✨ 테스트 시작하기! ✨", use_container_width=True):
        st.session_state.page = "test"
        st.session_state.current_q = 0
        st.session_state.answers = {}
        st.rerun()

# ===== 테스트 페이지 =====
elif st.session_state.page == "test":
    q_idx = st.session_state.current_q
    total = len(questions)
    
    # 진행률 표시
    progress = (q_idx) / total
    st.progress(progress)
    st.markdown(f"### 📝 진행도: {q_idx}/{total}")
    st.markdown("")
    
    if q_idx < total:
        q = questions[q_idx]
        
        st.markdown(f"""
        <div style='background: white; padding: 25px; border-radius: 20px; 
                    box-shadow: 0 4px 15px rgba(0,0,0,0.1); text-align: center;'>
            <h2 style='color: #ff6b9d;'>{q['q']}</h2>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button(q["a1"], key=f"a1_{q_idx}", use_container_width=True):
                st.session_state.answers[q_idx] = q["a1_type"]
                st.session_state.current_q += 1
                st.rerun()
        with col2:
            if st.button(q["a2"], key=f"a2_{q_idx}", use_container_width=True):
                st.session_state.answers[q_idx] = q["a2_type"]
                st.session_state.current_q += 1
                st.rerun()
    else:
        # 모든 질문 완료 → 결과 페이지로
        st.session_state.page = "result"
        st.rerun()

# ===== 결과 페이지 =====
elif st.session_state.page == "result":
    mbti = calculate_mbti(st.session_state.answers)
    pokemon = mbti_pokemon[mbti]
    
    st.balloons()
    
    st.markdown(f"""
    <div style='background: linear-gradient(135deg, #ffeef8 0%, #e0f7ff 100%); 
                padding: 20px; border-radius: 20px; text-align: center;'>
        <h2 style='color: #ff6b9d;'>🎉 테스트 완료! 🎉</h2>
        <h1 style='color: #ff6b9d; font-size: 50px;'>당신의 MBTI: {mbti}</h1>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown(f"## {pokemon['emoji']} 당신의 포켓몬 친구는... **{pokemon['name']}**! {pokemon['emoji']}")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        img_url = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/{pokemon['id']}.png"
        st.image(img_url, use_container_width=True)
    
    with col2:
        st.markdown(f"### 🏷️ 타입: `{pokemon['type']}`")
        st.markdown(f"### 💌 메시지")
        st.info(pokemon['desc'])
        st.markdown(f"### ✨ 성격")
        st.success(pokemon['personality'])
    
    st.markdown("---")
    st.markdown(f"## 🎮 {pokemon['name']}와(과) 놀아주기!")
    st.markdown("아래 버튼을 눌러 포켓몬과 상호작용해보세요! 💕")
    
    cols = st.columns(5)
    actions = list(interactions.keys())
    
    for i, action in enumerate(actions):
        with cols[i]:
            if st.button(action, key=f"action_{i}", use_container_width=True):
                response = random.choice(interactions[action])
                st.session_state.last_response = response
                st.session_state.action_count = st.session_state.get("action_count", 0) + 1
    
    if st.session_state.get("last_response"):
        st.markdown("### 💬 포켓몬의 반응")
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, #fff5f7 0%, #fef0e0 100%); 
                    padding: 20px; border-radius: 15px; border-left: 5px solid #ff9a9e;'>
            <h3>{pokemon['emoji']} {pokemon['name']}: {st.session_state.last_response}</h3>
        </div>
        """, unsafe_allow_html=True)
    
    # 친밀도 게이지
    st.markdown("### 💖 친밀도")
    affection = min(100, st.session_state.get("action_count", 0) * 20 + 20)
    st.progress(affection / 100)
    st.caption(f"친밀도: {affection}% - 점점 더 친해지고 있어요! 🥰")
    
    st.markdown("---")
    if st.button("🔄 다시 테스트하기", use_container_width=True):
        st.session_state.page = "intro"
        st.session_state.answers = {}
        st.session_state.current_q = 0
        st.session_state.last_response = None
        st.session_state.action_count = 0
        st.rerun()

# ===== 푸터 =====
st.markdown("---")
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown("""
    <div style='background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%); 
                padding: 20px; border-radius: 20px; text-align: center;
                box-shadow: 0 4px 15px rgba(0,0,0,0.1);'>
        <h2 style='color: #ff6b9d; margin: 0;'>🦈✨ Made by 이유리 ✨🦈</h2>
        <p style='color: #555; margin-top: 10px; font-size: 16px;'>
            💕 귀여운 포켓몬 친구들과 함께해요! 💕
        </p>
        <p style='font-size: 40px; margin: 10px 0;'>🦈💙🦈💙🦈</p>
    </div>
    """, unsafe_allow_html=True)
