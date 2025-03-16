import streamlit as st
import requests
import pandas as pd
from datetime import datetime
import base64

# Load and encode background and logo images
def get_base64_encoded_image(file_path):
    with open(file_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()

# Load background image once
bg_image = get_base64_encoded_image("attached_assets/Gl6mQfnXIAAam8z.jpg")
logo_image = get_base64_encoded_image("attached_assets/monad-labs-removebg-preview.png")

# Custom CSS with background image
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    /* Global font settings */
    * {{
        font-family: 'Inter', sans-serif;
    }}

    /* Background image with blur */
    .stApp {{
        background-image: url(data:image/jpg;base64,{bg_image});
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
    }}

    /* Logo styling */
    .logo {{
        width: 40px;
        height: 40px;
        display: inline-block;
        margin-right: 10px;
    }}

    /* Header container */
    .header-container {{
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 10px;
        margin-bottom: 2rem;
    }}

    /* Title text */
    .title-text {{
        font-size: 3em;
        font-weight: 800;
        background: linear-gradient(120deg, #836EF9, #9B8AFB);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        display: inline-block;
        line-height: 1.2;
    }}

    /* Overlay for better content visibility */
    .stApp:before {{
        content: "";
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(32, 0, 82, 0.75);
        backdrop-filter: blur(5px);
        z-index: 0;
    }}

    /* Ensure content stays above the overlay */
    .stApp > header {{
        z-index: 1;
        position: relative;
    }}

    .main {{
        z-index: 1;
        position: relative;
    }}

    /* Button styling */
    .stButton > button {{
        width: 100%;
        border-radius: 12px;
        border: 2px solid #836EF9;
        padding: 15px 32px;
        background: linear-gradient(45deg, #836EF9, #9B8AFB);
        color: #FBFAF9;
        font-weight: 600;
        font-family: 'Inter', sans-serif;
        letter-spacing: -0.01em;
        transition: all 0.3s ease;
    }}

    .stButton > button:hover {{
        transform: translateY(-3px);
        box-shadow: 0 8px 15px rgba(131, 110, 249, 0.3);
        background: linear-gradient(45deg, #9B8AFB, #836EF9);
    }}

    /* Card-like container */
    .content-container {{
        background: rgba(32, 0, 82, 0.6);
        border-radius: 15px;
        padding: 25px;
        backdrop-filter: blur(5px);
        border: 1px solid rgba(131, 110, 249, 0.2);
        margin: 10px 0;
        box-shadow: 0 8px 32px 0 rgba(131, 110, 249, 0.2);
    }}

    /* Subtitle and heading styles */
    h2, h3, h4, h5, h6 {{
        font-family: 'Inter', sans-serif;
        font-weight: 600;
        letter-spacing: -0.01em;
        color: #FBFAF9;
        margin-bottom: 1rem;
    }}

    /* Paragraph text */
    p, div {{
        font-family: 'Inter', sans-serif;
        font-weight: 400;
        line-height: 1.6;
        letter-spacing: -0.005em;
        color: #FBFAF9;
    }}

    /* Input field styling */
    .stTextInput > div > div > input {{
        font-family: 'Inter', sans-serif;
        border-radius: 10px;
        border: 1px solid #836EF9;
        background: rgba(32, 0, 82, 0.7);
        color: #FBFAF9;
        font-size: 1rem;
        letter-spacing: -0.005em;
    }}

    /* Metric styling */
    .css-1xarl3l {{
        background: rgba(32, 0, 82, 0.6);
        border-radius: 15px;
        padding: 20px;
        border: 1px solid rgba(131, 110, 249, 0.2);
        font-family: 'Inter', sans-serif;
        color: #FBFAF9;
    }}

    /* Label text */
    .stTextInput > label {{
        font-family: 'Inter', sans-serif;
        font-weight: 500;
        letter-spacing: -0.005em;
        color: #FBFAF9;
    }}

    /* Table text color */
    .stDataFrame {{
        color: #FBFAF9;
    }}
</style>

<div class="header-container">
    <img src='data:image/png;base64,{logo_image}' class='logo' alt='Monad Logo'>
    <span class="title-text">moNFT Holder Explorer</span>
</div>
""", unsafe_allow_html=True)

def fetch_addresses(contract_address, api_key):
    base_url = "https://api.blockvision.org/v2/monad/collection/holders"
    headers = {
        "accept": "application/json",
        "x-api-key": api_key
    }

    page_index = 1
    page_size = 50
    unique_addresses = set()
    total_processed = 0

    progress_bar = st.progress(0)
    status_text = st.empty()

    while True:
        status_text.text(f"🔍 Scanning page {page_index}...")
        url = f"{base_url}?contractAddress={contract_address}&pageIndex={page_index}&pageSize={page_size}"

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()

            data = response.json()
            current_holders = data.get('result', {}).get('data', [])

            if not current_holders:
                break

            for holder in current_holders:
                unique_addresses.add(holder['ownerAddress'])

            total_processed += len(current_holders)
            status_text.text(f"✨ Found {len(unique_addresses)} unique addresses...")
            progress_bar.progress(min(1.0, total_processed / 100))

            page_index += 1

        except requests.exceptions.RequestException as e:
            st.error(f"🚫 Error fetching data: {str(e)}")
            break

    progress_bar.empty()
    status_text.empty()
    return list(unique_addresses)

def main():
    st.markdown("""
<div style='text-align: center; color: #FBFAF9; font-size: 1.2em; margin-bottom: 30px;'>
    Take a snapshot of any moNFT holder addresses in just a few clicks and download them as a .csv or .txt file
</div>
""", unsafe_allow_html=True)

    # Create a card-like container with custom styling
    st.markdown('<div class="content-container">', unsafe_allow_html=True)

    # Input fields
    contract_address = st.text_input(
        "🔑 Contract Address",
        value="0xC7fBC69880a20Bac235d3965854275c20f875930",
        help="Enter the blockchain contract address"
    )

    api_key = st.text_input(
        "🔐 API Key",
        value="2ttJIAwzUhX7pUi4G96NOXwXOiU",
        help="Enter your BlockVision API key",
        type="password"
    )

    st.markdown('</div>', unsafe_allow_html=True)

    if st.button("🚀 Fetch Unique Addresses"):
        if not contract_address:
            st.error("⚠️ Please enter a contract address")
            return

        if not api_key:
            st.error("⚠️ Please enter an API key")
            return

        with st.spinner("🔮 Fetching unique addresses..."):
            addresses = fetch_addresses(contract_address, api_key)

            if addresses:
                # Create a new container for results
                st.markdown('<div class="content-container">', unsafe_allow_html=True)

                # Display statistics in a styled container
                st.markdown("### 📊 Statistics")
                st.metric("🎯 Total Unique Addresses", f"{len(addresses):,}")

                # Display data table
                st.markdown("### 📋 Unique Addresses")
                df = pd.DataFrame(addresses, columns=['Address'])
                st.dataframe(df, use_container_width=True)

                # Create download buttons
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                col1, col2 = st.columns(2)

                # Download as CSV
                with col1:
                    csv = df.to_csv(index=False)
                    st.download_button(
                        label="📥 Download CSV",
                        data=csv,
                        file_name=f"unique_addresses_{timestamp}.csv",
                        mime="text/csv"
                    )

                # Download as plain text
                with col2:
                    addresses_text = "\n".join(addresses)
                    st.download_button(
                        label="📄 Download TXT",
                        data=addresses_text,
                        file_name=f"unique_addresses_{timestamp}.txt",
                        mime="text/plain"
                    )

                st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.warning("⚠️ No addresses found or an error occurred")

if __name__ == "__main__":
    main()