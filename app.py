import streamlit as st
from main import run_crew_pipeline
from agents.product_agent import fetch_mock_products
import random

# -------------- Setup Page ------------------
st.set_page_config(
    page_title="DesignAlchemy",
    layout="wide",
    initial_sidebar_state="expanded",
    page_icon="🛋️"
)

# -------------- Custom CSS ------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 3rem 2rem;
        border-radius: 0 0 20px 20px;
        margin-bottom: 2rem;
        color: white;
        text-align: center;
    }
    
    .feature-card {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 16px;
        padding: 1.5rem;
        margin: 0.5rem 0;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    .product-card {
        background: white;
        border-radius: 16px;
        padding: 1rem;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        height: 100%;
        border: 1px solid rgba(0, 0, 0, 0.05);
    }
    
    .product-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.12);
    }
    
    .budget-badge {
        background: linear-gradient(135deg, #00b09b, #96c93d);
        color: white;
        padding: 0.3rem 1rem;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.8rem;
    }
    
    .style-badge {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        padding: 0.3rem 1rem;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.8rem;
    }
    
    .generate-btn {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        border: none;
        padding: 1rem 2rem;
        border-radius: 12px;
        font-weight: 600;
        font-size: 1.1rem;
        width: 100%;
        transition: all 0.3s ease;
    }
    
    .generate-btn:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3);
    }
    
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #f8f9fa 0%, #e9ecef 100%);
    }
    
    .dark-mode {
        background: #0f0f0f;
        color: white;
    }
    
    .dark-mode .product-card {
        background: #1e1e1e;
        color: white;
        border: 1px solid #333;
    }
    
    .progress-bar {
        height: 6px;
        background: linear-gradient(90deg, #667eea, #764ba2);
        border-radius: 3px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# -------------- Theme Toggle ----------------
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False

# -------------- Header ------------------
st.markdown("""
<div class="main-header">
    <h1 style="margin:0; font-size: 3rem; font-weight: 700;">🛋️ DesignAlchemy AI</h1>
    <p style="font-size: 1.2rem; opacity: 0.9; margin: 0.5rem 0 0 0;">
        Transform your space with AI-powered interior design recommendations
    </p>
</div>
""", unsafe_allow_html=True)

# -------------- Sidebar ------------------
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; margin-bottom: 2rem;">
        <h2 style="color: #667eea; margin-bottom: 0.5rem;">🎨 Design Preferences</h2>
        <p style="color: #666; font-size: 0.9rem;">Customize your perfect space</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Room Selection with Icons
    room_options = {
        "bedroom": "🛏️ Bedroom",
        "living room": "🛋️ Living Room", 
        "study room": "📚 Study Room",
        "dining room": "🍽️ Dining Room"
    }
    room = st.selectbox("Room Type", list(room_options.keys()), 
                       format_func=lambda x: room_options[x])
    
    # Style Selection
    style_emojis = {
        "boho": "🌿", "modern": "⚡", "minimalist": "⬜", 
        "scandinavian": "❄️", "vintage": "📻", "japanese style": "🎎"
    }
    style = st.selectbox("Design Style", list(style_emojis.keys()),
                        format_func=lambda x: f"{style_emojis[x]} {x.title()}")
    
    # Budget with visual indicator
    st.markdown("**Budget Range**")
    budget = st.slider("", 500, 100000, 2000, step=500, label_visibility="collapsed")
    
    # Budget progress visualization
    budget_percentage = min((budget / 100000) * 100, 100)
    st.markdown(f"""
    <div style="display: flex; justify-content: space-between; font-size: 0.8rem; color: #666;">
        <span>₹500</span>
        <span>₹{budget:,}</span>
        <span>₹100,000</span>
    </div>
    <div class="progress-bar" style="width: {budget_percentage}%;"></div>
    """, unsafe_allow_html=True)
    
    # Generate Button
    generate = st.button("✨ Generate Design Plan", use_container_width=True, 
                        type="primary")
    
    # Theme Toggle at bottom
    st.markdown("---")
    dark_mode = st.toggle("🌙 Dark Mode", value=st.session_state.dark_mode)
    st.session_state.dark_mode = dark_mode

# Apply dark mode
if st.session_state.dark_mode:
    st.markdown("""
    <style>
        .main, .css-1d391kg, .css-1r6slb0 {
            background-color: #0f0f0f;
            color: white;
        }
        .main-header {
            background: linear-gradient(135deg, #2d3748 0%, #4a5568 100%);
        }
    </style>
    """, unsafe_allow_html=True)

# -------------- Utility Functions ----------
def chunk_list(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

def display_product_grid(products, title, subtitle, chunk_size=3, start=0, end=None):
    st.markdown(f"""
    <div style="margin: 2rem 0 1rem 0;">
        <h3 style="margin: 0; color: {'white' if st.session_state.dark_mode else '#2d3748'};">{title}</h3>
        <p style="margin: 0.3rem 0 1rem 0; color: #666; font-size: 0.9rem;">{subtitle}</p>
    </div>
    """, unsafe_allow_html=True)
    
    visible_products = products[start:end]
    for chunk in chunk_list(visible_products, chunk_size):
        cols = st.columns(chunk_size)
        for col, item in zip(cols, chunk):
            with col:
                card_bg = "#1e1e1e" if st.session_state.dark_mode else "white"
                text_color = "white" if st.session_state.dark_mode else "#2d3748"
                border_color = "#333" if st.session_state.dark_mode else "rgba(0,0,0,0.05)"
                
                st.markdown(f"""
                <div class="product-card" style="background: {card_bg}; color: {text_color}; border-color: {border_color};">
                    <div style="position: relative;">
                        <img src="{item['image']}" style="width: 100%; height: 180px; object-fit: cover; border-radius: 12px; margin-bottom: 1rem;" />
                        <div style="position: absolute; top: 10px; right: 10px; background: rgba(0,0,0,0.7); color: white; padding: 0.3rem 0.6rem; border-radius: 20px; font-size: 0.8rem; font-weight: 600;">
                            ₹{item['price']:,}
                        </div>
                    </div>
                    <h4 style="margin: 0.5rem 0; font-size: 1rem; font-weight: 600;">{item['name']}</h4>
                    <p style="font-size: 0.85rem; color: {'#ccc' if st.session_state.dark_mode else '#666'}; line-height: 1.4; margin-bottom: 1rem;">
                        {item['description']}
                    </p>
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-top: auto;">
                        <span style="background: {'#333' if st.session_state.dark_mode else '#f1f3f4'}; color: {'#ccc' if st.session_state.dark_mode else '#666'}; padding: 0.2rem 0.6rem; border-radius: 12px; font-size: 0.7rem;">
                            {random.choice(['🛋️ Furniture', '💡 Lighting', '🎨 Decor', '📐 Essential'])}
                        </span>
                        <button style="background: #667eea; color: white; border: none; padding: 0.3rem 0.8rem; border-radius: 8px; font-size: 0.8rem; cursor: pointer;">
                            Add to Cart
                        </button>
                    </div>
                </div>
                """, unsafe_allow_html=True)

# -------------- Main Content ---------------
if generate:
    with st.spinner("🎨 Designing your perfect space..."):
        # Simulate loading with progress
        progress_bar = st.progress(0)
        for i in range(100):
            # Simulate processing time
            import time
            time.sleep(0.02)
            progress_bar.progress(i + 1)
        
        design_plan = run_crew_pipeline(room, style, budget)
        all_products = fetch_mock_products()

        # Categorize products
        within_budget = []
        above_budget = []
        total_cost = 0

        for p in all_products:
            if total_cost + p["price"] <= budget:
                within_budget.append(p)
                total_cost += p["price"]
            else:
                above_budget.append(p)

        st.session_state.within = within_budget
        st.session_state.above = above_budget
        st.session_state.load_count = 1

        # Success message
        st.success(f"✅ Successfully created your {style} {room} design plan!")

# -------------- Results Display -------------
if "within" in st.session_state:
    chunk = 3
    step = chunk * 2
    
    # Header with stats
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""
        <div style="text-align: center; padding: 1rem; background: {'#1e1e1e' if st.session_state.dark_mode else '#f8f9fa'}; border-radius: 12px;">
            <h3 style="margin: 0; color: {'white' if st.session_state.dark_mode else '#2d3748'};">{len(st.session_state.within)}</h3>
            <p style="margin: 0; color: #666; font-size: 0.9rem;">Recommended Items</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        total_cost = sum([p['price'] for p in st.session_state.within])
        st.markdown(f"""
        <div style="text-align: center; padding: 1rem; background: {'#1e1e1e' if st.session_state.dark_mode else '#f8f9fa'}; border-radius: 12px;">
            <h3 style="margin: 0; color: {'white' if st.session_state.dark_mode else '#2d3748'};">₹{total_cost:,}</h3>
            <p style="margin: 0; color: #666; font-size: 0.9rem;">Total Cost</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        savings = budget - total_cost
        st.markdown(f"""
        <div style="text-align: center; padding: 1rem; background: {'#1e1e1e' if st.session_state.dark_mode else '#f8f9fa'}; border-radius: 12px;">
            <h3 style="margin: 0; color: #00b09b;">₹{savings:,}</h3>
            <p style="margin: 0; color: #666; font-size: 0.9rem;">Under Budget</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Products within budget
    end_index = step * st.session_state.load_count
    display_product_grid(
        st.session_state.within, 
        "🎯 Perfect Picks Within Your Budget",
        f"Curated selection matching your {style} style for {room}",
        chunk_size=chunk, 
        end=end_index
    )
    
    # Load more button
    if len(st.session_state.within) > end_index:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("📦 Load More Products", use_container_width=True):
                st.session_state.load_count += 1
                st.rerun()
    
    # Above budget section
    if st.session_state.above:
        st.markdown("---")
        display_product_grid(
            st.session_state.above,
            "💎 Premium Upgrades",
            "Elevate your space with these premium selections",
            chunk_size=chunk,
            end=min(step, len(st.session_state.above))
        )
    
    # Design rationale
    st.markdown("---")
    st.markdown("""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 2rem; border-radius: 16px; margin-top: 2rem;">
        <h3 style="margin: 0 0 1rem 0; color: white;">🎨 Design Philosophy</h3>
        <p style="margin: 0; opacity: 0.9; line-height: 1.6;">
        These items were carefully selected to create a harmonious {style} aesthetic in your {room}, 
        balancing functionality with style while respecting your budget constraints. Each piece contributes 
        to a cohesive design narrative that transforms your space into a personalized sanctuary.
        </p>
    </div>
    """.format(style=style, room=room), unsafe_allow_html=True)

else:
    # Welcome state
    st.markdown("""
    <div style="text-align: center; padding: 4rem 2rem; color: #666;">
        <h2 style="color: #2d3748; margin-bottom: 1rem;">🚀 Ready to Transform Your Space?</h2>
        <p style="font-size: 1.1rem; max-width: 600px; margin: 0 auto 2rem auto; line-height: 1.6;">
        Tell us about your room preferences and budget, and our AI will create a personalized 
        design plan with product recommendations tailored just for you.
        </p>
        <div style="font-size: 3rem; margin: 2rem 0;">✨</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Features grid
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div class="feature-card">
            <h4>🎯 Smart Matching</h4>
            <p>AI-powered recommendations based on your style and budget</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <h4>💰 Budget Optimized</h4>
            <p>Get the most value without compromising on style</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="feature-card">
            <h4>🎨 Style Cohesive</h4>
            <p>All items work together for a unified look</p>
        </div>
        """, unsafe_allow_html=True)

# -------------- Footer ------------------
st.markdown("""
<div style="text-align: center; margin-top: 4rem; padding: 2rem; color: #666; border-top: 1px solid #e0e0e0;">
    <p>Made with ❤️ using DesignGenius AI • Your personal interior design assistant</p>
</div>
""", unsafe_allow_html=True)