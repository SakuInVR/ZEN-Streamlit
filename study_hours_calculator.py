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
    st.title("単位取得の目安計算ツール")
    
    # クォーター情報表示
    quarter_info = get_nearest_quarter()
    if quarter_info:
        q_name, end_date, days_left = quarter_info
        st.subheader(f"現在のクォーター: {q_name}")
        st.write(f"今日の日付: {datetime.now().strftime('%Y年%m月%d日')}")
        st.write(f"授業終了日: {end_date.strftime('%Y年%m月%d日')}")
        st.write(f"残り日数: {days_left}日")
    
    with st.form("study_form"):
        st.subheader("基本設定")
        if quarter_info:
            _, _, days_left = quarter_info
            weeks_remaining = st.number_input(
                "残りの期間(週数)",
                min_value=0, 
                value=max(1, days_left // 7),
                step=1
            )
        else:
            weeks_remaining = st.number_input(
                "残りの期間(週数)(例:12)",
                min_value=0, step=1
            )
            
        minutes_per_class = st.number_input(
            "1コマあたりの時間(分) (例:90)",
            min_value=1, value=90, step=5
        )
        classes_per_credit = st.number_input(
            "1単位あたりのコマ数 (例:15)",
            min_value=1, value=15, step=1
        )
        
        st.subheader("勉強計画を入力")
        st.info("📝 以下のいずれかを空欄にすると、目標達成に必要な勉強量を逆算できます")
        available_days = st.number_input(
            "毎週、勉強に使える日数(例:3)",
            min_value=0, max_value=7, step=1,
            help="0にすると推奨日数が計算されます"
        )
        study_minutes_per_day = st.number_input(
            "1日に勉強できる時間(分)(例:120)",
            min_value=0, step=30,
            help="0にすると推奨勉強時間が計算されます"
        )
        target_credits = st.number_input(
            "履修したい単位数(例:10)",
            min_value=0.0, 
            step=1.0
        )
        
        submitted = st.form_submit_button("計算する")
    
    if submitted:
        calculate_results(
            available_days,
            study_minutes_per_day,
            target_credits,
            weeks_remaining,
            minutes_per_class,
            classes_per_credit
        )

def calculate_results(available_days, study_minutes_per_day, target_credits, weeks_remaining, minutes_per_class, classes_per_credit):
    # ユーザー設定に基づいて1単位あたりの時間を計算
    minutes_per_credit = classes_per_credit * minutes_per_class
    weekly_study_minutes = available_days * study_minutes_per_day
    credits_per_week = weekly_study_minutes / minutes_per_credit

    st.divider()
    st.subheader("計算結果")
    st.write(f"あなたは毎週、 {credits_per_week:.2f} 単位分の勉強ができるよ!")
    total_possible_credits = credits_per_week * weeks_remaining
    st.write(f"残りの期間では、合計で {total_possible_credits:.2f} 単位分取れる計算だよ！")
    st.divider()

    # 勉強計画が未入力の場合の推奨値を計算
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

    if credits_per_week == 0:
        st.warning("勉強時間が確保できてないみたい...もっと時間を作ってね!")
    else:
        weeks_needed = target_credits / credits_per_week
        if weeks_needed <= weeks_remaining:
            st.success(f"目標の {target_credits:.2f} 単位を取得するには、あと {weeks_needed:.1f} 週間で大丈夫!")
        else:
            extra_weeks = weeks_needed - weeks_remaining
            st.error(f"目標の {target_credits:.2f} 単位を取得するには、あと {weeks_needed:.1f} 週間必要だよ。")
            st.error(f"つまり、今のペースだと、残りの {weeks_remaining} 週間では足りず、さらに {extra_weeks:.1f} 週間追加で必要かも")

        # 一日あたり進めるコマ数を計算
        if available_days > 0 and weeks_remaining > 0:
            total_required_classes = target_credits * classes_per_credit
            daily_required_classes = total_required_classes / (weeks_remaining * available_days)
            st.info(f"目標の {target_credits:.2f} 単位を取得するには、毎日 {daily_required_classes:.2f} コマの授業を進める必要があるよ!")
        else:
            st.warning("一日あたりのコマ数の計算ができないよ。")

if __name__ == "__main__":
    main()
