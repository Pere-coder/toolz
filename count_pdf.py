
#The aim of this script is to present several letter styles for students to be able to edit names 
name = input('Enter your name: ')
matric_number = input('Enter your matric no: ')
department = input('Enter your department: ')
with open("read.txt", "r") as file:
    x = file.read()
    new_name = x.replace("name-of-student", name)
    new_matric = new_name.replace("matric-num", matric_number)
    new_department = new_matric.replace("department-name", department)
    final_copy = new_department

with open("read-result.txt", "w") as result:
    r = result.write(final_copy)
    print('success')

print(f'Old text: {x} \n\nNew text: {final_copy}')    
