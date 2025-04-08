import streamlit as st
from datetime import datetime

# クォーター期間データ
QUARTERS = {
    "1Q": {
        "授業期間": ("2025-04-14", "2025-06-04"),
        "試験期間": ("2025-06-09", "2025-06-10")
    },
    "2Q": {
        "授業期間": ("2025-06-23", "2025-08-18"),
        "試験期間": ("2025-08-26", "2025-08-31")
    },
    "3Q": {
        "授業期間": ("2025-10-06", "2025-11-26"),
        "試験期間": ("2025-12-02", "2025-12-07")
    },
    "4Q": {
        "授業期間": ("2025-12-15", "2026-02-09"),
        "試験期間": ("2026-02-17", "2026-02-22")
    }
}

def get_nearest_quarter():
    today = datetime.now().date()
    nearest_quarter = None
    min_diff = float('inf')
    
    for q_name, q_data in QUARTERS.items():
        end_date = datetime.strptime(q_data["授業期間"][1], "%Y-%m-%d").date()
        if end_date >= today:
            diff = (end_date - today).days
            if diff < min_diff:
                min_diff = diff
                nearest_quarter = (q_name, end_date, diff)
    
    return nearest_quarter

def main():
    # セッション状態と変数の初期化
    if 'study_mode' not in st.session_state:
        st.session_state.update({
            'study_mode': "勉強時間で計画",
            'available_days': 0,
            'study_minutes_per_day': 0,
            'daily_classes': 0,
            'classes_per_day': 90
        })
    
    st.set_page_config(
        page_title="学習プランナー",
        page_icon="📚",
        layout="centered"
    )
    
    # モード選択 (フォーム外で実装)
    def on_mode_change():
        st.session_state.study_mode = st.session_state.mode_selector
        # st.rerun() はコールバック完了後に自動実行されるため不要
        
    st.radio(
        "計画モードを選択",
        ["勉強時間で計画", "コマ数で計画"],
        index=0 if st.session_state.study_mode == "勉強時間で計画" else 1,
        key="mode_selector",
        on_change=on_mode_change
    )
    st.title("クォーター制 学習プランナー")
    
    # クォーター情報表示
    quarter_info = get_nearest_quarter()
    if quarter_info:
        q_name, end_date, days_left = quarter_info
        st.subheader(f"現在のクォーター: {q_name}")
        st.write(f"今日の日付: {datetime.now().strftime('%Y年%m月%d日')}")
        st.write(f"授業終了日: {end_date.strftime('%Y年%m月%d日')}")
        weeks = days_left // 7
        remaining_days = days_left % 7
        st.write(f"残り日数: {days_left}日 ({weeks}週と{remaining_days}日)")
    
    with st.form("study_form"):
        st.subheader("基本設定")
        col1, col2 = st.columns(2)
        with col1:
            if quarter_info:
                _, _, days_left = quarter_info
        with col1:
            if quarter_info:
                _, _, days_left = quarter_info
        with col1:
            if quarter_info:
                _, _, days_left = quarter_info
                weeks_remaining = st.number_input(
                    "残りの期間(週数)",
                    min_value=0, 
                    value=max(1, days_left // 7),
                    step=1,
                    key='weeks_remaining_input' # key名を変更
                )
            else:
                weeks_remaining = st.number_input(
                    "残りの期間(週数)(例:12)",
                    min_value=0, step=1,
                    key='weeks_remaining_input' # key名を変更
                )
                
        with col2:
            minutes_per_class = st.number_input(
                "1コマあたりの時間(分) (例:90)",
                min_value=1, value=90, step=5,
                key='minutes_per_class_input' # key名を変更
            )
            classes_per_credit = st.number_input(
                "1単位あたりのコマ数 (例:15)",
                min_value=1, value=15, step=1,
                key='classes_per_credit_input' # key名を変更
            )
        
        st.subheader("勉強計画を入力")
        
        # 現在のモード表示
        st.write(f"現在のモード: {st.session_state.study_mode}")
        
        if st.session_state.study_mode == "勉強時間で計画":
            available_days = st.number_input(
                "毎週、勉強に使える日数(例:3)",
                min_value=1, 
                max_value=7, 
                step=1,
                value=st.session_state.available_days if st.session_state.available_days > 0 else 3,
                key='available_days_input', # key名を変更
                help="週に何日勉強できますか？"
            )
            study_minutes_per_day = st.number_input(
                "1日に勉強できる時間(分)(例:120)",
                min_value=30, 
                step=30,
                value=st.session_state.study_minutes_per_day if st.session_state.study_minutes_per_day > 0 else 120,
                key='study_minutes_input', # key名を変更
                help="1日あたりの勉強時間を入力"
            )
            # コマ数モード用入力欄は表示しない
        else:  # コマ数モード
            st.session_state.available_days = st.number_input(
                "毎週、勉強に使える日数(例:3)",
                min_value=1, 
                max_value=7, 
                step=1,
                value=st.session_state.available_days if st.session_state.available_days > 0 else 3,
                key='available_days_input_koma',
                help="週に何日勉強できますか？"
            )
            st.session_state.daily_classes = st.number_input(
                "1日に進める授業コマ数 (1-10)",
                min_value=1,
                max_value=10,
                step=1,
                value=st.session_state.daily_classes if st.session_state.daily_classes > 0 else 1,
                key='daily_classes_input',
                help="1日あたりの目標コマ数を入力"
            )
            # 勉強時間モード用入力欄は表示しない
            
        st.session_state.target_credits = st.number_input(
            "履修したい単位数(例:10)",
            min_value=1.0, 
            step=1.0,
            key='target_credits_input'
        )
        
        submitted = st.form_submit_button("計算する")
    
    if submitted:
        # フォーム送信時にセッション状態を更新 (ウィジェットのkey名を使用)
        st.session_state.weeks_remaining = st.session_state.weeks_remaining_input
        st.session_state.minutes_per_class = st.session_state.minutes_per_class_input
        st.session_state.classes_per_credit = st.session_state.classes_per_credit_input
        st.session_state.target_credits = st.session_state.target_credits_input
        
        if st.session_state.study_mode == "勉強時間で計画":
            st.session_state.available_days = st.session_state.available_days_input
            st.session_state.study_minutes_per_day = st.session_state.study_minutes_input
            st.session_state.daily_classes = 0 # コマ数モードの値をリセット
        else: # コマ数モード
            st.session_state.available_days = st.session_state.available_days_input_koma
            st.session_state.daily_classes = st.session_state.daily_classes_input
            st.session_state.study_minutes_per_day = 0 # 勉強時間モードの値をリセット
            
        calculate_results()

def calculate_results():
    # セッション状態からすべての値を取得
    available_days = st.session_state.get('available_days', 0)
    study_minutes_per_day = st.session_state.get('study_minutes_per_day', 0)
    target_credits = st.session_state.get('target_credits', 0)
    weeks_remaining = st.session_state.get('weeks_remaining', 0) 
    minutes_per_class = st.session_state.get('minutes_per_class', 90)
    classes_per_credit = st.session_state.get('classes_per_credit', 15)
    daily_classes = st.session_state.get('daily_classes', 0)
    # ユーザー設定に基づいて1単位あたりの時間を計算
    minutes_per_credit = classes_per_credit * minutes_per_class
    weekly_study_minutes = available_days * study_minutes_per_day
    credits_per_week = weekly_study_minutes / minutes_per_credit

    st.divider()
    st.subheader("計算結果")

    # 基本計算は常に実行（表示制御は後で処理）
    total_possible_credits = credits_per_week * weeks_remaining

    # 有効な計算モード判定 (セッション状態から取得)
    study_mode = st.session_state.get('study_mode', "勉強時間で計画")
    show_daily_classes_mode = study_mode == "コマ数で計画" and daily_classes > 0 and target_credits > 0
    show_normal_mode = study_mode == "勉強時間で計画" and target_credits > 0 and weeks_remaining > 0
    
    # コマ数モードの計算と表示
    if show_daily_classes_mode:
        total_classes = target_credits * classes_per_credit
        days_needed = total_classes / daily_classes
        study_days = available_days if available_days > 0 else 7
        
        st.info(f"🔔 コマ数ベースの計算結果:")
        weekly_classes = daily_classes * study_days
        st.write(f"毎週約 {weekly_classes} コマ進められます")
        weeks_needed = days_needed / study_days
        st.write(f"毎日{daily_classes}コマ進めると、目標達成まで約 {weeks_needed:.1f} 週間かかります")
        
        # 1日に必要な勉強時間を計算・表示
        daily_study_minutes = daily_classes * minutes_per_class
        hours = daily_study_minutes // 60
        minutes = daily_study_minutes % 60
        if hours > 0:
            st.write(f"   → 1日あたり約 {hours}時間{minutes}分の勉強が必要です")
        else:
            st.write(f"   → 1日あたり約 {minutes}分の勉強が必要です")
        
        if weeks_remaining > 0:
            if weeks_needed <= weeks_remaining:
                st.success(f"⏱️ 残り{weeks_remaining}週間で目標達成可能！")
            else:
                extra_weeks = weeks_needed - weeks_remaining
                st.error(f"⚠️ 残り期間では不足。あと約 {extra_weeks:.1f} 週間必要です")
        st.divider()
    
    # 通常モードの計算結果 (コマ数モード非アクティブ時のみ表示)
    if show_normal_mode:
        st.info("📊 単位ベースの計算結果:")
        st.write(f"毎週約 {credits_per_week:.2f} 単位分の勉強が可能")
        st.write(f"残り期間で取得可能な単位数: {total_possible_credits:.2f} 単位")
        st.divider()
    elif target_credits <= 0 or weeks_remaining <= 0:
        st.warning("目標単位数と残り週数を正しく入力してください")

    # 勉強時間モードの場合のみ推奨値を計算・表示
    if study_mode == "勉強時間で計画":
        if available_days == 0 or study_minutes_per_day == 0:
            st.subheader("勉強計画の推奨値")
            if target_credits > 0 and weeks_remaining > 0:
                required_weekly_minutes = (target_credits * minutes_per_credit) / weeks_remaining
            
            if available_days == 0:
                recommended_days = min(7, max(1, round(required_weekly_minutes / 120)))  # 1日120分を目安
                st.info(f"目標達成には週に {recommended_days} 日、勉強する必要があります")
                
            if study_minutes_per_day == 0:
                if available_days > 0:
                    recommended_minutes = max(30, round(required_weekly_minutes / available_days))
                    hours = recommended_minutes // 60
                    minutes = recommended_minutes % 60
                    if hours > 0:
                        st.info(f"目標達成には1日約 {hours}時間{minutes}分、勉強する必要があります")
                    else:
                        st.info(f"目標達成には1日約 {minutes}分、勉強する必要があります")
                else:
                    st.info("週の勉強日数を入力すると、1日に必要な勉強時間を計算できます")
            else:
                st.warning("目標単位数と残り週数を入力してください")
        
        # 勉強時間モードでの達成可否判定
        if show_normal_mode:
            if credits_per_week == 0:
                st.warning("勉強時間が確保できてないみたい...もっと時間を作ってね!")
            else:
                weeks_needed = target_credits / credits_per_week
                if weeks_needed <= weeks_remaining:
                    st.success(f"目標の {target_credits:.2f} 単位を取得するには、あと {weeks_needed:.1f} 週間で大丈夫!")
                else:
                    extra_weeks = weeks_needed - weeks_remaining
                    st.error(f"目標の {target_credits:.2f} 単位を取得するには、あと {weeks_needed:.1f} 週間必要だよ。")
                    st.error(f"つまり、今のペースだと、残りの {weeks_remaining} 週間では足りず、さらに {extra_weeks:.1f} 週間追加で必要かも")

                # 一日あたり進めるコマ数を計算 (勉強時間モード時のみ)
                if available_days > 0 and weeks_remaining > 0:
                    total_required_classes = target_credits * classes_per_credit
                    daily_required_classes = total_required_classes / (weeks_remaining * available_days)
                    st.info(f"目標の {target_credits:.2f} 単位を取得するには、毎日 {daily_required_classes:.2f} コマの授業を進める必要があるよ!")
                else:
                    st.warning("一日あたりのコマ数の計算ができないよ。")
        
if __name__ == "__main__":
    main()
