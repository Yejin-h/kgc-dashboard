import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import google.generativeai as genai
import os
from datetime import datetime

st.set_page_config(
    page_title="KGC Marketing Intelligence Dashboard",
    page_icon="🔴",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# KGC 브랜드 아이덴티티 및 디자인 토큰 적용
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;700&display=swap');
    
    :root {
        --kgc-red: #b91c1c;
        --dark-slate: #1e293b;
    }
    
    .main {
        background-color: #f1f5f9;
        font-family: 'Noto Sans KR', sans-serif;
    }
    
    /* 카드 스타일 커스텀 */
    div[data-testid="stMetric"] {
        background: white;
        padding: 1.5rem;
        border-radius: 1rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        border-left: 5px solid var(--kgc-red);
    }
    
    .kgc-header {
        background-color: var(--dark-slate);
        color: white;
        padding: 2rem;
        border-radius: 1rem;
        margin-bottom: 2rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    .ai-card {
        background: linear-gradient(135deg, #ffffff 0%, #eff6ff 100%);
        border: 1px solid #bfdbfe;
        padding: 1.5rem;
        border-radius: 1rem;
        margin-bottom: 1rem;
    }
    
    .roadmap-card {
        background: var(--dark-slate);
        color: white;
        padding: 2rem;
        border-radius: 1rem;
        margin-top: 2rem;
    }

    /* 버튼 스타일 */
    .stButton>button {
        width: 100%;
        border-radius: 0.75rem;
        font-weight: bold;
        transition: all 0.3s;
    }
    </style>
    """, unsafe_allow_html=True)

sales_data = {
    'Region': ['수도권 (CVS)', '수도권 (마트)', '지방 (CVS)', '지방 (마트)'],
    'Growth': [15, 8, 3, -2]
}
df_sales = pd.DataFrame(sales_data)

trend_data = {
    'Week': ['3월 1주', '3월 2주', '3월 3주', '3월 4주'],
    'Hiking': [120, 150, 190, 260],
    'Tennis': [80, 110, 160, 230]
}
df_trend = pd.DataFrame(trend_data)

sentiment_data = [
    {'x': 1, 'y': 5, 'text': '맛 개선(긍정)', 'size': 40, 'color': '#10b981'},
    {'x': 2, 'y': 4, 'text': '디자인(긍정)', 'size': 30, 'color': '#10b981'},
    {'x': 3, 'y': 1, 'text': '가격저항(부정)', 'size': 35, 'color': '#ef4444'},
    {'x': 4, 'y': 2, 'text': '패키징불편(부정)', 'size': 20, 'color': '#f59e0b'},
    {'x': 1.5, 'y': 4.5, 'text': '선물용 적합', 'size': 25, 'color': '#10b981'}
]
df_sentiment = pd.DataFrame(sentiment_data)

API_KEY = "" # 환경 변수에서 가져오거나 직접 입력 (예: os.getenv("GEMINI_API_KEY"))
if API_KEY:
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    model = None

st.markdown(f"""
    <div class="kgc-header">
        <div>
            <h1 style='margin:0; color:white; font-size: 2rem;'>정관장 에브리타임 밸런스 <span style='color:#f87171;'>리뉴얼 성과</span></h1>
            <p style='margin:0.5rem 0 0 0; color:#94a3b8; font-size: 1.1rem;'>2026년 3월 4주차 마케팅 전략 인텔리전스 (Streamlit v1.0)</p>
        </div>
        <div style='text-align:right;'>
            <div style='background:#b91c1c; padding:0.3rem 1rem; border-radius:1rem; font-size:0.8rem; font-weight:bold;'>INTERNAL ONLY</div>
            <p style='font-size:0.8rem; margin-top:0.5rem; color:#94a3b8;'>기준일: 2026.05.14</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("수도권 판매 성장", "+15.0%", "▲ CVS 채널 주도")
with col2:
    st.metric("지방 판매 추이", "-2.0%", "▼ 대형마트 정체", delta_color="inverse")
with col3:
    st.metric("2030 구매 비중", "45%", "Target Reached")
with col4:
    st.metric("아웃도어 키워드", "+30%", "Buzz Up")

st.write("---")

main_col, ai_col = st.columns([2, 1])

with ai_col:
    st.markdown('<div class="ai-card">', unsafe_allow_html=True)
    st.subheader("🤖 AI Strategist")
    
    if 'ai_insight' not in st.session_state:
        st.session_state.ai_insight = "데이터 분석을 시작하려면 아래 버튼을 누르세요."

    if st.button("전략 인사이트 생성", type="primary"):
        if model:
            with st.spinner("AI가 데이터를 분석 중입니다..."):
                try:
                    prompt = "2026년 3월 4주차 정관장 에브리타임 밸런스 실적: 수도권 +15%, 지방 -2%, 2030 비중 45%, 아웃도어 키워드 30% 증가. 이 데이터를 바탕으로 BM에게 줄 수 있는 전략적 조언 3줄 요약해줘."
                    response = model.generate_content(prompt)
                    st.session_state.ai_insight = response.text
                except Exception as e:
                    st.error(f"API 오류: {e}")
        else:
            st.warning("Gemini API 키가 설정되지 않았습니다.")

    st.info(st.session_state.ai_insight)
    
    st.divider()
    st.subheader("📱 SNS Copy AI")
    platform = st.selectbox("플랫폼", ["Instagram", "TikTok"])
    if st.button(f"{platform} 카피 생성"):
        if model:
            with st.spinner("카피라이팅 중..."):
                prompt = f"플랫폼: {platform}. 제품: 정관장 에브리타임 밸런스. 컨셉: Active Care (테니스/등산 후 활력). 2030 타겟의 짧고 강렬한 카피와 해시태그 3개 생성해줘."
                response = model.generate_content(prompt)
                st.success(response.text)
        else:
            st.warning("API 키가 필요합니다.")
    st.markdown('</div>', unsafe_allow_html=True)

with main_col:
    # 차트 1: 권역별 판매 실적 (Plotly Bar)
    fig_sales = px.bar(
        df_sales, 
        x='Region', 
        y='Growth',
        title="권역별 판매 실적 증감율 (%)",
        color='Growth',
        color_continuous_scale=['#f87171', '#b91c1c'],
        text_auto='.1f'
    )
    fig_sales.update_layout(
        showlegend=False, 
        plot_bgcolor='rgba(0,0,0,0)', 
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(t=50, b=20, l=0, r=0)
    )
    st.plotly_chart(fig_sales, use_container_width=True)
    
    # 차트 2: 라이프스타일 트렌드 (Plotly Area)
    fig_trend = go.Figure()
    fig_trend.add_trace(go.Scatter(
        x=df_trend['Week'], y=df_trend['Hiking'], 
        name='등산', line=dict(color='#b91c1c', width=4), 
        fill='tozeroy', mode='lines+markers'
    ))
    fig_trend.add_trace(go.Scatter(
        x=df_trend['Week'], y=df_trend['Tennis'], 
        name='테니스', line=dict(color='#3b82f6', width=4), 
        fill='tozeroy', mode='lines+markers'
    ))
    fig_trend.update_layout(
        title="Active Care 키워드 버즈량 추이", 
        plot_bgcolor='rgba(0,0,0,0)', 
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(t=50, b=20, l=0, r=0),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    st.plotly_chart(fig_trend, use_container_width=True)

st.subheader("📊 고객 리뷰 감성 클러스터 (N=500)")
fig_sentiment = px.scatter(
    df_sentiment, x='x', y='y', text='text', size='size',
    color='color', color_discrete_map='identity',
    title="고객 피드백 주요 테마 분석"
)
fig_sentiment.update_traces(textposition='top center')
fig_sentiment.update_layout(
    xaxis=dict(showgrid=False, zeroline=False, showticklabels=False, title=""),
    yaxis=dict(showgrid=False, zeroline=False, showticklabels=False, title=""),
    plot_bgcolor='#f8fafc',
    height=400
)
st.plotly_chart(fig_sentiment, use_container_width=True)

st.markdown("""
    <div class="roadmap-card">
        <h2 style='color:white; margin-bottom:1.5rem; display:flex; align-items:center; gap:10px;'>
            <span style='width:30px; height:5px; background:#3b82f6;'></span>
            전략 실행 로드맵 (Action Plan)
        </h2>
        <div style='display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 2rem;'>
            <div style='border-left: 1px solid #475569; padding-left: 1.5rem;'>
                <h4 style='color:#60a5fa; font-size:0.8rem; letter-spacing:1px;'>PHASE 01. AMPLIFY</h4>
                <p style='font-weight:bold; margin:0.5rem 0;'>아웃도어 접점 강화</p>
                <p style='font-size:0.85rem; color:#cbd5e1;'>테니스장/등산로 입구 CVS 전용 프로모션 및 매대 확장</p>
            </div>
            <div style='border-left: 1px solid #475569; padding-left: 1.5rem;'>
                <h4 style='color:#34d399; font-size:0.8rem; letter-spacing:1px;'>PHASE 02. ACTIVATE</h4>
                <p style='font-weight:bold; margin:0.5rem 0;'>지역 마트 활성화</p>
                <p style='font-size:0.85rem; color:#cbd5e1;'>지방 대형마트 시음회 재개 및 리뉴얼 체험 키트 집중 배포</p>
            </div>
            <div style='border-left: 1px solid #475569; padding-left: 1.5rem;'>
                <h4 style='color:#fbbf24; font-size:0.8rem; letter-spacing:1px;'>PHASE 03. OPTIMIZE</h4>
                <p style='font-weight:bold; margin:0.5rem 0;'>패키징 UX 개선</p>
                <p style='font-size:0.85rem; color:#cbd5e1;'>박스 지기 구조 공정 점검 및 개봉 편의성 개선 (CS 연계)</p>
            </div>
            <div style='border-left: 1px solid #475569; padding-left: 1.5rem;'>
                <h4 style='color:#f472b6; font-size:0.8rem; letter-spacing:1px;'>PHASE 04. VALUE UP</h4>
                <p style='font-weight:bold; margin:0.5rem 0;'>가격 저항선 관리</p>
                <p style='font-size:0.85rem; color:#cbd5e1;'>CVS 소포장(3포) 번들 기획 및 정기 구독 혜택 강화</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br><p style='text-align:center; color:#94a3b8; font-size:0.7rem;'>© 2026 KGC Brand Strategy Team | Confidential & Internal Use Only</p>", unsafe_allow_html=True)
