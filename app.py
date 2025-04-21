import streamlit as st
from PIL import Image
import io
import base64
import os
import random

# ----------------- Constants -----------------
IMAGE_PATHS = {
    "gallery": [
        "images/image2.jpg",
        "images/image3.jpg",
        "images/image4.jpg",
        "images/image5.jpg",
        "images/image6.jpg",
        "images/image8.jpg",
        "images/image10.jpg",
        "images/image1.jpg",
        "images/image11.jpg"
    ],
    "memory": [
        "images/image5.jpg",
        "images/image2.jpg",
        "images/image9.jpg"
    ],
    "gift": "images/image7.jpg",
    "puzzle": "images/image9.jpg",
    "cake": {
        "classic": "images/cake/classic.jpg",
        "chocolate": "images/cake/chocolate.jpg",
        "strawberry": "images/cake/strawberry.jpg"
    }
}


# ----------------- Helper Functions -----------------
def image_to_base64(image):
    """Convert PIL image to base64 string"""
    buffered = io.BytesIO()
    image.save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue()).decode()

def verify_image_paths():
    """Check if all required images exist"""
    missing = []
    for key, paths in IMAGE_PATHS.items():
        if key in ["gallery", "memory"]:
            for path in paths:
                if not os.path.exists(path):
                    missing.append(path)
        elif key == "cake":
            for path in paths.values():
                if not os.path.exists(path):
                    missing.append(path)
        else:
            if not os.path.exists(paths):
                missing.append(paths)
    return missing

# ----------------- Configuration -----------------
st.set_page_config(
    page_title="Happy Birthday Vyshnavi!", 
    page_icon="🦋",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'current_page' not in st.session_state:
    st.session_state.current_page = "gallery"
if 'gift_opened' not in st.session_state:
    st.session_state.gift_opened = False
if 'puzzle_complete' not in st.session_state:
    st.session_state.puzzle_complete = False
if 'puzzle_pieces' not in st.session_state:
    # Create a shuffled list of positions for the puzzle
    positions = [(x, y) for y in [0, 50, 100] for x in [0, 50, 100]]
    random.shuffle(positions)
    st.session_state.puzzle_pieces = positions
if 'selected_piece' not in st.session_state:
    st.session_state.selected_piece = None
if 'selected_cake' not in st.session_state:
    st.session_state.selected_cake = 'classic'

# ----------------- CSS -----------------
def load_css():
    st.markdown("""
        <style>
            :root {
                --primary: #ff6b9e;
                --secondary: #ff8fab;
                --accent: #ffb3c6;
                --light: #ffffff;
                --dark: #590d22;
                --success: #4CAF50;
                --warning: #FFC107;
                --danger: #F44336;
                --info: #2196F3;
            }
            
            body {
                font-family: 'Poppins', sans-serif;
                background-color: #fff0f5; /* Baby pink background */
                color: var(--dark);
                overflow-x: hidden;
            }
            
            .stApp {
                background: #fff0f5; /* Baby pink background */
            }
            
            /* Floating Birthday Title */
            .birthday-title {
                font-size: 4rem;
                font-weight: 800;
                background: linear-gradient(135deg, #ff006e, #ff8fab);
                -webkit-background-clip: text;
                background-clip: text;
                color: transparent;
                text-align: center;
                margin: 2rem 0;
                animation: float 3s ease-in-out infinite;
                text-shadow: 0 0 10px rgba(255,107,158,0.3);
                position: relative;
                z-index: 100;
            }
            
            @keyframes float {
                0% { transform: translateY(0px); }
                50% { transform: translateY(-20px); }
                100% { transform: translateY(0px); }
            }
            
            .butterfly {
                position: absolute;
                font-size: 2rem;
                animation: fly 15s linear infinite;
                opacity: 0.8;
                z-index: 50;
            }
            
            @keyframes fly {
                0% { transform: translateX(-100px) translateY(0px) rotate(0deg); }
                25% { transform: translateX(25vw) translateY(-50px) rotate(10deg); }
                50% { transform: translateX(50vw) translateY(0px) rotate(0deg); }
                75% { transform: translateX(75vw) translateY(-50px) rotate(-10deg); }
                100% { transform: translateX(100vw) translateY(0px) rotate(0deg); }
            }
            
            /* Profile Card Styles */
            .profile-card {
                background: white;
                border-radius: 15px;
                padding: 2rem;
                box-shadow: 0 10px 30px rgba(0,0,0,0.1);
                text-align: center;
                margin: 2rem auto;
                max-width: 400px;
                transition: all 0.3s ease;
            }
            
            .profile-card:hover {
                transform: translateY(-5px);
                box-shadow: 0 15px 40px rgba(0,0,0,0.15);
            }
            
            .profile-icon {
                font-size: 4rem;
                margin-bottom: 1rem;
                color: var(--primary);
            }
            
            .profile-name {
                font-size: 2rem;
                font-weight: 700;
                margin-bottom: 0.5rem;
                color: var(--dark);
            }
            
            .profile-title {
                font-size: 1.2rem;
                color: var(--secondary);
                margin-bottom: 1.5rem;
            }
            
            .profile-details {
                display: flex;
                justify-content: space-between;
                margin-top: 1.5rem;
            }
            
            .detail-item {
                flex: 1;
                padding: 0.5rem;
            }
            
            .detail-label {
                font-size: 0.9rem;
                color: var(--secondary);
                margin-bottom: 0.3rem;
            }
            
            .detail-value {
                font-size: 1.1rem;
                font-weight: 600;
                color: var(--dark);
            }
            
            /* Improved button styles */
            .nav-tab {
                padding: 0.8rem 1.5rem;
                border-radius: 30px;
                background: white;
                color: var(--dark);
                font-weight: 800; /* CHANGED: Made buttons bold */
                cursor: pointer;
                transition: all 0.3s ease;
                box-shadow: 0 4px 15px rgba(0,0,0,0.1);
                border: none;
                outline: none;
                font-size: 1rem;
                text-align: center;
                display: block;
                width: 100%;
                margin-bottom: 0.5rem;
                font-family: 'Poppins', sans-serif; /* CHANGED: Added font */
            }
            
            .nav-tab:hover {
                transform: translateY(-3px);
                box-shadow: 0 6px 20px rgba(0,0,0,0.15);
            }
            
            .nav-tab.active {
                background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
                color: white;
                box-shadow: 0 6px 20px rgba(255,107,158,0.4);
            }
            
            /* Sidebar button styling */
            .stButton button {
                border-radius: 30px !important;
                font-weight: 800 !important; /* CHANGED: Made buttons bold */
                transition: all 0.3s ease !important;
                box-shadow: 0 4px 15px rgba(0,0,0,0.1) !important;
                border: none !important;
                font-family: 'Poppins', sans-serif !important; /* CHANGED: Added font */
            }
            
            .stButton button:hover {
                transform: translateY(-3px) !important;
                box-shadow: 0 6px 20px rgba(0,0,0,0.15) !important;
            }
            
            /* Gallery Styles */
            .gallery {
                display: flex;
                flex-wrap: wrap;
                justify-content: center;
                gap: 2rem;
                margin: 2rem auto;
                max-width: 1200px;
            }
            
            .gallery-item {
                width: 300px;
                height: 300px;
                perspective: 1000px;
                cursor: pointer;
            }
            
            .gallery-item-inner {
                width: 100%;
                height: 100%;
                border-radius: 15px;
                box-shadow: 0 10px 20px rgba(0,0,0,0.1);
                overflow: hidden;
                transition: all 0.5s ease;
            }
            
            .gallery-item:hover .gallery-item-inner {
                transform: scale(1.05) rotate(2deg);
                box-shadow: 0 15px 30px rgba(0,0,0,0.2);
            }
            
            /* Memory Lane Styles */
            .memory-container {
                display: flex;
                flex-direction: column;
                align-items: center;
                max-width: 800px;
                margin: 0 auto;
                padding: 2rem;
                background-color: white;
                border-radius: 20px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            }
            
            .memory-item {
                margin: 2rem 0;
                width: 100%;
                display: flex;
                flex-direction: column;
                align-items: center;
            }
            
            .memory-image {
                width: 100%;
                max-width: 500px;
                border-radius: 15px;
                box-shadow: 0 5px 15px rgba(0,0,0,0.1);
                transition: transform 0.5s ease;
            }
            
            .memory-image:hover {
                transform: scale(1.03);
            }
            
            /* Gift Box Styles - Fixed for proper opening */
            .gift-box-container {
                perspective: 1000px;
                width: 300px;
                height: 300px;
                margin: 3rem auto;
            }
            
            .gift-box {
                width: 100%;
                height: 100%;
                position: relative;
                transform-style: preserve-3d;
                transition: transform 0.8s ease;
                cursor: pointer;
            }
            
            .gift-box.opened {
                transform: rotateY(180deg);
            }
            
            .gift-box-front, .gift-box-back {
                position: absolute;
                width: 100%;
                height: 100%;
                backface-visibility: hidden;
                border-radius: 15px;
                display: flex;
                align-items: center;
                justify-content: center;
                box-shadow: 0 15px 35px rgba(0,0,0,0.2);
            }
            
            .gift-box-front {
                background: linear-gradient(45deg, var(--primary), var(--secondary));
                animation: pulse 2s infinite alternate;
            }
            
            @keyframes pulse {
                from { transform: scale(1); }
                to { transform: scale(1.05); }
            }
            
            .gift-box-back {
                background: white;
                transform: rotateY(180deg);
                padding: 20px;
                flex-direction: column;
            }
            
            /* Puzzle Game Styles */
            .puzzle-container {
                display: grid;
                grid-template-columns: repeat(3, 1fr);
                gap: 5px;
                max-width: 500px;
                margin: 2rem auto;
            }
            
            .puzzle-piece {
                aspect-ratio: 1;
                background-size: 300% 300%;
                background-repeat: no-repeat;
                border-radius: 8px;
                cursor: pointer;
                transition: all 0.3s ease;
                box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            }
            
            .puzzle-piece:hover {
                transform: scale(1.05);
                box-shadow: 0 8px 20px rgba(0,0,0,0.15);
            }
            
            .puzzle-piece.selected {
                border: 3px solid var(--primary);
                box-shadow: 0 0 15px var(--primary);
            }
            
            /* Cake Designer Styles */
            .cake-option {
                display: flex;
                flex-direction: column;
                align-items: center;
                gap: 0.5rem;
                padding: 10px;
                border-radius: 10px;
                transition: all 0.3s ease;
                cursor: pointer;
            }
            
            .cake-option:hover {
                background-color: var(--light);
                transform: scale(1.05);
            }
            
            .cake-result {
                padding: 2rem;
                border-radius: 15px;
                background-color: white;
                box-shadow: 0 10px 30px rgba(0,0,0,0.1);
                transition: all 0.5s ease;
            }
            
            .cake-result:hover {
                transform: scale(1.03);
                box-shadow: 0 15px 40px rgba(0,0,0,0.15);
            }
            
            .birthday-message {
                background: linear-gradient(135deg, #ffb3c6, #ff8fab);
                padding: 2rem;
                border-radius: 15px;
                color: white;
                text-align: center;
                margin-top: 1rem;
                box-shadow: 0 10px 20px rgba(0,0,0,0.1);
            }
            
            /* Confetti Animation */
            @keyframes confetti-fall {
                0% { transform: translateY(-100vh) rotate(0deg); }
                100% { transform: translateY(100vh) rotate(360deg); }
            }
            
            .confetti {
                position: fixed;
                width: 10px;
                height: 10px;
                border-radius: 50%;
                animation: confetti-fall 5s linear infinite;
                z-index: 999;
            }
            
            /* Magic Dust Particles */
            .magic-dust {
                position: fixed;
                width: 5px;
                height: 5px;
                border-radius: 50%;
                background: gold;
                opacity: 0;
                z-index: 999;
                animation: magic-dust-fall 5s linear infinite;
            }
            
            @keyframes magic-dust-fall {
                0% { transform: translateY(-100vh) rotate(0deg); opacity: 0.8; }
                100% { transform: translateY(100vh) rotate(360deg); opacity: 0; }
            }
            
            /* Disney Castle Silhouette */
            .disney-castle {
                position: fixed;
                bottom: 0;
                left: 50%;
                transform: translateX(-50%);
                font-size: 10rem;
                z-index: -1;
                opacity: 0.1;
                animation: twinkle 3s ease-in-out infinite alternate;
            }
            
            @keyframes twinkle {
                0% { opacity: 0.1; }
                100% { opacity: 0.2; }
            }
            
            /* CHANGED: Added new style for section headers */
            .section-header {
                text-align: center;
                font-weight: 800;
                font-family: 'Poppins', sans-serif;
                margin-bottom: 1.5rem;
            }
            
            /* CHANGED: Added styling for cake options */
            .cake-option-text {
                font-weight: 800;
                font-family: 'Poppins', sans-serif;
            }
        </style>
        
        <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700&display=swap" rel="stylesheet">
        <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    """, unsafe_allow_html=True)

# ----------------- Page Components -----------------
def show_header():
    st.markdown("""
        <div style="position: relative;">
            <div class="birthday-title">HAPPY BIRTHDAY VYSHNAVI</div>
            <div class="butterfly" style="top: -20px; left: 10%; animation-delay: 0s;">🦋</div>
            <div class="butterfly" style="top: 50px; left: 30%; animation-delay: 2s;">🦋</div>
            <div class="butterfly" style="top: -10px; left: 70%; animation-delay: 4s;">🦋</div>
            <div class="butterfly" style="top: 60px; left: 90%; animation-delay: 6s;">🦋</div>
        </div>
    """, unsafe_allow_html=True)

def create_sidebar():
    with st.sidebar:
        st.markdown("""
            <div style="text-align: center; margin-bottom: 2rem;">
                <h2>Birthday Celebration</h2>
                <p>Navigate through your birthday surprises!</p>
            </div>
        """, unsafe_allow_html=True)
        
        pages = {
            "gallery": "🖼️ Photo Gallery",
            "memory": "🌟 Memory Lane",
            "gift": "🎁 Virtual Gift",
            "puzzle": "🧩 Photo Puzzle",
            "cake": "🎂 Cake Designer"
        }
        
        # Apply custom styling to buttons
        for page_id, page_name in pages.items():
            button_class = "active" if st.session_state.current_page == page_id else ""
            if st.button(page_name, key=f"{page_id}_btn", 
                        use_container_width=True,
                        type="primary" if st.session_state.current_page == page_id else "secondary"):
                st.session_state.current_page = page_id
                st.rerun()

def show_gallery():
    # CHANGED: Updated heading to use centered, bold styling
    st.markdown("<h2 class='section-header'>Photo Gallery</h2>", unsafe_allow_html=True)
    st.markdown("<div class='gallery'>", unsafe_allow_html=True)
    cols = st.columns(3)
    for i, path in enumerate(IMAGE_PATHS["gallery"]):
        with cols[i % 3]:
            try:
                image = Image.open(path)
                st.markdown(f"""
                    <div class="gallery-item">
                        <div class="gallery-item-inner">
                            <img src="data:image/jpeg;base64,{image_to_base64(image)}" style="width:100%; height:100%; object-fit:cover;">
                        </div>
                    </div>
                """, unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Error loading image: {e}")
    st.markdown("</div>", unsafe_allow_html=True)

def show_memory_lane():
    # CHANGED: Updated heading to use centered, bold styling
    st.markdown("<h2 class='section-header'>Memory Lane</h2>", unsafe_allow_html=True)
    
    st.markdown("<div class='memory-container'>", unsafe_allow_html=True)
    
    for i, path in enumerate(IMAGE_PATHS["memory"]):
        try:
            image = Image.open(path)
            st.markdown(f"""
                <div class="memory-item">
                    <img src="data:image/jpeg;base64,{image_to_base64(image)}" class="memory-image">
                </div>
            """, unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Error loading memory image: {e}")
    
    st.markdown("</div>", unsafe_allow_html=True)

def show_gift_box():
    # CHANGED: Updated heading to use centered, bold styling
    st.markdown("<h2 class='section-header'>Your Special Gift</h2>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        # Gift box HTML with fixed event handling
        gift_box_class = "opened" if st.session_state.gift_opened else ""
        gift_image = image_to_base64(Image.open(IMAGE_PATHS['gift']))
        
        st.markdown(f"""
            <div class="gift-box-container">
                <div class="gift-box {gift_box_class}" onclick="this.classList.toggle('opened')">
                    <div class="gift-box-front">
                        <div style="text-align: center;">
                            <div style="font-size: 5rem;">🎁</div>
                            <p style="margin-top: 1rem; color: white;">Click to open!</p>
                        </div>
                    </div>
                    <div class="gift-box-back" style="display: flex; justify-content: center; align-items: center; height: 100%;">
                        <img src="data:image/jpeg;base64,{gift_image}" 
                             style="width: 100%; height: 100%; object-fit: contain; border-radius:10px;">
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        # Button to toggle gift box state
        if st.button("Open/Close Gift", use_container_width=True):
            st.session_state.gift_opened = not st.session_state.gift_opened
            st.rerun()

def show_puzzle_game():
    # CHANGED: Updated heading to use centered, bold styling
    st.markdown("<h2 class='section-header'>Photo Puzzle Challenge</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Click on two pieces to swap them. Try to arrange the image correctly!</p>", unsafe_allow_html=True)
    
    # Create the puzzle board
    cols = st.columns(3)
    for i in range(9):
        x, y = st.session_state.puzzle_pieces[i]
        with cols[i % 3]:
            # Create a button for each puzzle piece
            if st.button(f"Piece {i+1}", key=f"puzzle_{i}", use_container_width=True):
                # Handle piece selection
                if st.session_state.selected_piece is None:
                    st.session_state.selected_piece = i
                else:
                    # Swap the selected pieces
                    idx1 = st.session_state.selected_piece
                    idx2 = i
                    st.session_state.puzzle_pieces[idx1], st.session_state.puzzle_pieces[idx2] = \
                        st.session_state.puzzle_pieces[idx2], st.session_state.puzzle_pieces[idx1]
                    st.session_state.selected_piece = None
                st.rerun()
            
            # Display the puzzle piece
            try:
                bg_img = image_to_base64(Image.open(IMAGE_PATHS['puzzle']))
                st.markdown(f"""
                    <div class="puzzle-piece {'selected' if st.session_state.selected_piece == i else ''}" 
                         style="background-image: url('data:image/jpeg;base64,{bg_img}'); 
                                background-position: {x}% {y}%;">
                    </div>
                """, unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Error loading puzzle image: {e}")
    
    # Check if puzzle is complete
    original_positions = [(x, y) for y in [0, 50, 100] for x in [0, 50, 100]]
    if st.session_state.puzzle_pieces == original_positions:
        st.session_state.puzzle_complete = True
    
    # Show congratulations message if puzzle is complete
    if st.session_state.puzzle_complete:
        st.balloons()
        st.markdown("""
            <div style="text-align: center; margin-top: 2rem; padding: 1rem; background-color: var(--light); border-radius: 10px;">
                <h3>🎉 Congratulations! 🎉</h3>
                <p>You completed the puzzle! You're amazing!</p>
            </div>
        """, unsafe_allow_html=True)
    
    # Reset button
    if st.button("Reset Puzzle", use_container_width=True):
        positions = [(x, y) for y in [0, 50, 100] for x in [0, 50, 100]]
        random.shuffle(positions)
        st.session_state.puzzle_pieces = positions
        st.session_state.selected_piece = None
        st.session_state.puzzle_complete = False
        st.rerun()

def show_cake_decorator():
    # CHANGED: Updated heading to use centered, bold styling
    st.markdown("<h2 class='section-header'>Design Your Birthday Cake</h2>", unsafe_allow_html=True)
    
    # Profile card
    st.markdown("""
        <div class="profile-card">
            <div class="profile-icon">🦋</div>
            <div class="profile-name">Vyshnavi</div>
            <div class="profile-title">Birthday Girl</div>
            <div class="profile-details">
                <div class="detail-item">
                    <div class="detail-label">Birthday:</div>
                    <div class="detail-value">Today!</div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("<div class='cake-result'>", unsafe_allow_html=True)
        try:
            selected_cake_path = IMAGE_PATHS['cake'][st.session_state.selected_cake]
            st.image(Image.open(selected_cake_path), caption="Your Custom Birthday Cake", use_container_width=True)
            
            # Birthday message in a styled box
            st.markdown("""
                <div class="birthday-message">
                    <h3>🎉 Happy Birthday Vyshnavi! 🎉</h3>
                </div>
            """, unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Error loading cake image: {e}")
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        # CHANGED: Updated heading to use the same bold, Poppins font
        st.markdown("<h3 style='font-weight: 800; font-family: \"Poppins\", sans-serif;'>Choose Your Flavor</h3>", unsafe_allow_html=True)
        
        cake_options = list(IMAGE_PATHS['cake'].keys())
        for cake_type in cake_options:
            # CHANGED: Using the cake-option-text class for bold text
            if st.button(f"{cake_type.capitalize()} Cake", key=f"cake_{cake_type}", use_container_width=True):
                st.session_state.selected_cake = cake_type
                st.rerun()

# ----------------- Main App -----------------
def main():
    # Verify all images exist
    missing_images = verify_image_paths()
    if missing_images:
        st.error(f"Missing images: {', '.join(missing_images)}")
        return

    load_css()
    show_header()
    create_sidebar()
    
    if st.session_state.current_page == "gallery":
        show_gallery()
    elif st.session_state.current_page == "memory":
        show_memory_lane()
    elif st.session_state.current_page == "gift":
        show_gift_box()
    elif st.session_state.current_page == "puzzle":
        show_puzzle_game()
    elif st.session_state.current_page == "cake":
        show_cake_decorator()

if __name__ == "__main__":
    main()