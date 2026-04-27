import pandas as pd
import streamlit as st
import plotly.express as px

# Load dataset
try:
    df = pd.read_csv("company_data.csv")
except FileNotFoundError:
    df = pd.read_csv("public/company_data.csv")

st.title("📊 Company Analysis Dashboard")

# Select company
company = st.selectbox("Select Company", df["Company"].unique())
df_company = df[df["Company"] == company]

# Select year
year = st.selectbox("Select Year", df_company["Year"].unique())
df_filtered = df_company[df_company["Year"] == year]

# Charts
st.subheader("Experience Distribution")
st.plotly_chart(px.pie(df_filtered, names="Experience"))

st.subheader("Salary by Role")
st.plotly_chart(px.bar(df_filtered, x="Role", y="Salary_LPA"))

st.subheader("Skill Demand")
st.plotly_chart(px.histogram(df_filtered, x="Skill"))

# ------------------------
# Recommendation Feature
# ------------------------
st.sidebar.title("🔍 Career Recommendation")

role = st.sidebar.selectbox("Select Role", df["Role"].unique())
skill = st.sidebar.selectbox("Select Skill", df["Skill"].unique())

filtered = df[(df["Role"] == role) & (df["Skill"] == skill)]

top = filtered["Company"].value_counts().head(3)

st.sidebar.write("Top Companies:")
st.sidebar.write(top)

# ------------------------
# 1) Hiring Type Analysis
# ------------------------
st.header("Hiring Type Analysis")

if not df_filtered.empty and "Hiring_Type" in df_filtered.columns:
    st.subheader(f"Hiring Type Distribution for {company} ({year})")
    st.plotly_chart(px.pie(df_filtered, names="Hiring_Type"))
    
    most_frequent_hiring = df_filtered["Hiring_Type"].mode()[0] if not df_filtered["Hiring_Type"].mode().empty else "Unknown"
    st.write(f"This company hires more through {most_frequent_hiring} drives.")
    
st.subheader("Hiring Type Across All Companies")
hiring_all = df.groupby(["Company", "Hiring_Type"]).size().reset_index(name="Count")
st.plotly_chart(px.bar(hiring_all, x="Company", y="Count", color="Hiring_Type", barmode="group"))

# ------------------------
# 2) Top Skills per Company
# ------------------------
st.header("Top Skills per Company")
st.subheader(f"Top Skills for {company}")

if not df_company.empty:
    skill_counts = df_company["Skill"].value_counts().reset_index()
    skill_counts.columns = ["Skill", "Count"]
    top_3_skills = skill_counts.head(3)
    
    st.write("Top 3 Most Frequent Skills:")
    for idx, row in top_3_skills.iterrows():
        st.write(f"• {row['Skill']} (Frequency: {row['Count']})")
        
    st.plotly_chart(px.bar(top_3_skills, x="Skill", y="Count"))
    st.write("These are the most demanded skills in this company.")

# ------------------------
# 3) Company Ranking System
# ------------------------
st.header("Company Ranking System")

ranking_data = []
for c in df["Company"].unique():
    c_data = df[df["Company"] == c]
    avg_sal = c_data["Salary_LPA"].mean()
    h_count = len(c_data)
    s_freq = c_data["Skill"].value_counts().max() if not c_data["Skill"].empty else 0
    ranking_data.append({"Company": c, "Salary": avg_sal, "Hiring_Count": h_count, "Skill_Frequency": s_freq})

ranking_df = pd.DataFrame(ranking_data).fillna(0)

if not ranking_df.empty:
    ranking_df["Salary_Norm"] = ranking_df["Salary"] / ranking_df["Salary"].max() if ranking_df["Salary"].max() > 0 else 0
    ranking_df["Hiring_Count_Norm"] = ranking_df["Hiring_Count"] / ranking_df["Hiring_Count"].max() if ranking_df["Hiring_Count"].max() > 0 else 0
    ranking_df["Skill_Frequency_Norm"] = ranking_df["Skill_Frequency"] / ranking_df["Skill_Frequency"].max() if ranking_df["Skill_Frequency"].max() > 0 else 0

    ranking_df["Score"] = ranking_df["Salary_Norm"] + ranking_df["Hiring_Count_Norm"] + ranking_df["Skill_Frequency_Norm"]
    ranking_df = ranking_df.sort_values(by="Score", ascending=False).reset_index(drop=True)
    
    top_5 = ranking_df.head(5)
    
    st.subheader("Top 5 Ranked Companies")
    st.dataframe(top_5[["Company", "Score", "Salary", "Hiring_Count", "Skill_Frequency"]])
    
    best_company = top_5.iloc[0]["Company"]
    st.success(f"🏆 The Best Company based on the ranking system is: **{best_company}**")
    
    st.plotly_chart(px.bar(top_5, x="Company", y="Score", title="Top 5 Companies by Score"))
