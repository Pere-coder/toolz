import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
 
st.write("# GRAPH PLOTS")
numberx_string = st.text_input("Enter a list of numbers separated by commas:", key="x_data")
numbery_string = st.text_input("Enter a list of numbers separated by commas:", key="y_data")


def plotgraph(numberx_string, numbery_string):
        try:
            xvalues = [float(num.strip()) for num in numberx_string.split(",")]
            yvalues = [float(num.strip()) for num in numbery_string.split(",")]
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

if st.button('Plot'):
    try:
        plotgraph(numberx_string, numbery_string)
    except ValueError:
        st.error("Please enter a valid list of numbers.")

