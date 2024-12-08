import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText



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

st.write("# GRAPH PLOTS")
text = st.text_input("Have any complaints or suggestion?", key="complaints", placeholder="Type here...")
sender_email = "gpere800@gmail.com"
receiver_email = "gpere800@gmail.com"
password ="fyya kccu tzsf fwgm"

if st.button("Send Message"):
    try:
        sendmail(sender_email, receiver_email, text, password)
    except Exception as e:
        st.write(f"Error {e}")

     


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
     

if st.button("Plot"):
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


