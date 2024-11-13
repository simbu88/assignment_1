import streamlit as st

def about_us():
    st.title("About Us")
    
    st.write(
        """
        Welcome to the Youtube Data Harvesting Application!

        Youtube Data Harvesting was developed by myself, an IT professional with over 13 years of industry experience. This project marks my first venture into the world of AI and machine learning as part of an advanced course, where I’m excited to apply and share my knowledge in data science.

        If you have any questions or suggestions about the project, feel free to reach out! Contact me at: simbu88.btech@gmail.com
        """
    )
    
      
    # Team Member 1
    col1, col2 = st.columns([1, 3])
    with col1:
        st.image("./images/user.png", width=150)  # Replace with actual image path or URL
    with col2:
        st.subheader("Silambarasan Damodaran")
        st.write("**Role:** Project Lead")
        


# Run the about_us function to display the About Us page
about_us()
