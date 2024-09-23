import streamlit as st
import pandas as pd
import plotly.express as px
import json
import requests
from PIL import Image
from io import BytesIO
from streamlit_plotly_events import plotly_events

# Load the data
with open('data/images.json', 'r') as f:
    data = json.load(f)

# Convert to DataFrame
df = pd.DataFrame(data)

# Sidebar dropdown for image selection
selected_image_url = st.sidebar.selectbox("Select an image", df['image_url'].tolist())
selected_index = df[df['image_url'] == selected_image_url].index[0]

# Create the scatter plot
fig = px.scatter(
    df,
    x='x',
    y='y',
    hover_data=['image_url'],
    title='UMAP Visualization of Images'
)

# Highlight the selected point
fig.add_trace(px.scatter(
    df.iloc[[selected_index]],
    x='x',
    y='y',
    hover_data=['image_url'],
    color_discrete_sequence=['red']
).data[0])

# Customize hover template
fig.update_traces(
    hovertemplate='<br>'.join([
        'x: %{x}',
        'y: %{y}'
    ])
)

# Enable selection and lasso tools
fig.update_layout(
    dragmode='lasso',
    hovermode='closest',
    selectdirection='any'
)
fig.update_xaxes(fixedrange=False)
fig.update_yaxes(fixedrange=False)

# Display the plot and capture selected points
selected_points = plotly_events(fig, click_event=False, hover_event=False, select_event=True)

# Create containers for the image grid and selected image
image_grid = st.container()
selected_image_container = st.container()

# Function to update image grid
def update_image_grid(selected_indices):
    if selected_indices:
        selected_images = [df.iloc[i]['image_url'] for i in selected_indices]
        with image_grid:
            st.empty()
            cols = st.columns(min(5, len(selected_images)))
            for i, image_url in enumerate(selected_images):
                try:
                    response = requests.get(image_url)
                    img = Image.open(BytesIO(response.content))
                    cols[i % 5].image(img, use_column_width=True)
                except Exception as e:
                    cols[i % 5].error(f"Failed to load image: {str(e)}")

# Display selected image
with selected_image_container:
    st.sidebar.subheader("Selected Image")
    try:
        response = requests.get(selected_image_url)
        img = Image.open(BytesIO(response.content))
        st.sidebar.image(img, use_column_width=True)
    except Exception as e:
        st.error(f"Failed to load image: {str(e)}")

# Add a button to trigger selection
if st.button('Update Images from Selection'):
    if selected_points:
        selected_indices = [point['pointIndex'] for point in selected_points]
        update_image_grid(selected_indices)
    else:
        st.write("No points selected. Use the lasso or box select tool to select points on the plot.")

# Add instructions for interacting with the plot
st.write("Use the lasso or box select tool to select points on the plot, then click 'Update Images from Selection' to view the corresponding images.")
