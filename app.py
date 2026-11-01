
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="E-commerce Review Analytics",
    page_icon="🛒",
    layout="wide"
)

st.title("🛒 E-commerce Product Review Analysis")
st.write("Big Data Analytics Project")

# Upload dataset
uploaded_file = st.file_uploader(
    "Upload Processed Amazon Reviews CSV",
    type=["csv"]
)

if uploaded_file is not None:

    df = pd.read_csv(uploaded_file)

    # KPI calculations
    total_reviews = len(df)
    avg_rating = df["Rating"].mean()

    sentiment_counts = df["Sentiment"].value_counts()

    positive = sentiment_counts.get("Positive", 0)
    negative = sentiment_counts.get("Negative", 0)
    neutral = sentiment_counts.get("Neutral", 0)

    positive_percentage = positive / total_reviews * 100
    negative_percentage = negative / total_reviews * 100

    # KPI cards
    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Total Reviews", total_reviews)
    c2.metric("Average Rating", round(avg_rating, 2))
    c3.metric("Positive Reviews", f"{positive_percentage:.1f}%")
    c4.metric("Negative Reviews", f"{negative_percentage:.1f}%")

    st.divider()

    # Navigation
    tab1, tab2, tab3, tab4 = st.tabs([
        "Sentiment Analysis",
        "Rating Analysis",
        "Country Analysis",
        "Customer Feedback"
    ])

    with tab1:

        st.subheader("Customer Sentiment Distribution")

        sentiment_df = pd.DataFrame({
            "Sentiment": ["Positive", "Negative", "Neutral"],
            "Count": [positive, negative, neutral]
        })

        fig = px.pie(
            sentiment_df,
            names="Sentiment",
            values="Count",
            hole=0.4
        )

        st.plotly_chart(fig, use_container_width=True)

    with tab2:

        st.subheader("Rating Distribution")

        rating_df = df["Rating"].value_counts().sort_index()

        fig = px.bar(
            x=rating_df.index,
            y=rating_df.values,
            labels={"x": "Rating", "y": "Reviews"}
        )

        st.plotly_chart(fig, use_container_width=True)

    with tab3:

        st.subheader("Country-wise Review Analysis")

        if "Country" in df.columns:

            country_df = df["Country"].value_counts().head(10)

            fig = px.bar(
                x=country_df.index,
                y=country_df.values,
                labels={"x": "Country", "y": "Reviews"}
            )

            st.plotly_chart(fig, use_container_width=True)

    with tab4:

        st.subheader("Customer Feedback")

        sentiment_filter = st.selectbox(
            "Select Sentiment",
            ["All", "Positive", "Negative", "Neutral"]
        )

        if sentiment_filter != "All":
            filtered_df = df[
                df["Sentiment"] == sentiment_filter
            ]
        else:
            filtered_df = df

        search = st.text_input("Search customer reviews")

        if search:
            filtered_df = filtered_df[
                filtered_df["Review Text"].astype(str).str.contains(
                    search,
                    case=False,
                    na=False
                )
            ]

        display_columns = [
            c for c in [
                "Country", "Rating", "Review Title",
                "Review Text", "Sentiment"
            ] if c in filtered_df.columns
        ]

        st.dataframe(
            filtered_df[display_columns],
            use_container_width=True
        )

    # Download report
    st.divider()

    csv = df.to_csv(index=False).encode("utf-8")

    st.download_button(
        "Download Analysis Report",
        data=csv,
        file_name="amazon_review_analysis.csv",
        mime="text/csv"
    )

else:
    st.info("Please upload your processed Amazon reviews CSV.")
