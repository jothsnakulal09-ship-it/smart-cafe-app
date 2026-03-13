import streamlit as st
import pandas as pd
import os
import base64
from datetime import datetime
import random

# Set page config
st.set_page_config(
    page_title="Smart Café",
    page_icon="☕",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    /* Home page special background */
    [data-testid="stAppViewContainer"]:has(.home-page-marker) {
        background: linear-gradient(135deg, #F5F0E6 0%, #D8C3A5 100%);
    }

    .home-header {
        font-size: 3rem;
        font-weight: 800;
        color: #4A3B32;
        text-align: center;
        margin-bottom: 1rem;
        padding-top: 2rem;
    }
    .home-subtitle {
        text-align: center;
        color: #6B5B52;
        font-size: 1.2rem;
        margin-bottom: 3rem;
    }

    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #8B5E3C;
        text-align: center;
        margin-bottom: 2rem;
    }
    .menu-card {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
        border: 1px solid #e9ecef;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .order-card {
        background-color: #fff3cd;
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
        border: 1px solid #ffeaa7;
    }
    .status-preparing {
        background-color: #fff3cd;
        color: #856404;
        padding: 0.25rem 0.5rem;
        border-radius: 5px;
        font-weight: bold;
    }
    .status-ready {
        background-color: #d1ecf1;
        color: #0c5460;
        padding: 0.25rem 0.5rem;
        border-radius: 5px;
        font-weight: bold;
    }
    .status-completed {
        background-color: #d4edda;
        color: #155724;
        padding: 0.25rem 0.5rem;
        border-radius: 5px;
        font-weight: bold;
    }
    .sidebar-nav {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
    }
    .menu-card {
        position: relative;
        background-color: #f8f9fa;
        border-radius: 10px;
        margin: 0.5rem 0;
        border: 1px solid #e9ecef;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        overflow: hidden;
    }
    .menu-card img {
        width: 100%;
        display: block;
        border-radius: 10px 10px 0 0;
    }
    .menu-card-overlay {
        position: absolute;
        bottom: 0;
        left: 0;
        right: 0;
        background: rgba(0, 0, 0, 0.6);
        color: white;
        padding: 0.5rem;
        text-align: center;
    }
    .menu-card-overlay h4 {
        margin: 0;
        font-size: 1.1rem;
    }
    .menu-card-overlay p {
        margin: 0;
        font-size: 0.9rem;
    }
    .add-btn-container {
        padding: 0.5rem;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# Menu data
MENU = {
    "Coffee": [
        {"name": "Espresso", "price": 3.50, "image": "https://images.unsplash.com/photo-1510591509098-f4fdc6d0ff04?w=200&h=150&fit=crop"},
        {"name": "Cappuccino", "price": 4.50, "image": "https://images.unsplash.com/photo-1534778101976-62847782c213?w=200&h=150&fit=crop"},
        {"name": "Latte", "price": 4.00, "image": "https://images.unsplash.com/photo-1461023058943-07fcbe16d735?w=200&h=150&fit=crop"},
        {"name": "Americano", "price": 3.00, "image": "https://images.unsplash.com/photo-1559056199-641a0ac8b55e?w=200&h=150&fit=crop"},
        {"name": "Mocha", "price": 4.75, "image": "https://images.unsplash.com/photo-1620050860361-ec8802958742?w=200&h=150&fit=crop"},
        {"name": "Macchiato", "price": 4.25, "image": "https://images.unsplash.com/photo-1559496417-e7f25cb247f3?w=200&h=150&fit=crop"}
    ],
    "Tea": [
        {"name": "Green Tea", "price": 3.00, "image": "imges/green tea.jpeg"},
        {"name": "Earl Grey", "price": 3.50, "image": "imges/eral tea.jpeg"},
        {"name": "Chamomile", "price": 3.25, "image": "https://images.unsplash.com/photo-1576092762793-48d4d7c41c3f?w=200&h=150&fit=crop"},
        {"name": "Black Tea", "price": 3.00, "image": "https://images.unsplash.com/photo-1544787219-7f47ccb76574?w=200&h=150&fit=crop"}
    ],
    "Snacks": [
        {"name": "Croissant", "price": 2.50, "image": "https://images.unsplash.com/photo-1555507036-ab1f4038808a?w=200&h=150&fit=crop"},
        {"name": "Muffin", "price": 3.00, "image": "https://images.unsplash.com/photo-1587668178277-295251f900ce?w=200&h=150&fit=crop"},
        {"name": "Bagel", "price": 2.75, "image": "https://images.unsplash.com/photo-1627308595186-6b1c78a16847?w=200&h=150&fit=crop"},
        {"name": "Sandwich", "price": 5.50, "image": "https://images.unsplash.com/photo-1481070414801-51b21dc96594?w=200&h=150&fit=crop"}
    ],
    "Desserts": [
        {"name": "Cheesecake", "price": 5.00, "image": "https://images.unsplash.com/photo-1533134242443-d4fd215305ad?w=200&h=150&fit=crop"},
        {"name": "Brownie", "price": 4.00, "image": "https://images.unsplash.com/photo-1464305795204-6f5bbfc7fb81?w=200&h=150&fit=crop"},
        {"name": "Tiramisu", "price": 5.50, "image": "https://images.unsplash.com/photo-1571877227200-a0d98ea607e9?w=200&h=150&fit=crop"},
        {"name": "Ice Cream", "price": 3.50, "image": "https://images.unsplash.com/photo-1567206563064-6f60f40a2b57?w=200&h=150&fit=crop"}
    ]
}

# Today's Special
TODAYS_SPECIAL = {
    "name": "Caramel Macchiato",
    "price": 5.50,
    "image": "https://images.unsplash.com/photo-1485808191679-5f86510681a2?w=400&h=300&fit=crop",
    "description": "Our signature espresso with steamed milk and a drizzle of sweet caramel sauce."
}

# File paths
ORDERS_FILE = "orders.csv"

# Initialize session state
if 'cart' not in st.session_state:
    st.session_state.cart = []
if 'customer_name' not in st.session_state:
    st.session_state.customer_name = ""
if 'table_number' not in st.session_state:
    st.session_state.table_number = ""
if 'order_placed' not in st.session_state:
    st.session_state.order_placed = False
if 'current_order_id' not in st.session_state:
    st.session_state.current_order_id = None
if 'page' not in st.session_state:
    st.session_state.page = "Home"

def change_page(new_page):
    st.session_state.page = new_page

# Functions
def get_image_src(image_path):
    """Convert local image path to base64 data URI, or return URL as-is."""
    if image_path.startswith("http"):
        return image_path
    if os.path.exists(image_path):
        with open(image_path, "rb") as f:
            data = base64.b64encode(f.read()).decode()
        ext = os.path.splitext(image_path)[1].lstrip(".").lower()
        if ext in ("jpg", "jpeg"):
            mime = "image/jpeg"
        elif ext == "png":
            mime = "image/png"
        else:
            mime = f"image/{ext}"
        return f"data:{mime};base64,{data}"
    return image_path

def load_orders():
    if os.path.exists(ORDERS_FILE):
        try:
            return pd.read_csv(ORDERS_FILE)
        except pd.errors.EmptyDataError:
            return pd.DataFrame(columns=['order_id', 'customer_name', 'table_number', 'items', 'quantities', 'total_price', 'status', 'created_at', 'feedback'])
        except Exception as e:
            st.error(f"Error loading orders: {e}")
            return pd.DataFrame(columns=['order_id', 'customer_name', 'table_number', 'items', 'quantities', 'total_price', 'status', 'created_at', 'feedback'])
    else:
        return pd.DataFrame(columns=['order_id', 'customer_name', 'table_number', 'items', 'quantities', 'total_price', 'status', 'created_at', 'feedback'])

def get_customer_order_count(name):
    orders_df = load_orders()
    if orders_df.empty or not name:
        return 0
    return len(orders_df[orders_df['customer_name'].str.lower() == name.lower()])

def save_orders(df):
    df.to_csv(ORDERS_FILE, index=False)

def get_next_order_id():
    orders_df = load_orders()
    if orders_df.empty:
        return 1
    return orders_df['order_id'].max() + 1

def calculate_analytics():
    orders_df = load_orders()
    if orders_df.empty:
        return {
            'total_orders': 0,
            'total_revenue': 0.0,
            'popular_items': {},
            'daily_revenue': 0.0
        }

    total_orders = len(orders_df)
    total_revenue = orders_df['total_price'].sum()

    # Popular items
    popular_items = {}
    for _, row in orders_df.iterrows():
        items = eval(row['items'])  # Assuming items are stored as string representation of list
        quantities = eval(row['quantities'])
        for item, qty in zip(items, quantities):
            if item in popular_items:
                popular_items[item] += qty
            else:
                popular_items[item] = qty

    # Sort popular items
    popular_items = dict(sorted(popular_items.items(), key=lambda x: x[1], reverse=True))

    # Daily revenue (assuming all orders are from today for simplicity)
    daily_revenue = total_revenue

    return {
        'total_orders': total_orders,
        'total_revenue': total_revenue,
        'popular_items': popular_items,
        'daily_revenue': daily_revenue
    }

# Sidebar navigation
st.sidebar.markdown('<div class="sidebar-nav">', unsafe_allow_html=True)
st.sidebar.title("☕ Smart Café")

# Navigation using session state
page_options = ["Home", "Customer Order", "Order Status", "Admin Dashboard"]
page = st.sidebar.radio("Navigation", page_options, index=page_options.index(st.session_state.page), key="nav_radio")
if page != st.session_state.page:
    st.session_state.page = page
    st.rerun()
    
st.sidebar.markdown('</div>', unsafe_allow_html=True)

# Main content
if st.session_state.page == "Home":
    st.markdown('<div class="home-page-marker"></div>', unsafe_allow_html=True)
    st.markdown('<h1 class="home-header">Welcome to Smart Café ☕</h1>', unsafe_allow_html=True)
    st.markdown('<p class="home-subtitle">Please enter your details to begin your order</p>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown('<div style="background: white; padding: 2rem; border-radius: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.05);">', unsafe_allow_html=True)
        st.session_state.customer_name = st.text_input("👤 Your Name", value=st.session_state.customer_name)
        st.session_state.table_number = st.text_input("🪑 Table Number", value=st.session_state.table_number)

        if st.session_state.customer_name:
            order_count = get_customer_order_count(st.session_state.customer_name)
            if order_count > 0:
                st.info(f"Welcome back! You have placed {order_count} orders with us.")
            if order_count >= 3:
                st.success("🎉 **Congratulations!** Because you've placed more than 3 orders, you qualify for a **Free Gift Hamper** with your next order!")

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Proceed to Menu", use_container_width=True, type="primary"):
            if not st.session_state.customer_name or not st.session_state.table_number:
                st.warning("Please enter both your name and table number to proceed.")
            else:
                st.session_state.page = "Customer Order"
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.page == "Customer Order":
    st.markdown('<h1 class="main-header">Menu</h1>', unsafe_allow_html=True)
    st.markdown("Freshly brewed coffee and delicious snacks delivered to your table.")
    
    if not st.session_state.customer_name or not st.session_state.table_number:
        st.warning("⚠️ Please go to the **Home** page first to enter your Name and Table Number before ordering.")
        st.stop()

    # Today's Special
    st.subheader("⭐ Today's Special")
    col1, col2 = st.columns([1, 2])
    with col1:
        st.image(TODAYS_SPECIAL["image"], use_column_width=True)
    with col2:
        st.markdown(f"### {TODAYS_SPECIAL['name']}")
        st.markdown(f"**${TODAYS_SPECIAL['price']:.2f}**")
        st.markdown(TODAYS_SPECIAL["description"])
        if st.button("Add to Order", key="special"):
            if TODAYS_SPECIAL["name"] not in [item['name'] for item in st.session_state.cart]:
                st.session_state.cart.append({
                    'name': TODAYS_SPECIAL["name"],
                    'price': TODAYS_SPECIAL["price"],
                    'quantity': 1
                })
            else:
                for item in st.session_state.cart:
                    if item['name'] == TODAYS_SPECIAL["name"]:
                        item['quantity'] += 1
            st.success("Added to cart!")

    # Menu
    st.subheader("Our Menu")
    for category, items in MENU.items():
        st.markdown(f"### {category}")
        cols = st.columns(2)
        for i, item in enumerate(items):
            with cols[i % 2]:
                st.markdown(f"""
                <div class="menu-card">
                    <img src="{get_image_src(item['image'])}">
                    <div class="menu-card-overlay">
                        <h4>{item['name']}</h4>
                        <p>${item['price']:.2f}</p>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                st.markdown('<div class="add-btn-container">', unsafe_allow_html=True)
                if st.button("ADD", key=f"{category}_{i}"):
                    if item['name'] not in [cart_item['name'] for cart_item in st.session_state.cart]:
                        st.session_state.cart.append({
                            'name': item['name'],
                            'price': item['price'],
                            'quantity': 1
                        })
                    else:
                        for cart_item in st.session_state.cart:
                            if cart_item['name'] == item['name']:
                                cart_item['quantity'] += 1
                    st.success("Added to cart!")
                st.markdown('</div>', unsafe_allow_html=True)

    # Cart
    st.subheader("Your Order")
    if st.session_state.cart:
        cart_df = pd.DataFrame(st.session_state.cart)
        cart_df['Subtotal'] = cart_df['price'] * cart_df['quantity']
        st.dataframe(cart_df[['name', 'quantity', 'price', 'Subtotal']])

        total = cart_df['Subtotal'].sum()
        st.markdown(f"**Total: ${total:.2f}**")

        if st.button("Place Order", disabled=not (st.session_state.customer_name and st.session_state.table_number and st.session_state.cart)):
            # Save order
            orders_df = load_orders()
            order_id = get_next_order_id()
            order_count = get_customer_order_count(st.session_state.customer_name)
            includes_gift = order_count >= 3
            
            new_order = {
                'order_id': order_id,
                'customer_name': st.session_state.customer_name,
                'table_number': st.session_state.table_number,
                'items': str([item['name'] for item in st.session_state.cart] + (["Gift Hamper"] if includes_gift else [])),
                'quantities': str([item['quantity'] for item in st.session_state.cart] + ([1] if includes_gift else [])),
                'total_price': total,
                'status': 'Preparing',
                'created_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'feedback': ''
            }
            
            try:
                orders_df = pd.concat([orders_df, pd.DataFrame([new_order])], ignore_index=True)
                save_orders(orders_df)

                st.session_state.current_order_id = order_id
                st.session_state.order_placed = True
                st.session_state.cart = []
                st.success("Order placed successfully! Please wait while we prepare your order.")
                if includes_gift:
                    st.balloons()
                    st.success("🎁 A Free Gift Hamper has been added to your order!")
            except Exception as e:
                st.error(f"Order is not placed. Error: {e}")
    else:
        st.info("Your cart is empty. Add some items from the menu!")

elif st.session_state.page == "Order Status":
    st.markdown('<h1 class="main-header">Order Tracking</h1>', unsafe_allow_html=True)
    st.markdown("Real-time updates on your delicious treats.")

    if st.session_state.current_order_id:
        orders_df = load_orders()
        user_orders = orders_df[orders_df['order_id'] == st.session_state.current_order_id]

        if not user_orders.empty:
            order = user_orders.iloc[0]
            status = order['status']

            col1, col2 = st.columns([1, 2])
            with col1:
                if status == 'Preparing':
                    st.markdown('<div class="status-preparing">Preparing</div>', unsafe_allow_html=True)
                elif status == 'Ready':
                    st.markdown('<div class="status-ready">Ready</div>', unsafe_allow_html=True)
                elif status == 'Completed':
                    st.markdown('<div class="status-completed">Completed</div>', unsafe_allow_html=True)

            with col2:
                st.markdown(f"**Order #{int(order['order_id'])}**")
                st.markdown(f"**Customer:** {order['customer_name']}")
                st.markdown(f"**Table:** {order['table_number']}")
                st.markdown(f"**Total:** ${order['total_price']:.2f}")
                st.markdown(f"**Ordered at:** {order['created_at']}")
            
            # Feedback section for Completed orders
            if status == 'Completed':
                st.markdown("---")
                st.subheader("How was your experience?")
                
                # Check if feedback already exists
                current_feedback = order.get('feedback', '')
                if pd.isna(current_feedback):
                    current_feedback = ''
                    
                feedback = st.text_area("Leave a review or feedback", value=current_feedback, key=f"fb_{order['order_id']}")
                if st.button("Submit Feedback"):
                    if feedback.strip():
                        # Update the dataframe
                        idx = orders_df.index[orders_df['order_id'] == order['order_id']].tolist()[0]
                        orders_df.at[idx, 'feedback'] = feedback
                        save_orders(orders_df)
                        st.success("Thank you for your feedback!")
                    else:
                        st.warning("Please enter some feedback before submitting.")
        else:
            st.info("No active orders found.")
    else:
        st.info("No active orders. Place an order first!")

elif st.session_state.page == "Admin Dashboard":
    st.markdown('<h1 class="main-header">Admin Dashboard</h1>', unsafe_allow_html=True)
    st.markdown("Monitor café performance and manage orders.")

    analytics = calculate_analytics()

    # Stats
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Orders", analytics['total_orders'])
    with col2:
        st.metric("Total Revenue", f"${analytics['total_revenue']:.2f}")
    with col3:
        if analytics['popular_items']:
            most_popular = list(analytics['popular_items'].keys())[0]
            st.metric("Most Popular Item", most_popular)
        else:
            st.metric("Most Popular Item", "N/A")

    # Orders Table
    st.subheader("Recent Orders")
    orders_df = load_orders()
    if not orders_df.empty:
        # Add status update functionality
        for idx, row in orders_df.iterrows():
            col1, col2, col3, col4, col5 = st.columns([1, 2, 2, 1, 2])
            with col1:
                st.write(f"#{int(row['order_id'])}")
            with col2:
                st.write(row['customer_name'])
            with col3:
                st.write(f"Table {row['table_number']}")
            with col4:
                if row['status'] == 'Preparing':
                    st.markdown('<div class="status-preparing">Preparing</div>', unsafe_allow_html=True)
                elif row['status'] == 'Ready':
                    st.markdown('<div class="status-ready">Ready</div>', unsafe_allow_html=True)
                elif row['status'] == 'Completed':
                    st.markdown('<div class="status-completed">Completed</div>', unsafe_allow_html=True)
            with col5:
                new_status = st.selectbox(
                    f"Update status for order #{int(row['order_id'])}",
                    ['Preparing', 'Ready', 'Completed'],
                    index=['Preparing', 'Ready', 'Completed'].index(row['status']),
                    key=f"status_{idx}"
                )
                if new_status != row['status']:
                    orders_df.at[idx, 'status'] = new_status
                    save_orders(orders_df)
                    st.rerun()

        st.dataframe(orders_df[['order_id', 'customer_name', 'table_number', 'total_price', 'status', 'created_at']])
    else:
        st.info("No orders yet.")

    # Popular Items Chart
    if analytics['popular_items']:
        st.subheader("Popular Items")
        chart_data = pd.DataFrame({
            'Item': list(analytics['popular_items'].keys())[:10],  # Top 10
            'Orders': list(analytics['popular_items'].values())[:10]
        })
        st.bar_chart(chart_data.set_index('Item'))
    else:
        st.info("No data available for popular items chart.")
