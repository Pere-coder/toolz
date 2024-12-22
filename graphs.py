import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv
import os
load_dotenv()

password = os.environ.get("password")
def sendmail(sender_email, receiver_email, text, password):
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = receiver_email
    message['Subject'] = "message from GRAPH PLOT"
    body = text
    message.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, password)

        server.sendmail(sender_email, receiver_email, message.as_string())

        st.write("Email sent successfully!")
    except Exception as e:
         st.write(f"Error {e}")
    finally:
         server.quit()

st.write("# GRAPHY")
st.write("""
# Graphy: An Interactive Graph Plotting Tool for Students

**Graphy** is an innovative tool designed to help students seamlessly plot and visualize mathematical graphs in real-time, enhancing their learning experience and deepening their understanding of concepts. With its intuitive interface, **Graphy** empowers users to quickly input their data points and immediately see the resulting graph, making it ideal for interactive learning in classrooms or for self-paced study.

## Key Features of Graphy

- **Real-Time Plotting**:  
  As students input data points, the graph updates dynamically, allowing them to instantly observe the effects of their changes. This helps with immediate feedback and makes learning more interactive.

- **Default Axis Customization**:  
  Students can define the boundaries of the graph with adjustable default axes, providing flexibility to create graphs that suit various mathematical problems.

- **Slope and Intercept Calculation**:  
  With just a few clicks, students can easily calculate the slope and intercept of their data points and see the best-fit line, reinforcing their understanding of linear regression.

- **Interactive Annotations**:  
  The tool includes the ability to highlight key features of the graph, such as the change in X and Y values (`Δx`, `Δy`), and display the corresponding coordinates, aiding students in their analysis.

- **Grid and Labels**:  
  The graphing interface is designed with clear axis labels and grid lines to help students interpret their graphs more easily.

## How Graphy Enhances Learning

The primary goal of **Graphy** is to make graph plotting an effortless task, allowing students to focus more on interpreting the results rather than spending time on the mechanics of graph creation. Whether plotting basic linear graphs, exploring advanced data trends, or visualizing mathematical functions, **Graphy** enables users to intuitively see how changes in input data affect the graph.

By combining a user-friendly interface with powerful functionality, **Graphy** bridges the gap between theory and application, making graph plotting not only easy but also an engaging and effective way to learn. This tool helps students not only visualize but also better understand the relationships between variables, making it an invaluable resource in subjects like algebra, calculus, statistics, and data science.

## Conclusion

The goal is for **Graphy** to become an essential part of students' learning tools, empowering them to explore mathematical concepts in a way that is both interactive and educational.
""")

st.markdown("### <u style='color: coral;'>Normal graph</u>", unsafe_allow_html=True)
numberx_string = st.text_input("Enter a list of X values (comma-separated):", value="1,2,3,4,5")
numbery_string = st.text_input("Enter a list of Y values (comma-separated):", value="3,5,8,9,10")




if st.checkbox('Input default x and y axis'):
    default_x = st.text_input("Enter a list of default X values (comma-separated):", key='x')
    default_y = st.text_input("Enter a list of default Y values (comma-separated):", key='y')

    # Parse default X and Y values if provided
    default_x = default_x if default_x else None
    default_y = default_y if default_y else None
else:
    default_x = None
    default_y = None


def plotgraph(xvalues, yvalues, default_x=None, default_y=None):
    try:
        # Ensure that xvalues and yvalues are numpy arrays of type float
        xpoints = np.array(xvalues, dtype=float)
        ypoints = np.array(yvalues, dtype=float)

        # Perform linear regression using the user data points
        coefficients = np.polyfit(xpoints, ypoints, 1)
        slope = coefficients[0]
        intercept = coefficients[1]

        # Create the plot
        fig, ax = plt.subplots()

        # Plot the default axis if provided
        if default_x is not None and default_y is not None:
            ax.plot(default_x, default_y, label='Default Axis', color='gray', alpha=0.3)

        # Plot the user data points
        ax.plot(xpoints, ypoints, 'o', label='Data Points', color='blue')

        # Plot the line of best fit for the user data
        ax.plot(xpoints, slope * xpoints + intercept, label=f'Best Fit: y={slope:.2f}x + {intercept:.2f}', color='red')

        # Find two points on the line (for showing Δx and Δy)
        x1, x2 = xpoints[1], xpoints[3]
        y1, y2 = slope * x1 + intercept, slope * x2 + intercept

        # Plot the change in x and y with dashed lines
        ax.plot([x1, x2], [y1, y1], 'r--', label=f'Δx = {x2 - x1:.2f}')
        ax.plot([x2, x2], [y1, y2], 'g--', label=f'Δy = {y2 - y1:.2f}')

        # Add text labels at points (x1, y1) and (x2, y2)
        ax.text(x1, y1, f'(x1:{x1}, y1:{y1:.2f})', fontsize=8, ha='right')
        ax.text(x2, y2, f'(x2:{x2}, y2:{y2:.2f})', fontsize=8, ha='left')

        # Add grid and labels
        ax.set_xlabel('X-axis')
        ax.set_ylabel('Y-axis')
        ax.set_title('Line of Best Fit and User Data on Default Axis')

        # Show legend
        ax.legend()

        # Add grid lines for readability
        ax.grid(which='major', linestyle='-', linewidth=0.5, alpha=0.7)
        ax.minorticks_on()
        ax.grid(which='minor', linestyle=':', linewidth=0.3, alpha=0.5)

        # Display plot and results in Streamlit
        st.write(f"Slope: {slope:.3f}\nIntercept: {intercept:.3f}")
        st.pyplot(fig)

    except ValueError as e:
        st.error(f"Error: {e}")

def parse_input(number_string):
     try:
        if len(number_string) < 5:
             st.error('List should be greater than 4 numbers')
        return np.array([float(num.strip()) for num in number_string.split(",")])
     except ValueError:
          return None
     

if st.button("Plot normal graph"):
    xpoints = parse_input(numberx_string)
    ypoints = parse_input(numbery_string)
    if default_x and default_y:
        default_x = parse_input(default_x)
        default_y = parse_input(default_y)
    if xpoints is None or ypoints is None:
        st.error("Invalid input. Please enter valid comma-separated numbers.")
    elif len(xpoints) != len(ypoints):
        st.error("X and Y values must have the same length.")
    elif len(xpoints) < 2:
        st.error("At least two points are required for plotting.")
    else:
        plotgraph(xpoints, ypoints, default_x, default_y)




st.markdown("### <u style='color: coral;'>Bar graph</u>", unsafe_allow_html=True)
numberx_bar_string = st.text_input("Enter a list of X values (comma-separated):", value="1,2,3,4,5", key='x_bar')
numbery_bar_string = st.text_input("Enter a list of Y values (comma-separated):", value="3,5,8,9,10", key="y_bar")

def plot_bar_graph(numberx_bar_string, numbery_bar_string):
    # Parsing the inputs
    x_bar = parse_input(numberx_bar_string)
    y_bar = parse_input(numbery_bar_string)
    
    # Check if X and Y values have the same length
    if len(x_bar) != len(y_bar):
         st.error("X and Y values must have the same length.")
         return
    
    # Define custom colors for the bars
    bar_colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b']
    
    # Set up the figure and axis
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Create the bar graph with color and additional styles
    bars = ax.bar(x_bar, y_bar, color=bar_colors[:len(x_bar)])
    
    # Add title and labels
    ax.set_title('Bar Graph Example', fontsize=16, fontweight='bold')
    ax.set_xlabel('X Axis Label', fontsize=12)
    ax.set_ylabel('Y Axis Label', fontsize=12)
    
    # Display the value of each bar on top
    for bar in bars:
        yval = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, yval + 0.1, str(round(yval, 2)),
                ha='center', va='bottom', fontsize=10, color='black', fontweight='bold')
    
    # Add gridlines for better readability
    ax.grid(True, axis='y', linestyle='--', alpha=0.7)
    
    # Display the graph
    st.pyplot(fig)

if st.button("Plot bar graph"):
    try:
        plot_bar_graph(numberx_bar_string, numbery_bar_string)
    except Exception as e:
        st.write(f"An Error occured {e}")



st.markdown("### <u style='color: coral;'>Scatter Plot</u>", unsafe_allow_html=True)
numberx_scatter_string = st.text_input("Enter a list of X values (comma-separated):", value="1,2,3,4,5", key='x_scatter')
numbery_scatter_string = st.text_input("Enter a list of Y values (comma-separated):", value="3,5,8,9,10", key="y_scatter")


def plot_scatter_graph(numberx_scatter_string, numbery_scatter_string):
    x_scatter = parse_input(numberx_scatter_string)
    y_scatter = parse_input(numbery_scatter_string)
    
    if len(x_scatter) != len(y_scatter):
         st.error("X and Y values must have the same length.")
         return
    
    scatter_colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b']
    fig, ax = plt.subplots(figsize=(10, 6))
    
    scatter = ax.scatter(x_scatter, y_scatter, c=scatter_colors[:len(x_scatter)], s=100, edgecolors='black', alpha=0.7)
    
    ax.set_title('Scatter Plot Example', fontsize=16, fontweight='bold')
    ax.set_xlabel('X Axis Label', fontsize=12)
    ax.set_ylabel('Y Axis Label', fontsize=12)
    
    # Display the value of each point next to it
    for i in range(len(x_scatter)):
        ax.text(x_scatter[i] + 0.1, y_scatter[i] + 0.1, f'({x_scatter[i]}, {y_scatter[i]})', 
                fontsize=10, color='black', fontweight='bold')
    
    ax.grid(True, linestyle='--', alpha=0.7)
    st.pyplot(fig)

if st.button("Plot scatter graph"):
    try:
        plot_scatter_graph(numberx_scatter_string, numbery_scatter_string)
    except Exception as e:
        st.write(f"An Error occurred: {e}")


st.markdown("""
    <style>
    .stTextInput>div>div>input[placeholder="Type here..."] {
        background-color: #d4edda;  /* Light green background */
        color: green;  /* Green text color */
    }
    </style>
""", unsafe_allow_html=True)
text = st.text_input("Have any complaints or suggestion?", key="complaints", placeholder="Type here...")
sender_email = "gpere800@gmail.com"
receiver_email = "gpere800@gmail.com"
password = password

if st.button("Send Message"):
    try:
        sendmail(sender_email, receiver_email, text, password)
    except Exception as e:
        st.write(f"Error {e}")



