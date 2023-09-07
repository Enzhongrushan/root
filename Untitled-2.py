def count_and_replace(file_name):

    with open(file_name, 'file_to_read.txt') as file:
       
        content = file.read()

  
        count = content.count('terrible')


        replaced_content = content.replace('terrible', 'pathetic', count//2)
        replaced_content = replaced_content.replace('terrible', 'marvellous', count-count//2)


        print(replaced_content)

        return count

file_name = "file_to_read.txt"
count = count_and_replace(file_name)
print("The word 'terrible' appears", count, "times in the file.")