import streamlit as st


st.write("### LETTER HELP")
st.write("Choose a template to edit")
#The aim of this script is to present several letter styles for students to be able to edit names 
letter_of_complaints = st.checkbox("Letter of complaint", value=True)
letter_of_health = st.checkbox("Health emergency", value=True)
if letter_of_complaints:
    name =  st.text_input("name: ")
    matric_number = st.text_input("matric no: ")
    department = st.text_input("department: ")
    address = st.text_input("your address: ")
    city = st.text_input("your city: ")
    state = st.text_input("your state: ")
    zip = st.text_input("your zip code: ")
    email = st.text_input("your email: ")
    phone = st.text_input("your phone: ")
    date = st.text_input("your date: ")

    st.write("Letter of complaints!")
    with open("read.txt", "r") as file:
        x = file.read()
        new_name = x.replace("name-of-student", name)
        new_matric = new_name.replace("matric-num", matric_number)
        new_department = new_matric.replace("department-name", department)
        final_copy = new_department
        st.write(final_copy)


elif letter_of_health:
    name =  st.text_input("name: ")
    matric_number = st.text_input("matric no: ")
    department = st.text_input("department: ")

    st.write("Letter of Health!")
    with open("read.txt", "r") as file:
        x = file.read()
        new_name = x.replace("name-of-student", name)
        new_matric = new_name.replace("matric-num", matric_number)
        new_department = new_matric.replace("department-name", department)
        final_copy = new_department
        st.write(final_copy)


# with open("read-result.txt", "w") as result:
#     r = result.write(final_copy)
#     print('success')

# print(f'Old text: {x} \n\nNew text: {final_copy}')    
