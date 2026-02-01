import streamlit as st
import pandas as pd
import plotly.express as px
import os

# ملف البيانات
DB_FILE = "data.csv"

def load_data():
    cols = ["Name", "Botany", "Zoology", "Chemistry", "Math", "Physics", "English"]
    if os.path.exists(DB_FILE):
        try:
            df = pd.read_csv(DB_FILE)
            # التأكد من مطابقة الأعمدة في حال تم تغييرها
            if list(df.columns) != cols:
                return pd.DataFrame(columns=cols)
            return df
        except:
            return pd.DataFrame(columns=cols)
    return pd.DataFrame(columns=cols)

st.set_page_config(page_title="Advanced Analytics System", layout="wide")

# تنسيق الموقع
st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    .stMetric { background-color: white; padding: 15px; border-radius: 10px; box-shadow: 2px 2px 10px rgba(0,0,0,0.1); }
    </style>
    """, unsafe_allow_html=True)

menu = ["📝 Register Grades", "📊 Admin Dashboard"]
choice = st.sidebar.selectbox("Menu", menu)

if choice == "📝 Register Grades":
    st.title("📝 Student Grades Entry")
    st.write("Please enter your scores accurately:")
    with st.form("student_form", clear_on_submit=True):
        name = st.text_input("Full Name (Optional)")
        c1, c2 = st.columns(2)
        with c1:
            botany = st.number_input("Botany", 0, 100, 0)
            zoology = st.number_input("Zoology", 0, 100, 0)
            chem = st.number_input("Chemistry", 0, 100, 0)
        with c2:
            math = st.number_input("Math", 0, 100, 0)
            phys = st.number_input("Physics", 0, 100, 0)
            eng = st.number_input("English", 0, 100, 0)
        
        if st.form_submit_button("Submit Data"):
            df = load_data()
            new_row = {"Name": name if name else "Anonymous", "Botany": botany, "Zoology": zoology, "Chemistry": chem, "Math": math, "Physics": phys, "English": eng}
            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
            df.to_csv(DB_FILE, index=False)
            st.success("✅ Data saved successfully!")

else:
    st.title("📊 Admin Statistical Analysis")
    pw = st.text_input("Enter Password", type="password")
    
    if pw == "3070":
        df = load_data()
        if not df.empty:
            st.write("### 📈 Overview")
            col1, col2 = st.columns(2)
            col1.metric("Total Students", len(df))
            
            subjects = ["Botany", "Zoology", "Chemistry", "Math", "Physics", "English"]
            subject = st.selectbox("Select Subject for Analysis:", subjects)
            
            # رسم بياني تفاعلي
            fig = px.bar(df, x="Name", y=subject, color=subject, 
                         title=f"Students Grades in {subject}",
                         color_continuous_scale=px.colors.sequential.Viridis,
                         text_auto=True)
            st.plotly_chart(fig, use_container_width=True)

            st.markdown("---")
            st.write(f"### ⚠️ Students Below 60 in {subject}")
            
            low_60_55 = df[(df[subject] < 60) & (df[subject] >= 55)]
            low_55_50 = df[(df[subject] < 55) & (df[subject] >= 50)]
            low_under_50 = df[df[subject] < 50]

            c1, c2, c3 = st.columns(3)
            c1.warning(f"Grade (55-59): {len(low_60_55)}")
            c2.warning(f"Grade (50-54): {len(low_55_50)}")
            c3.error(f"Below 50: {len(low_under_50)}")

            st.write("#### Detailed List (Below 60):")
            st.table(df[df[subject] < 60][["Name", subject]])

            st.markdown("---")
            st.write("### 📋 Full Data Table")
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No data registered yet.")
    elif pw:
        st.error("❌ Incorrect Password!")
