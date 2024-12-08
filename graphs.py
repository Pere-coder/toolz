import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
 
st.write("# GRAPH PLOTS")
st.write("Have anu complaint or suggestion, Contact us")
numberx_string = st.text_input("Enter a list of X values (comma-separated):", value="1,2,3,4,5")
numbery_string = st.text_input("Enter a list of Y values (comma-separated):", value="3,5,8,9,10")

def plotgraph(xvalues, yvalues):
        try:
            xpoints = np.array(xvalues)
            ypoints = np.array(yvalues)
            coefficients = np.polyfit(xpoints, ypoints, 1)
            slope = coefficients[0]
            intercept = coefficients[1]
            x1, x2 = xpoints[1], xpoints[3]
            y1, y2 = slope * x1 + intercept, slope * x2 + intercept
            fig, ax = plt.subplots()
            ax.plot(xpoints, ypoints, 'o', label='Data Points')
            ax.plot(xpoints, slope * xpoints + intercept, label=f'Best Fit: y={slope:.2f}x+{intercept:.2f}', color='blue')
            ax.plot([x1, x2], [y1, y1], 'r--', label=f'Δx = {x2 - x1}')
            ax.plot([x2, x2], [y1, y2], 'g--', label=f'Δy = {y2 - y1:.3f}')
            ax.text(x1, y1, f'(x1:{x1}, y1:{y1:.2f})', fontsize=8, ha='right')
            ax.text(x2, y2, f'(x2:{x2}, y2:{y2:.2f})', fontsize=8, ha='left')
            ax.set_xlabel('X-axis')
            ax.set_ylabel('Y-axis')
            ax.set_title('Line of Best Fit and Slope Calculation')
            ax.legend()
            ax.grid(which='major', linestyle='-', linewidth=0.5, alpha=0.7)
            ax.minorticks_on()
            ax.grid(which='minor', linestyle=':', linewidth=0.3, alpha=0.5)

            # Display plot and results in Streamlit
            st.write(f"Slope: {slope:.3f}\n\nIntercept: {intercept:.3f}")
            st.pyplot(fig)
        except ValueError:
              st.error("Please enter a correct list of numbers.")


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

    if xpoints is None or ypoints is None:
        st.error("Invalid input. Please enter valid comma-separated numbers.")
    elif len(xpoints) != len(ypoints):
        st.error("X and Y values must have the same length.")
    elif len(xpoints) < 2:
        st.error("At least two points are required for plotting.")
    else:
        plotgraph(xpoints, ypoints)


