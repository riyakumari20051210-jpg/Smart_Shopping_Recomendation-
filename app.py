import streamlit as st
import pandas as pd
import plotly.express as px

from recommender import recommend_products, load_data


# Page configuration
st.set_page_config(
    page_title="Smart Shopping Recommendation System",
    page_icon="🛍️",
    layout="wide"
)


# Title
st.title("🛍️ Smart Shopping Recommendation System")

st.write(
    "Find the best products according to your category, "
    "budget and minimum rating."
)


# Load dataset
df = load_data()


# Sidebar
st.sidebar.header("🔍 Shopping Preferences")

category = st.sidebar.selectbox(
    "Select Category",
    df["category"].unique()
)

budget = st.sidebar.number_input(
    "Maximum Budget (₹)",
    min_value=1000,
    max_value=200000,
    value=60000,
    step=1000
)

min_rating = st.sidebar.slider(
    "Minimum Rating",
    min_value=0.0,
    max_value=5.0,
    value=4.0,
    step=0.1
)


# Recommendation button
if st.sidebar.button("Get Recommendations"):

    recommendations = recommend_products(
        category,
        budget,
        min_rating
    )

    st.subheader("⭐ Recommended Products")

    if recommendations.empty:

        st.warning(
            "No products found. Try increasing your budget "
            "or reducing the minimum rating."
        )

    else:

        # Display products
        for index, row in recommendations.iterrows():

            st.markdown(
                f"""
                ### 🏆 {row['product_name']}

                **Brand:** {row['brand']}  
                **Price:** ₹{row['price']:,.0f}  
                **Rating:** ⭐ {row['rating']}  
                **Discount:** {row['discount']}%  
                **Recommendation Score:** 
                {row['recommendation_score']}%

                **Features:** {row['features']}
                """
            )

            st.divider()


        # Chart 1
        st.subheader("📊 Recommendation Score")

        fig1 = px.bar(
            recommendations,
            x="product_name",
            y="recommendation_score",
            title="Product Recommendation Score",
            labels={
                "product_name": "Product",
                "recommendation_score": "Score (%)"
            }
        )

        st.plotly_chart(
            fig1,
            use_container_width=True
        )


        # Chart 2
        st.subheader("💰 Price vs Rating")

        fig2 = px.scatter(
            recommendations,
            x="price",
            y="rating",
            size="recommendation_score",
            hover_name="product_name",
            title="Price vs Rating",
            labels={
                "price": "Price (₹)",
                "rating": "Rating"
            }
        )

        st.plotly_chart(
            fig2,
            use_container_width=True
        )


        # Chart 3
        st.subheader("🏷️ Discount Comparison")

        fig3 = px.bar(
            recommendations,
            x="product_name",
            y="discount",
            title="Product Discount Comparison",
            labels={
                "product_name": "Product",
                "discount": "Discount (%)"
            }
        )

        st.plotly_chart(
            fig3,
            use_container_width=True
        )


# Dataset section
st.subheader("📋 Product Dataset")

st.dataframe(
    df,
    use_container_width=True
)


#py -m streamlit run app.py