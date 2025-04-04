import streamlit as st

def main():
    st.title("単位取得の目安計算ツール")
    
    with st.form("study_form"):
        st.subheader("勉強計画を入力")
        available_days = st.number_input(
            "毎週、勉強に使える日数を入力してね(例:3)",
            min_value=0, max_value=7, step=1
        )
        study_minutes_per_day = st.number_input(
            "1日に勉強できる時間(分)を入力してね(例:120)",
            min_value=0, step=5
        )
        target_credits = st.number_input(
            "履修したい単位数を入力してね(例:10)",
            min_value=0.0, step=0.5
        )
        weeks_remaining = st.number_input(
            "残りの期間(何週間あるか)を入力してね(例:12)",
            min_value=0, step=1
        )
        
        submitted = st.form_submit_button("計算する")
    
    if submitted:
        calculate_results(
            available_days,
            study_minutes_per_day,
            target_credits,
            weeks_remaining
        )

def calculate_results(available_days, study_minutes_per_day, target_credits, weeks_remaining):
    # 1単位は15コマ×90分=1350分の授業に相当
    minutes_per_credit = 15 * 90  # 1350分
    weekly_study_minutes = available_days * study_minutes_per_day
    credits_per_week = weekly_study_minutes / minutes_per_credit

    st.divider()
    st.subheader("計算結果")
    st.write(f"あなたは毎週、約 {credits_per_week:.2f} 単位分の勉強ができるよ!")
    total_possible_credits = credits_per_week * weeks_remaining
    st.write(f"残りの期間では、合計で約 {total_possible_credits:.2f} 単位分取れる計算だヨ")
    st.divider()

    if credits_per_week == 0:
        st.warning("勉強時間が確保できてないみたい...もっと時間を作ってね!")
    else:
        weeks_needed = target_credits / credits_per_week
        if weeks_needed <= weeks_remaining:
            st.success(f"目標の {target_credits:.2f} 単位を取得するには、あと約 {weeks_needed:.1f} 週間で大丈夫!")
        else:
            extra_weeks = weeks_needed - weeks_remaining
            st.error(f"目標の {target_credits:.2f} 単位を取得するには、あと約 {weeks_needed:.1f} 週間必要だよ。")
            st.error(f"つまり、今のペースだと、残りの {weeks_remaining} 週間では足りず、さらに約 {extra_weeks:.1f} 週間追加で必要かも")

        # 一日あたり進めるコマ数を計算
        if available_days > 0 and weeks_remaining > 0:
            total_required_classes = target_credits * 15  # 必要な総コマ数
            daily_required_classes = total_required_classes / (weeks_remaining * available_days)
            st.info(f"目標の {target_credits:.2f} 単位を取得するには、毎日約 {daily_required_classes:.2f} コマの授業を進める必要があるよ!")
        else:
            st.warning("一日あたりのコマ数の計算ができないよ。")

if __name__ == "__main__":
    main()
