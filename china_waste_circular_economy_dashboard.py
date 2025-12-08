"""
중국 폐기물 처리 및 순환경제 시장 분석 대시보드
China Waste Management & Circular Economy Market Dashboard
Version 1.0
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ============================================================
# 페이지 설정
# ============================================================
st.set_page_config(
    page_title="중국 폐기물/순환경제 시장 분석",
    page_icon="🇨🇳",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# CSS 스타일 (색상/가독성 개선 버전)
# ============================================================
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #D32F2F;
        text-align: center;
        padding: 1rem;
        background: linear-gradient(90deg, #FFEBEE 0%, #FFCDD2 100%);
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    /* 요약 카드: 노랑 톤 + 진한 글자 */
    .metric-card {
        background: linear-gradient(135deg, #FFF3E0 0%, #FFE0B2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #FB8C00;
        margin: 0.5rem 0;
        color: #3E2723;
    }
    .metric-card h4 {
        color: #E65100;
        margin-top: 0;
    }
    /* 출처 박스: 파랑 톤 + 진한 글자 */
    .source-box {
        background-color: #E3F2FD;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #1976D2;
        font-size: 0.85rem;
        margin-top: 1rem;
        color: #0D47A1;
    }
    /* 초록 하이라이트 박스 (도시 카드, 순환경제 목표 등) */
    .highlight-box {
        background: linear-gradient(135deg, #DCEDC8 0%, #C5E1A5 100%);
        padding: 1.2rem;
        border-radius: 10px;
        border: 2px solid #558B2F;
        margin: 1rem 0;
        color: #1B5E20;
    }
    .highlight-box h4 {
        color: #33691E;
        margin-top: 0;
    }
    /* 경고/이슈 박스: 주황 톤 + 진한 글자 */
    .warning-box {
        background-color: #FFECB3;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #F57C00;
        margin: 0.5rem 0;
        color: #4E342E;
    }
    .warning-box h4 {
        color: #E65100;
        margin-top: 0;
    }
    /* 기술 카드: 보라 톤 + 진한 글자 */
    .tech-card {
        background: linear-gradient(135deg, #EDE7F6 0%, #D1C4E9 100%);
        padding: 1.2rem;
        border-radius: 10px;
        border-left: 5px solid #6A1B9A;
        margin: 0.5rem 0;
        color: #311B92;
    }
    .tech-card h4 {
        color: #4A148C;
        margin-top: 0;
    }
    /* 기업 카드: 청록 톤 + 진한 글자 */
    .company-card {
        background: linear-gradient(135deg, #E0F7FA 0%, #B2EBF2 100%);
        padding: 1rem;
        border-radius: 8px;
        margin: 0.3rem 0;
        color: #004D40;
        border-left: 4px solid #00838F;
    }
    .company-card h4 {
        color: #00695C;
        margin-top: 0;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================
# 헤더
# ============================================================
st.markdown('<div class="main-header">🇨🇳 중국 폐기물 처리 & 순환경제 시장 분석</div>', unsafe_allow_html=True)
st.markdown("##### China Waste Management & Circular Economy Market Dashboard")

# ============================================================
# 사이드바
# ============================================================
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/f/fa/Flag_of_the_People%27s_Republic_of_China.svg/200px-Flag_of_the_People%27s_Republic_of_China.svg.png", width=100)
    st.markdown("### 📊 데이터 개요")
    st.info("""
    **분석 기준**: 2024년 12월
    
    **핵심 지표:**
    - 폐기물 시장: $781억 (2024)
    - WtE 시설: 1,010개
    - 순환경제 목표: 5조 위안
    - 소각 비율: 72.5%
    """)
    
    st.markdown("---")
    st.markdown("### 🎯 14차 5개년 계획 목표")
    st.success("""
    **2025년 목표:**
    - 자원순환산업: 5조 위안
    - 재생 비철금속: 2,000만 톤
    - 자원 생산성: 20% 향상
    """)
    
    st.markdown("---")
    st.markdown("### 📈 시장 성장률")
    st.metric("폐기물 관리 CAGR", "5.25%", "2025-2030")
    st.metric("순환경제 CAGR", "11.8%", "2024-2029")

# ============================================================
# 탭 구성
# ============================================================
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📊 시장 규모", 
    "🏭 폐기물 현황", 
    "🔥 WtE 기술", 
    "♻️ 순환경제",
    "🏢 주요 기업",
    "📚 출처"
])

# ============================================================
# 탭1: 시장 규모
# ============================================================
with tab1:
    st.markdown("## 📊 중국 폐기물 관리 시장 규모")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("2024년 시장 규모", "$781.6억", "기준연도")
    with col2:
        st.metric("2025년 예상", "$824.9억", "+5.5%")
    with col3:
        st.metric("2030년 전망", "$1,065.5억", "+36.3%")
    with col4:
        st.metric("CAGR (25-30)", "5.25%", "연평균 성장률")
    
    st.markdown("---")
    
    # 시장 규모 추이 차트
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📈 폐기물 관리 시장 규모 전망 (USD)")
        market_data = pd.DataFrame({
            '연도': [2019, 2020, 2021, 2022, 2023, 2024, 2025, 2026, 2027, 2028, 2029, 2030],
            '시장규모(십억달러)': [55.2, 58.5, 62.3, 67.8, 74.2, 78.16, 82.49, 86.82, 91.38, 96.18, 101.23, 106.55]
        })
        
        fig1 = px.area(market_data, x='연도', y='시장규모(십억달러)',
                      title='중국 폐기물 관리 시장 규모 추이 및 전망',
                      color_discrete_sequence=['#D32F2F'])
        fig1.add_vline(x=2024, line_dash="dash", line_color="gray", 
                      annotation_text="현재(2024)")
        fig1.update_layout(height=400)
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        st.markdown("### 🥧 환경보호산업 분야별 시장 (2020년 기준)")
        sector_data = pd.DataFrame({
            '분야': ['폐기물 처리', '오수처리', '대기오염 방지', '토양오염 정화'],
            '시장규모(억위안)': [8030, 5820, 3094, 114]
        })
        
        fig2 = px.pie(sector_data, values='시장규모(억위안)', names='분야',
                     title='중국 환경보호산업 분야별 비중',
                     color_discrete_sequence=px.colors.sequential.Reds_r)
        fig2.update_traces(textposition='inside', textinfo='percent+label')
        fig2.update_layout(height=400)
        st.plotly_chart(fig2, use_container_width=True)
    
    st.markdown("---")
    
    # 분야별 시장 규모 상세
    st.markdown("### 💰 분야별 시장 규모 및 전망")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
        <h4>🗑️ 폐기물 처리 시장</h4>
        <table style="width:100%">
            <tr><td><b>2020년</b></td><td>8,030억 위안</td></tr>
            <tr><td><b>2025년 전망</b></td><td>1.3조 위안</td></tr>
            <tr><td><b>성장률</b></td><td>연간 4% 이상</td></tr>
            <tr><td><b>고형폐기물 처리량</b></td><td>105.5억 톤 (2021)</td></tr>
        </table>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="metric-card">
        <h4>💧 오수처리 시장</h4>
        <table style="width:100%">
            <tr><td><b>2020년</b></td><td>5,245억 위안</td></tr>
            <tr><td><b>2023년</b></td><td>5,820억 위안</td></tr>
            <tr><td><b>CAGR (2019-2023)</b></td><td>14.7%</td></tr>
        </table>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
        <h4>🌫️ 대기오염 방지 시장</h4>
        <table style="width:100%">
            <tr><td><b>2016년</b></td><td>1,575억 위안</td></tr>
            <tr><td><b>2020년</b></td><td>3,094억 위안</td></tr>
            <tr><td><b>2025년 전망</b></td><td>3,300억 위안</td></tr>
            <tr><td><b>CAGR (2016-2020)</b></td><td>18.4%</td></tr>
        </table>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="metric-card">
        <h4>🌱 환경보호산업 전체</h4>
        <table style="width:100%">
            <tr><td><b>2027년 전망</b></td><td>4.4조 위안</td></tr>
            <tr><td><b>연평균성장률</b></td><td>12%</td></tr>
            <tr><td><b>정부 목표</b></td><td>쌍탄(双碳) 달성</td></tr>
        </table>
        </div>
        """, unsafe_allow_html=True)
    
    with st.expander("📚 데이터 출처 보기"):
        st.markdown("""
        | 지표 | 출처 | 신뢰도 |
        |------|------|--------|
        | 폐기물 관리 시장 규모 | Mordor Intelligence (2024) | ✅ 검증됨 |
        | 환경보호산업 분야별 규모 | KOTRA 중국무역관 | ✅ 검증됨 |
        | 고형폐기물 처리량 | 중국 국가통계국 | ✅ 공식통계 |
        | 2027년 전망 | 中国环保产业协会 | ✅ 검증됨 |
        """)

# ============================================================
# 탭2: 폐기물 현황
# ============================================================
with tab2:
    st.markdown("## 🏭 중국 폐기물 발생 및 처리 현황")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("2023년 도시폐기물", "2.54억 톤", "+8.1% vs 2020")
    with col2:
        st.metric("소각 비율", "72.5%", "2021년 기준")
    with col3:
        st.metric("소각 시설 수", "927개", "2023년")
    with col4:
        st.metric("무해화 처리율", "99%+", "도시 기준")
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📈 도시 생활폐기물 발생량 추이")
        waste_gen = pd.DataFrame({
            '연도': [2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023],
            '발생량(백만톤)': [191, 204, 215, 228, 242, 235, 249, 247, 254]
        })
        
        fig3 = px.bar(waste_gen, x='연도', y='발생량(백만톤)',
                     title='중국 도시 생활폐기물 발생량',
                     color='발생량(백만톤)',
                     color_continuous_scale='Reds')
        fig3.add_annotation(x=2020, y=235, text="COVID-19 영향",
                           showarrow=True, arrowhead=1)
        fig3.update_layout(height=400)
        st.plotly_chart(fig3, use_container_width=True)
    
    with col2:
        st.markdown("### 🔄 처리 방식 변화 추이")
        treatment = pd.DataFrame({
            '연도': [2015, 2017, 2019, 2020, 2021, 2023],
            '소각': [31, 40, 51, 56, 62, 72],
            '매립': [64, 55, 45, 40, 34, 24],
            '기타': [5, 5, 4, 4, 4, 4]
        })
        
        fig4 = go.Figure()
        fig4.add_trace(go.Scatter(x=treatment['연도'], y=treatment['소각'],
                                 name='소각', fill='tozeroy', line=dict(color='#D32F2F')))
        fig4.add_trace(go.Scatter(x=treatment['연도'], y=treatment['매립'],
                                 name='매립', fill='tozeroy', line=dict(color='#795548')))
        fig4.add_trace(go.Scatter(x=treatment['연도'], y=treatment['기타'],
                                 name='기타', fill='tozeroy', line=dict(color='#9E9E9E')))
        fig4.update_layout(title='폐기물 처리 방식 비율 변화 (%)',
                          height=400, yaxis_title='비율 (%)')
        st.plotly_chart(fig4, use_container_width=True)
    
    st.markdown("---")
    
    st.markdown("### 🗺️ 주요 도시별 폐기물 현황")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="highlight-box">
        <h4>🏙️ 선전 (Shenzhen)</h4>
        <ul>
            <li><b>일일 발생량:</b> 15,000톤</li>
            <li><b>1979년 대비:</b> 300배 증가</li>
            <li><b>인구:</b> 1,300만명</li>
            <li><b>세계 최대 WtE 건설 중</b></li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="highlight-box">
        <h4>🏙️ 시안 (Xi'an)</h4>
        <ul>
            <li><b>장춘거우 매립지:</b> 중국 최대</li>
            <li><b>설계 용량:</b> 2,500톤/일</li>
            <li><b>실제 유입:</b> 10,000톤+/일</li>
            <li><b>25년 앞당겨 포화</b></li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="highlight-box">
        <h4>🏝️ 하이난 (Hainan)</h4>
        <ul>
            <li><b>WtE 100% 달성:</b> 최초 성급 지역</li>
            <li><b>매립 의존도:</b> 0%</li>
            <li><b>전량 소각 처리</b></li>
            <li><b>환경 관리 모범 사례</b></li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("### ⚠️ 주요 이슈 및 과제")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="warning-box">
        <h4>🚨 현재 문제점</h4>
        <ul>
            <li><b>매립지 포화:</b> 대도시 매립지 용량 한계</li>
            <li><b>불법 투기:</b> 농촌 지역 불법 폐기물 투기 만연</li>
            <li><b>분리수거 미흡:</b> 2019년부터 강화 중이나 지역 편차</li>
            <li><b>WtE 과잉 용량:</b> 60% 가동률, 쓰레기 부족</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="warning-box">
        <h4>📋 정책 대응</h4>
        <ul>
            <li><b>고체폐기물법 개정:</b> 2020년 9월 시행</li>
            <li><b>폐기물 수입 전면 금지:</b> 2021년 1월부터</li>
            <li><b>쓰레기 분리수거 의무화:</b> 대도시 중심</li>
            <li><b>WtE 신규 건설 축소:</b> 재활용 강화로 전환</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with st.expander("📚 데이터 출처 보기"):
        st.markdown("""
        | 지표 | 출처 | 링크 |
        |------|------|------|
        | 도시폐기물 발생량 | 중국 국가통계국 | [Statista](https://www.statista.com/statistics/279117/amount-of-disposed-garbage-in-china/) |
        | 처리 방식 비율 | US Trade.gov China Report | [Trade.gov](https://www.trade.gov/country-commercial-guides/china-environmental-technology) |
        | 선전 현황 | Yale E360 | [Yale E360](https://e360.yale.edu/features/as-china-pushes-waste-to-energy-incinerators-protests-are-mounting) |
        | 정책 동향 | KDI 경제교육정보센터 | [KDI](https://eiec.kdi.re.kr/policy/materialView.do?num=208553) |
        """)

# ============================================================
# 탭3: WtE 기술
# ============================================================
with tab3:
    st.markdown("## 🔥 폐기물 에너지화(WtE) 기술 현황")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("WtE 시설 수", "1,010개", "2024년 10월")
    with col2:
        st.metric("세계 점유율", "50%+", "전 세계 WtE의 절반")
    with col3:
        st.metric("일일 처리 능력", "~110만 톤", "평균 750톤/시설")
    with col4:
        st.metric("평균 가동률", "60%", "용량 과잉 상태")
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📈 WtE 시설 증가 추이")
        wte_growth = pd.DataFrame({
            '연도': [2010, 2012, 2014, 2016, 2018, 2020, 2021, 2023, 2024],
            '시설수': [90, 138, 188, 231, 331, 400, 500, 927, 1010],
            '용량(백만톤/년)': [30, 45, 62, 80, 110, 150, 180, 254, 292]
        })
        
        fig5 = make_subplots(specs=[[{"secondary_y": True}]])
        fig5.add_trace(go.Bar(x=wte_growth['연도'], y=wte_growth['시설수'],
                             name='시설 수', marker_color='#D32F2F'), secondary_y=False)
        fig5.add_trace(go.Scatter(x=wte_growth['연도'], y=wte_growth['용량(백만톤/년)'],
                                 name='연간 용량', line=dict(color='#1976D2', width=3)),
                      secondary_y=True)
        fig5.update_layout(title='WtE 시설 수 및 처리 용량', height=400)
        fig5.update_yaxes(title_text="시설 수", secondary_y=False)
        fig5.update_yaxes(title_text="용량 (백만톤/년)", secondary_y=True)
        st.plotly_chart(fig5, use_container_width=True)
    
    with col2:
        st.markdown("### 🌍 주요국 WtE 용량 비교")
        global_wte = pd.DataFrame({
            '국가': ['중국', '일본', '독일', '미국', '프랑스', '한국'],
            '용량(백만톤/년)': [292, 38, 26, 25, 15, 8]
        })
        
        fig6 = px.bar(global_wte, x='국가', y='용량(백만톤/년)',
                     title='주요국 WtE 연간 처리 용량 비교',
                     color='용량(백만톤/년)',
                     color_continuous_scale='Reds')
        fig6.update_layout(height=400)
        st.plotly_chart(fig6, use_container_width=True)
    
    st.markdown("---")
    
    st.markdown("### 🏗️ 주요 WtE 프로젝트")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="tech-card">
        <h4>🏭 선전 동부 WtE (건설중)</h4>
        <ul>
            <li><b>처리 용량:</b> 5,000톤/일</li>
            <li><b>발전 용량:</b> 200MW</li>
            <li><b>특징:</b> 세계 최대 규모</li>
            <li><b>태양광:</b> 40,000㎡ 패널</li>
            <li><b>수혜 가구:</b> 300만 가구</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="tech-card">
        <h4>🏭 항저우 WtE 단지</h4>
        <ul>
            <li><b>특징:</b> 대규모 통합 시설</li>
            <li><b>초기 주민 반대 → 수용</b></li>
            <li><b>밀집 도시지역 성공 사례</b></li>
            <li><b>환경교육 연계</b></li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="tech-card">
        <h4>🏭 광저우 순환경제 산업단지</h4>
        <ul>
            <li><b>WtE + 재활용 통합</b></li>
            <li><b>퇴비화 시설 연계</b></li>
            <li><b>환경교육센터 운영</b></li>
            <li><b>순환경제 모델 사례</b></li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("### ⚙️ 기술 수준 및 O&M 현황")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="highlight-box">
        <h4>🔧 주요 기술 현황</h4>
        
        <b>소각로 유형:</b>
        <ul>
            <li>기계식 그레이트 소각로 (주류)</li>
            <li>유동층 소각로</li>
            <li>회전로 (위험폐기물)</li>
        </ul>
        
        <b>모니터링 시스템:</b>
        <ul>
            <li>CEMS (실시간 배출 모니터링)</li>
            <li>IoT 기반 스마트 운영</li>
            <li>원격 감시 및 예측 정비</li>
        </ul>
        
        <b>배출 관리:</b>
        <ul>
            <li>2004년 대비 배출량 100배 감소</li>
            <li>단, 유럽 기준 대비 10배 높음</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="highlight-box">
        <h4>📊 O&M 주요 지표</h4>
        
        <b>운영 현황:</b>
        <ul>
            <li>연간 가동 시간: 8,000시간</li>
            <li>평균 가동률: 60% (용량 과잉)</li>
            <li>발전 효율: 20-25%</li>
        </ul>
        
        <b>침출수 처리:</b>
        <ul>
            <li>시장 규모: 68.79억 위안 (2023)</li>
            <li>2030년 전망: 134.12억 위안</li>
            <li>연평균 성장률: 10%</li>
        </ul>
        
        <b>특허 출원:</b>
        <ul>
            <li>2020년: 954건 (최고치)</li>
            <li>2022년: 622건</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("### 🔬 기술 발전 동향")
    
    tech_trends = pd.DataFrame({
        '기술 분야': ['스마트 소각 시스템', 'CCUS 연계', '침출수 전량 처리', 'AI 연소 제어', '바이오매스 혼소'],
        '성숙도': [80, 40, 55, 65, 70],
        '투자 증가율': [25, 45, 30, 35, 20]
    })
    
    fig7 = go.Figure()
    fig7.add_trace(go.Bar(name='기술 성숙도 (%)', x=tech_trends['기술 분야'], 
                         y=tech_trends['성숙도'], marker_color='#D32F2F'))
    fig7.add_trace(go.Bar(name='투자 증가율 (%)', x=tech_trends['기술 분야'], 
                         y=tech_trends['투자 증가율'], marker_color='#1976D2'))
    fig7.update_layout(barmode='group', title='WtE 기술 분야별 성숙도 및 투자 동향',
                      height=400)
    st.plotly_chart(fig7, use_container_width=True)
    
    with st.expander("📚 데이터 출처 보기"):
        st.markdown("""
        | 지표 | 출처 | 링크 |
        |------|------|------|
        | WtE 시설 수 (1,010개) | Catalyst Planet | [링크](https://www.catalystplanet.com/travel-and-social-action-stories/chinas-waste-revolution-turning-garbage-into-energy) |
        | WtE 시설 상세 (997개, 2024.1) | ScienceDirect | [링크](https://www.sciencedirect.com/science/article/abs/pii/S0306261924025327) |
        | 선전 프로젝트 | World Economic Forum | [링크](https://www.weforum.org/stories/2019/07/one-of-china-s-biggest-megacities-is-building-a-giant-waste-to-energy-plant/) |
        | 침출수 시장 | KOTRA 샤먼무역관 | [KOTRA](https://dream.kotra.or.kr) |
        """)

# ============================================================
# 탭4: 순환경제
# ============================================================
with tab4:
    st.markdown("## ♻️ 중국 순환경제 시장")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("2025년 목표", "5조 위안", "자원순환산업")
    with col2:
        st.metric("재생자원 재활용량", "3.76억 톤", "2023년")
    with col3:
        st.metric("중고품 시장", "1.3조 위안+", "시엔위 플랫폼")
    with col4:
        st.metric("탄소 감축 기여", "30%+", "2025년 목표")
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📈 글로벌 순환경제 시장 전망")
        circular_market = pd.DataFrame({
            '연도': [2024, 2025, 2026, 2027, 2028, 2029],
            '시장규모(십억달러)': [463.07, 517.79, 578.85, 647.16, 723.56, 798.30]
        })
        
        fig8 = px.line(circular_market, x='연도', y='시장규모(십억달러)',
                      title='글로벌 순환경제 시장 규모 전망 (CAGR 11.8%)',
                      markers=True)
        fig8.update_traces(line=dict(color='#4CAF50', width=3))
        fig8.update_layout(height=400)
        st.plotly_chart(fig8, use_container_width=True)
    
    with col2:
        st.markdown("### 🔄 재생자원 재활용 현황 (2023년)")
        recycling_data = pd.DataFrame({
            '품목': ['폐철강', '폐지', '폐플라스틱', '폐타이어', '폐유리', '폐가전', '폐섬유', '기타'],
            '재활용량(백만톤)': [245, 58, 19, 15, 12, 10, 8, 9]
        })
        
        fig9 = px.treemap(recycling_data, path=['품목'], values='재활용량(백만톤)',
                         title='재생자원 품목별 재활용량',
                         color='재활용량(백만톤)',
                         color_continuous_scale='Greens')
        fig9.update_layout(height=400)
        st.plotly_chart(fig9, use_container_width=True)
    
    st.markdown("---")
    
    st.markdown("### 📋 14차 5개년 계획 순환경제 목표")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="highlight-box">
        <h4>🎯 핵심 수치 목표</h4>
        <table style="width:100%">
            <tr><td><b>자원 생산성</b></td><td>2020년 대비 20%↑</td></tr>
            <tr><td><b>재생 비철금속</b></td><td>2,000만 톤</td></tr>
            <tr><td><b>자원순환산업</b></td><td>5조 위안</td></tr>
            <tr><td><b>고형폐기물 활용률</b></td><td>73%</td></tr>
        </table>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="highlight-box">
        <h4>📜 주요 정책 (2024년)</h4>
        <ul>
            <li><b>폐기물 재활용 체계 구축</b> (2월, 국무원)</li>
            <li><b>순환경제 표준화 시범사업</b> (1월)</li>
            <li><b>설비 갱신 행동계획</b> (3월)</li>
            <li><b>소비재 교체 촉진</b> (3월)</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="highlight-box">
        <h4>🌱 쌍탄(双碳) 목표</h4>
        <ul>
            <li><b>2030년:</b> 탄소배출 피크</li>
            <li><b>2060년:</b> 탄소중립 달성</li>
            <li><b>순환경제 기여:</b> 탄소감축의 30%</li>
            <li><b>녹색 저탄소 산업 시스템 구축</b></li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("### 🛒 중고품 시장 성장")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="company-card">
        <h4>📱 시엔위 (闲鱼, Xianyu) - 알리바바</h4>
        <ul>
            <li><b>등록 사용자:</b> 6억명 이상</li>
            <li><b>일일 거래액:</b> 10억 위안+</li>
            <li><b>시장 가치:</b> 1.3조 위안+</li>
            <li><b>2024 Q3 재활용:</b> 9.5억 위안 (YoY +270%)</li>
        </ul>
        </div>
        
        <div class="company-card">
        <h4>📱 좐좐 (转转, Zhuanzhuan)</h4>
        <ul>
            <li><b>중고 전자제품 전문</b></li>
            <li><b>방문 수거 서비스</b></li>
            <li><b>2025년 목표:</b> 1,000개 도시</li>
            <li><b>탄소감축 기여:</b> 410만 톤+</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        secondhand_growth = pd.DataFrame({
            '연도': [2019, 2020, 2021, 2022, 2023, 2024],
            '시장규모(조위안)': [0.72, 0.85, 0.98, 1.1, 1.2, 1.35]
        })
        
        fig10 = px.bar(secondhand_growth, x='연도', y='시장규모(조위안)',
                      title='중국 중고품 시장 규모',
                      color='시장규모(조위안)',
                      color_continuous_scale='Greens')
        fig10.update_layout(height=350)
        st.plotly_chart(fig10, use_container_width=True)
    
    with st.expander("📚 데이터 출처 보기"):
        st.markdown("""
        | 지표 | 출처 | 링크 |
        |------|------|------|
        | 글로벌 순환경제 시장 | Business Research Company | [링크](https://www.giiresearch.com/report/tbrc1713558-circular-economy-global-market-report.html) |
        | 14차 5개년 계획 | IEA Policies | [링크](https://www.iea.org/policies/24989-14th-five-year-plan-on-circular-economy) |
        | 재생자원 재활용량 | 中国资源再生协会 | [Xinhua](https://english.news.cn/20250221/514d0c2d47ce434f808bba5639ef519e/c.html) |
        | 중고품 시장 | China.org.cn | [링크](http://www.china.org.cn/business/2025-04/15/content_117826204.htm) |
        | 2024년 정책 | Enviliance Asia | [링크](https://enviliance.com/regions/east-asia/cn/cn-waste/cn-circular-economy-2024) |
        """)

# ============================================================
# 탭5: 주요 기업
# ============================================================
with tab5:
    st.markdown("## 🏢 중국 폐기물 관리 주요 기업")
    
    st.markdown("### 📊 시가총액 기준 상위 기업")
    
    companies = pd.DataFrame({
        '순위': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        '기업명': [
            'Zhejiang Weiming Environment Protection',
            'Beijing Originwater Technology',
            'Qingdao Huicheng Environmental Technology',
            'Chongqing Sanfeng Environment Group',
            'Shanghai Environment Group',
            'China Resources and Environment',
            'Tianjin Capital Environmental Protection',
            'Beijing GeoEnviron Engineering',
            'Dynagreen Environmental Protection',
            'EIT Environmental Development'
        ],
        '시가총액(억달러)': [47.5, 27.0, 24.5, 18.3, 14.4, 11.4, 10.9, 10.7, 10.2, 8.8],
        '주요 사업': [
            'WtE, 환경 보호',
            '수처리, 막기술',
            '환경기술',
            'WtE, 환경 서비스',
            '도시환경 서비스',
            '자원순환',
            '환경 보호',
            '환경 엔지니어링',
            'WtE, 청정에너지',
            '환경 개발'
        ]
    })
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        fig11 = px.bar(companies.head(10), x='기업명', y='시가총액(억달러)',
                      title='중국 폐기물 관리 기업 시가총액 Top 10',
                      color='시가총액(억달러)',
                      color_continuous_scale='Reds')
        fig11.update_layout(height=450, xaxis_tickangle=-45)
        st.plotly_chart(fig11, use_container_width=True)
    
    with col2:
        st.markdown("### 💡 시장 특성")
        st.info("""
        **시장 구조:**
        - 중간 수준 집중도
        - 대기업 + 다수 지역 업체
        - 기술 장벽 높음
        
        **주요 외국 기업:**
        - Veolia (프랑스)
        - Sembcorp (싱가포르)
        - Remondis (독일)
        """)
    
    st.markdown("---")
    
    st.markdown("### 🏆 주요 기업 상세")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="company-card">
        <h4>🥇 Zhejiang Weiming</h4>
        <p><b>시가총액:</b> $47.5억</p>
        <ul>
            <li>WtE 선두기업</li>
            <li>환경보호 종합 서비스</li>
            <li>저장성 본사</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="company-card">
        <h4>🥈 Beijing Originwater</h4>
        <p><b>시가총액:</b> $27.0억</p>
        <ul>
            <li>막(Membrane) 기술 선도</li>
            <li>수처리 전문</li>
            <li>R&D 강점</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="company-card">
        <h4>🌟 China Everbright</h4>
        <p><b>유형:</b> 종합 환경기업</p>
        <ul>
            <li>WtE 시설 다수 운영</li>
            <li>홍콩 상장</li>
            <li>국제 사업 확장</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="company-card">
        <h4>🌟 Chongqing Sanfeng</h4>
        <p><b>시가총액:</b> $18.3억</p>
        <ul>
            <li>WtE 설비 제조</li>
            <li>환경 서비스</li>
            <li>충칭 본사</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="company-card">
        <h4>🔧 핵심 기술 기업</h4>
        <ul>
            <li><b>Sound Environmental:</b> 의료폐기물</li>
            <li><b>Grandblue Environment:</b> 종합환경</li>
            <li><b>Infore Environment:</b> 환경기술</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="company-card">
        <h4>🌍 글로벌 기업 (중국 진출)</h4>
        <ul>
            <li><b>Veolia (프랑스):</b> 수처리, 폐기물</li>
            <li><b>Sembcorp (싱가포르):</b> WtE</li>
            <li><b>Remondis (독일):</b> 위험폐기물</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("### 📈 매출 기준 상위 기업")
    
    revenue_companies = pd.DataFrame({
        '기업명': [
            'Beijing Capital Eco-environment',
            'Infore Environment Technology',
            'Grandblue Environment',
            'Beijing GeoEnviron Engineering',
            'Jiangsu Rainbow Heavy Industries',
            'Jiangsu Huahong Technology',
            'Shanghai Environment Group',
            'EIT Environmental Development',
            'Chongqing Sanfeng Environment',
            'Zhejiang Weiming Environment'
        ],
        '매출순위': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    })
    
    st.dataframe(revenue_companies, use_container_width=True)
    
    with st.expander("📚 데이터 출처 보기"):
        st.markdown("""
        | 지표 | 출처 | 링크 |
        |------|------|------|
        | 시가총액 순위 | Disfold | [링크](https://disfold.com/china/industry/waste-management/companies/) |
        | 매출 순위 | StockViz | [링크](https://stockviz.com/en/ranking-of-china-stocks-in-waste-management-by-revenue) |
        | 시장 분석 | Mordor Intelligence | [링크](https://www.mordorintelligence.com/industry-reports/china-waste-management-market/companies) |
        """)

# ============================================================
# 탭6: 출처
# ============================================================
with tab6:
    st.markdown("## 📚 전체 데이터 출처 및 참고자료")
    
    st.markdown("### 📊 시장 데이터 출처")
    
    st.markdown("""
    | 분류 | 데이터 | 출처 | URL |
    |------|--------|------|-----|
    | 시장규모 | 중국 폐기물 관리 시장 | Mordor Intelligence | [mordorintelligence.com](https://www.mordorintelligence.com/industry-reports/china-waste-management-market) |
    | 시장규모 | 글로벌 순환경제 시장 | Business Research Company | [giiresearch.com](https://www.giiresearch.com/report/tbrc1713558-circular-economy-global-market-report.html) |
    | 시장규모 | 중국 환경보호산업 | KOTRA | [dream.kotra.or.kr](https://dream.kotra.or.kr/kotranews/cms/news/actionKotraBoardDetail.do?pNttSn=200891) |
    | 통계 | 도시 폐기물 발생량 | Statista / 중국 국가통계국 | [statista.com](https://www.statista.com/statistics/279117/amount-of-disposed-garbage-in-china/) |
    | 통계 | 고형폐기물 현황 | Statista | [statista.com](https://www.statista.com/topics/5655/solid-waste-in-china/) |
    """)
    
    st.markdown("### 🏭 기술 및 시설 출처")
    
    st.markdown("""
    | 분류 | 데이터 | 출처 | URL |
    |------|--------|------|-----|
    | WtE | 시설 수 (1,010개) | Catalyst Planet | [catalystplanet.com](https://www.catalystplanet.com/travel-and-social-action-stories/chinas-waste-revolution-turning-garbage-into-energy) |
    | WtE | 시설 상세 데이터 | ScienceDirect | [sciencedirect.com](https://www.sciencedirect.com/science/article/abs/pii/S0306261924025327) |
    | WtE | 선전 프로젝트 | World Economic Forum | [weforum.org](https://www.weforum.org/stories/2019/07/one-of-china-s-biggest-megacities-is-building-a-giant-waste-to-energy-plant/) |
    | WtE | 시장 동향 | Ecoprog / RECYCLING Magazine | [recycling-magazine.com](https://www.recycling-magazine.com/2024/02/01/waste-to-energy-boom-takes-a-break-new-markets-on-the-horizon/) |
    | 기술 | 침출수 처리 | KOTRA 샤먼무역관 | [dream.kotra.or.kr](https://dream.kotra.or.kr/kotranews/cms/news/actionKotraBoardDetail.do?pNttSn=223643) |
    """)
    
    st.markdown("### 📜 정책 및 계획 출처")
    
    st.markdown("""
    | 분류 | 데이터 | 출처 | URL |
    |------|--------|------|-----|
    | 정책 | 14차 5개년 순환경제 계획 | IEA | [iea.org](https://www.iea.org/policies/24989-14th-five-year-plan-on-circular-economy) |
    | 정책 | 2024년 순환경제 정책 | Enviliance Asia | [enviliance.com](https://enviliance.com/regions/east-asia/cn/cn-waste/cn-circular-economy-2024) |
    | 정책 | 폐기물 수입 규제 | KDI 경제교육정보센터 | [eiec.kdi.re.kr](https://eiec.kdi.re.kr/policy/materialView.do?num=208553) |
    | 정책 | 환경기술 시장 | US Trade.gov | [trade.gov](https://www.trade.gov/country-commercial-guides/china-environmental-technology) |
    """)
    
    st.markdown("### ♻️ 순환경제 출처")
    
    st.markdown("""
    | 분류 | 데이터 | 출처 | URL |
    |------|--------|------|-----|
    | 순환경제 | 재생자원 재활용량 | Xinhua News | [english.news.cn](https://english.news.cn/20250221/514d0c2d47ce434f808bba5639ef519e/c.html) |
    | 순환경제 | 중고품 시장 | China.org.cn | [china.org.cn](http://www.china.org.cn/business/2025-04/15/content_117826204.htm) |
    | 순환경제 | 순환경제 개요 | Wikipedia | [wikipedia.org](https://en.wikipedia.org/wiki/China's_circular_economy) |
    | 순환경제 | COP29 발표 | China Daily | [chinadaily.com.cn](https://www.chinadaily.com.cn/a/202411/20/WS673d3b58a310f1265a1ce877.html) |
    """)
    
    st.markdown("### 🏢 기업 데이터 출처")
    
    st.markdown("""
    | 분류 | 데이터 | 출처 | URL |
    |------|--------|------|-----|
    | 기업 | 시가총액 순위 | Disfold | [disfold.com](https://disfold.com/china/industry/waste-management/companies/) |
    | 기업 | 매출 순위 | StockViz | [stockviz.com](https://stockviz.com/en/ranking-of-china-stocks-in-waste-management-by-revenue) |
    | 기업 | 기업 분석 | Mordor Intelligence | [mordorintelligence.com](https://www.mordorintelligence.com/industry-reports/china-waste-management-market/companies) |
    """)
    
    st.markdown("---")
    
    st.markdown("### ⚠️ 데이터 신뢰도 안내")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="highlight-box">
        <h4>✅ 검증된 데이터</h4>
        <ul>
            <li>중국 국가통계국 공식 통계</li>
            <li>IEA, WEF 등 국제기구 자료</li>
            <li>KOTRA 현지 조사 보고서</li>
            <li>상장기업 재무 데이터</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="warning-box">
        <h4>⚠️ 추정치 포함</h4>
        <ul>
            <li>시장규모 전망 (리서치 기관)</li>
            <li>CAGR 예측치</li>
            <li>일부 기술 성숙도 평가</li>
            <li>비상장 기업 데이터</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="source-box">
        <h4>📅 데이터 기준일</h4>
        <ul>
            <li><b>시장 데이터:</b> 2024년 기준</li>
            <li><b>시설 현황:</b> 2024년 10월</li>
            <li><b>정책:</b> 2024년 발표 기준</li>
            <li><b>대시보드 작성:</b> 2024년 12월</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)

# ============================================================
# 푸터
# ============================================================
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 1rem;">
    <p>📊 중국 폐기물 처리 & 순환경제 시장 분석 대시보드 v1.0</p>
    <p>데이터 기준: 2024년 12월 | 작성: Claude AI</p>
    <p>⚠️ 본 자료는 참고용이며, 투자 결정 시 추가 검증이 필요합니다.</p>
</div>
""", unsafe_allow_html=True)
