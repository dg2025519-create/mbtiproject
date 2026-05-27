import streamlit as st
import random

# 페이지 설정
st.set_page_config(
    page_title="MBTI 포켓몬 추천 ✨",
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
    .pokemon-card {
        background: white;
        border-radius: 20px;
        padding: 20px;
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# MBTI별 포켓몬 데이터 (이미지는 공식 포켓몬 API 사용)
mbti_pokemon = {
    "INTJ": {
        "name": "뮤츠", "emoji": "🔮", "type": "사이코",
        "id": 150,
        "desc": "전략가이자 천재! 강력한 정신력으로 모든 걸 계획하는 너에게 딱! 🧠✨",
        "personality": "차갑지만 깊이 있는 지적인 매력의 소유자"
    },
    "INTP": {
        "name": "메타몽", "emoji": "🟣", "type": "노말",
        "id": 132,
        "desc": "무엇이든 될 수 있는 변신의 귀재! 호기심 많은 너처럼 다재다능해! 🌈",
        "personality": "유연한 사고와 무한한 가능성의 소유자"
    },
    "ENTJ": {
        "name": "리자몽", "emoji": "🔥", "type": "불꽃/비행",
        "id": 6,
        "desc": "타고난 리더! 카리스마 넘치는 불꽃의 지배자야! 👑🔥",
        "personality": "당당하고 강력한 카리스마의 소유자"
    },
    "ENTP": {
        "name": "피카츄", "emoji": "⚡", "type": "전기",
        "id": 25,
        "desc": "번뜩이는 아이디어! 활발하고 재치있는 너의 매력 그 자체! ⚡💛",
        "personality": "재치있고 에너지 넘치는 분위기 메이커"
    },
    "INFJ": {
        "name": "뮤", "emoji": "🌸", "type": "사이코",
        "id": 151,
        "desc": "신비롭고 따뜻한 마음! 모든 포켓몬의 시작이자 특별한 존재야! 💖",
        "personality": "신비롭고 통찰력 있는 이상주의자"
    },
    "INFP": {
        "name": "이브이", "emoji": "🦊", "type": "노말",
        "id": 133,
        "desc": "무한한 가능성을 품은 순수한 영혼! 너만의 색깔로 진화할 거야! 🌟",
        "personality": "꿈 많고 감수성 풍부한 자유로운 영혼"
    },
    "ENFJ": {
        "name": "샤미드", "emoji": "💧", "type": "물",
        "id": 134,
        "desc": "따뜻한 카리스마! 사람들을 이끄는 우아한 리더야! 🌊✨",
        "personality": "따뜻하고 영감을 주는 멘토"
    },
    "ENFP": {
        "name": "잠만보", "emoji": "🌙", "type": "노말",
        "id": 143,
        "desc": "낙천적이고 사랑스러운 존재! 자유로운 영혼의 너와 닮았어! 💕",
        "personality": "긍정 에너지 가득한 자유로운 영혼"
    },
    "ISTJ": {
        "name": "꼬부기", "emoji": "🐢", "type": "물",
        "id": 7,
        "desc": "성실하고 든든한 너! 단단한 등껍질처럼 믿음직스러워! 🛡️",
        "personality": "책임감 강하고 신뢰할 수 있는 든든이"
    },
    "ISFJ": {
        "name": "이상해씨", "emoji": "🌱", "type": "풀/독",
        "id": 1,
        "desc": "따뜻하고 헌신적인 너! 모두를 챙기는 다정한 마음! 🌿💚",
        "personality": "다정하고 헌신적인 보호자"
    },
    "ESTJ": {
        "name": "근육몬", "emoji": "💪", "type": "격투",
        "id": 67,
        "desc": "강력한 추진력! 목표를 향해 거침없이 나아가는 리더! 🏆",
        "personality": "체계적이고 결단력 있는 실행가"
    },
    "ESFJ": {
        "name": "푸린", "emoji": "🎤", "type": "노말/페어리",
        "id": 39,
        "desc": "사랑스럽고 사교적인 너! 모두를 행복하게 하는 매력쟁이! 🎵💖",
        "personality": "사랑스럽고 사교적인 분위기 메이커"
    },
    "ISTP": {
        "name": "고라파덕", "emoji": "🦆", "type": "물",
        "id": 54,
        "desc": "조용하지만 알고보면 천재! 위기에서 빛나는 해결사! 🧩",
        "personality": "쿨하고 실용적인 문제 해결사"
    },
    "ISFP": {
        "name": "이브이(요정)", "emoji": "🎨", "type": "노말",
        "id": 700,
        "desc": "예술적 감성의 소유자! 부드럽고 아름다운 영혼이야! 🌸✨",
        "personality": "예술적이고 감성적인 자유 영혼"
    },
    "ESTP": {
        "name": "파이리", "emoji": "🔥", "type": "불꽃",
        "id": 4,
        "desc": "에너지 넘치는 모험가! 도전을 즐기는 열정의 화신! 🔥⚡",
        "personality": "활동적이고 모험을 즐기는 행동파"
    },
    "ESFP": {
        "name": "이상해꽃", "emoji": "🌺", "type": "풀/독",
        "id": 3,
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

# 메인 타이틀
st.markdown("# ⚡ MBTI 포켓몬 친구 찾기 🌟")
st.markdown("### 🎀 당신의 MBTI에 어울리는 포켓몬 친구를 만나보세요! 🎀")
st.markdown("---")

# 사이드바
with st.sidebar:
    st.markdown("## 🌈 사용 방법")
    st.info("""
    1️⃣ MBTI를 선택해주세요  
    2️⃣ 포켓몬 친구를 만나보세요  
    3️⃣ 상호작용 버튼으로 놀아주세요!  
    """)
    st.markdown("## 💡 MBTI란?")
    st.success("MBTI는 16가지 성격 유형 검사예요! 모르신다면 검사해보고 오세요 😊")

# MBTI 선택
col1, col2 = st.columns(2)
with col1:
    ei = st.radio("🗣️ E(외향) vs I(내향)", ["E", "I"], horizontal=True)
    sn = st.radio("👀 S(감각) vs N(직관)", ["S", "N"], horizontal=True)
with col2:
    tf = st.radio("💭 T(사고) vs F(감정)", ["T", "F"], horizontal=True)
    jp = st.radio("📅 J(판단) vs P(인식)", ["J", "P"], horizontal=True)

mbti = ei + sn + tf + jp

st.markdown(f"### 🎯 당신의 MBTI: **{mbti}**")

# 포켓몬 추천 버튼
if st.button("✨ 내 포켓몬 친구 만나기! ✨", use_container_width=True):
    st.session_state.show_pokemon = True
    st.session_state.mbti = mbti

# 포켓몬 표시
if st.session_state.get("show_pokemon", False):
    pokemon = mbti_pokemon[st.session_state.mbti]
    
    st.markdown("---")
    st.balloons()
    
    # 포켓몬 카드
    st.markdown(f"## {pokemon['emoji']} 당신의 포켓몬 친구는... **{pokemon['name']}**! {pokemon['emoji']}")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        # 포켓몬 이미지 (PokeAPI 공식 이미지)
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
    
    # 상호작용 버튼들
    cols = st.columns(5)
    actions = list(interactions.keys())
    
    for i, action in enumerate(actions):
        with cols[i]:
            if st.button(action, key=f"action_{i}", use_container_width=True):
                response = random.choice(interactions[action])
                st.session_state.last_action = action
                st.session_state.last_response = response
    
    # 상호작용 결과 표시
    if st.session_state.get("last_response"):
        st.markdown("### 💬 포켓몬의 반응")
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, #fff5f7 0%, #fef0e0 100%); 
                    padding: 20px; border-radius: 15px; border-left: 5px solid #ff9a9e;'>
            <h3>{pokemon['emoji']} {pokemon['name']}: {st.session_state.last_response}</h3>
        </div>
        """, unsafe_allow_html=True)
    
    # 친밀도 게이지 (재미 요소)
    st.markdown("### 💖 친밀도")
    affection = min(100, len([k for k in st.session_state.keys() if k.startswith("action_")]) * 20 + 20)
    st.progress(affection / 100)
    st.caption(f"친밀도: {affection}% - 점점 더 친해지고 있어요! 🥰")

# 푸터
st.markdown("---")
st.markdown("<center>🌟 Made with 💖 by 당곡고 AI 도우미 🌟</center>", unsafe_allow_html=True)
