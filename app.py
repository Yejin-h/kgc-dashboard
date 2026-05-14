import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_gsheets import GSheetsConnection
from datetime import datetime

# ==========================================================
# 1. 여기에 본인의 구글 스프레드시트 주소를 입력하세요!
# ==========================================================
SHEET_URL = "https://docs.google.com/spreadsheets/d/1ZtaUpB-KgtOMnEwqIKzjh5Jc7ln-HkFOwKZho4o_Z7g/edit#gid=0"
# ==========================================================

# 페이지 기본 설정
st.set_page_config(
    page_title="KGC 마케팅 전략 대시보드",
    page_icon="🔴",
    layout="wide"
)

# KGC 브랜드 스타일 적용 (CSS)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;700&display=swap');
    :root { --kgc-red: #b91c1c; --dark-slate: #1e293b; }
    .main { background-color: #f1f5f9; font-family: 'Noto Sans KR', sans-serif; }
    .kgc-header {
        background-color: var(--dark-slate);
        color: white;
        padding: 2rem;
        border-radius: 1rem;
        margin-bottom: 2rem;
    }
    .insight-box {
        background-color: white;
        padding: 1.5rem;
        border-radius: 0.75rem;
        border-left: 6px solid var(--kgc-red);
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);
        margin-bottom: 2rem;
    }
    </style>
    """, unsafe_allow_html=True)

# 구글 스프레드시트 연결 객체 생성
conn = st.connection("gsheets", type=GSheetsConnection)

@st.cache_data(ttl=600) # 10분 캐싱
def load_data(url):
    # 각 시트의 데이터를 SHEET_URL을 직접 참조하여 읽어옵니다.
    kpi_df = conn.read(spreadsheet=url, worksheet="KPI", nrows=4)
    full_kpi = conn.read(spreadsheet=url, worksheet="KPI")
    summary = full_kpi.iloc[5, 0] if len(full_kpi) > 5 else "데이터 분석 중..."
    
    region_df = conn.read(spreadsheet=url, worksheet="지역")
    age_df = conn.read(spreadsheet=url, worksheet="연령")
    
    return kpi_df, summary, region_df, age_df

try:
    # 데이터 불러오기 실행
    df_kpi, summary_text, df_region, df_age = load_data(SHEET_URL)

    # [상단 헤더]
    st.markdown(f"""
        <div class="kgc-header">
            <h1 style='margin:0; font-size: 2.2rem;'>정관장 에브리타임 밸런스 <span style='color:#f87171;'>전략 리포트</span></h1>
            <p style='margin:0.5rem 0 0 0; color:#94a3b8;'>기준일: {datetime.now().strftime('%Y.%m.%d')} (실시간 연동 모드)</p>
        </div>
        """, unsafe_allow_html=True)

    # [전략 인사이트 박스] - KPI 시트의 7행 데이터
    st.markdown(f"""
        <div class="insight-box">
            <h4 style='margin-top:0; color:#1e293b;'>📢 Weekly Strategic Insight</h4>
            <p style='margin:0; color:#334155; font-size: 1.1rem; line-height: 1.6;'>{summary_text}</p>
        </div>
        """, unsafe_allow_html=True)

    # [KPI 지표 레이아웃]
    cols = st.columns(4)
    for i, row in df_kpi.iterrows():
        if i < 4:
            with cols[i]:
                val = row['value']
                display_val = f"{val*100:.1f}%" if isinstance(val, float) and val <= 1 else f"{val}"
                st.metric(label=row['label'], value=display_val, delta=row['delta'])

    st.write("---")

    # [하단 차트 섹션]
    col_left, col_right = st.columns(2)

    with col_left:
        st.subheader("📍 지역별 성장률 (편의점 vs 마트)")
        fig_region = px.bar(
            df_region, x='지역', y='성장률', text_auto=True,
            color='성장률', color_continuous_scale=['#fca5a5', '#b91c1c']
        )
        fig_region.update_layout(plot_bgcolor='rgba(0,0,0,0)', yaxis_title="성장률 (%)", xaxis_title=None)
        st.plotly_chart(fig_region, use_container_width=True)

    with col_right:
        st.subheader("👥 구매 연령대별 비중")
        fig_age = px.pie(
            df_age, names='연령대', values='비중', hole=0.4,
            color_discrete_sequence=['#b91c1c', '#334155', '#94a3b8']
        )
        fig_age.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig_age, use_container_width=True)

except Exception as e:
    st.error(f"데이터 연동 중 오류가 발생했습니다.")
    st.write(f"상세 에러: {e}")
    st.info("💡 해결 방법: 코드 상단의 SHEET_URL이 정확한지, 구글 시트 공유 설정이 '링크가 있는 모든 사용자(뷰어)'인지 확인해 주세요.")

st.markdown("<br><p style='text-align:center; color:#94a3b8; font-size:0.75rem;'>본 리포트는 구글 스프레드시트 데이터를 실시간으로 반영합니다.</p>", unsafe_allow_html=True)
```eof

### 🛠 수정 방법 (필독)

1.  **URL 변경**: 위 코드의 **11행**에 있는 `SHEET_URL = "..."` 부분의 따옴표 안에 본인의 구글 스프레드시트 전체 주소를 복사해서 넣어주세요.
2.  **구글 시트 설정**:
    *   구글 시트 오른쪽 위 **[공유]** 버튼 클릭
    *   '일반 액세스'를 **[링크가 있는 모든 사용자]**로 변경
    *   권한은 **[뷰어]**로 유지
3.  **저장 및 업데이트**: 수정된 `app.py`를 깃허브에 올리면 즉시 반영됩니다.

**중요:** `conn.read()` 함수 안에 `spreadsheet=url` 매개변수를 직접 전달하도록 수정했으므로, 이제 별도의 Secrets 설정 없이도 이 URL을 통해 데이터를 가져오게 됩니다.
