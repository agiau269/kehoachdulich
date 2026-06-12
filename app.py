import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ======================
# Cấu hình trang
# ======================

st.set_page_config(
    page_title="Travel Planner",
    page_icon="✈️",
    layout="wide"
)

# ======================
# Tiêu đề
# ======================

st.title("✈️ Travel Planner & Budget Tracker")
st.write("Lập kế hoạch du lịch, quản lý chi phí và ghi chú chuyến đi")

st.divider()

# ======================
# Thông tin chuyến đi
# ======================

st.header("📍 Thông tin chuyến đi")

col1, col2 = st.columns(2)

with col1:
  
    destination = st.text_input("Điểm đến")

with col2:
    travel_date = st.date_input("Ngày khởi hành")

days = st.number_input(
    "Số ngày du lịch",
    min_value=1,
    value=3
)

st.divider()

# ======================
# Lịch trình
# ======================

st.header("🗓️ Lịch trình")

schedule = {}

for day in range(1, days + 1):

    with st.expander(f"Ngày {day}"):

        morning = st.text_input(
            f"🌤️ Buổi sáng - Ngày {day}"
        )

        afternoon = st.text_input(
            f"☀️ Buổi chiều - Ngày {day}"
        )

        evening = st.text_input(
            f"🌙 Buổi tối - Ngày {day}"
        )

        schedule[day] = [
            morning,
            afternoon,
            evening
        ]

st.divider()

# ======================
# Chi phí
# ======================

st.header("💰 Quản lý chi phí")

col1, col2 = st.columns(2)

with col1:
    transport = st.number_input(
        "🚗 Di chuyển",
        min_value=0,
        value=0
    )

    hotel = st.number_input(
        "🏨 Khách sạn",
        min_value=0,
        value=0
    )

    food = st.number_input(
        "🍜 Ăn uống",
        min_value=0,
        value=0
    )

with col2:
    ticket = st.number_input(
        "🎫 Vé tham quan",
        min_value=0,
        value=0
    )

    other = st.number_input(
        "📦 Chi phí khác",
        min_value=0,
        value=0
    )

total = transport + hotel + food + ticket + other

st.success(
    f"💵 Tổng chi phí dự kiến: {total:,.0f} VNĐ"
)

# ======================
# Biểu đồ chi phí
# ======================

st.subheader("📊 Phân bổ chi phí")

values = [
    transport,
    hotel,
    food,
    ticket,
    other
]

labels = [
    "Di chuyển",
    "Khách sạn",
    "Ăn uống",
    "Tham quan",
    "Khác"
]

if total > 0:

    fig, ax = plt.subplots()

    ax.pie(
        values,
        labels=labels,
        autopct="%1.1f%%"
    )

    st.pyplot(fig)

else:
    st.info("Nhập chi phí để hiển thị biểu đồ")

st.divider()

# ======================
# Ghi chú
# ======================

st.header("📝 Ghi chú chuyến đi")

note = st.text_area(
    "Nhập ghi chú",
    height=150
)

st.divider()

# ======================
# Lưu dữ liệu
# ======================

if st.button("💾 Lưu kế hoạch"):

    data = {
        "Điểm đến": [destination],
        "Ngày khởi hành": [travel_date],
        "Số ngày": [days],
        "Tổng chi phí": [total],
        "Ghi chú": [note]
    }

    df = pd.DataFrame(data)

    try:
        old_df = pd.read_csv("trip_data.csv")
        df = pd.concat([old_df, df], ignore_index=True)
    except:
        pass

    df.to_csv(
        "trip_data.csv",
        index=False
    )

    st.success("✅ Đã lưu kế hoạch thành công!")

st.divider()

# ======================
# Kế hoạch đã lưu
# ======================

st.header("📁 Kế hoạch đã lưu")

try:

    saved_df = pd.read_csv("trip_data.csv")

    st.dataframe(
        saved_df,
        use_container_width=True
    )

    st.subheader("🗑️ Xóa kế hoạch")

    row_to_delete = st.selectbox(
        "Chọn kế hoạch muốn xóa",
        saved_df.index,
        format_func=lambda x:
        f"{saved_df.loc[x, 'Điểm đến']} - {saved_df.loc[x, 'Ngày khởi hành']}"
    )

    confirm = st.checkbox(
        "Tôi chắc chắn muốn xóa kế hoạch này"
    )

    if confirm and st.button("❌ Xóa kế hoạch"):

        saved_df = saved_df.drop(
            row_to_delete
        )

        saved_df.to_csv(
            "trip_data.csv",
            index=False
        )

        st.success(
            "✅ Đã xóa kế hoạch!"
        )

        st.rerun()

except:
    st.info("Chưa có kế hoạch nào được lưu.")
