import sudokum, sys
import socket
import threading
import numpy as np
import time


def verify_sudoku_size(out_sudoku):
    try:
        if len(out_sudoku)!=9:
            return False
        for row in out_sudoku:
            if len(row)!=9:
                return False
        return True
    except:
        return False
    
def verify_sudoku_input(in_sudoku,out_sudoku):
    try:
        for i in range(9):
            for j in range(9):
                if int(out_sudoku[i][j])<1 or int(out_sudoku[i][j])>9:
                    return False
                if in_sudoku[i][j]!=0:
                    if in_sudoku[i][j]!=out_sudoku[i][j]:
                        return False
        return True
    except:
        return False
    
def verify_sudoku_solution(out_sudoku):
    try:
        for i in range(9):
            check_list=[]
            for j in range(9):
                if int(out_sudoku[i][j]) in check_list:
                    return False
                check_list.append(int(out_sudoku[i][j]))

        for i in range(9):
            check_list=[]
            for j in range(9):
                if int(out_sudoku[j][i]) in check_list:
                    return False
                check_list.append(int(out_sudoku[j][i]))
        
        for i in range(3):
            for j in range(3):
                check_list=[]
                for a in range(3):
                    for b in range(3):
                        row_idx = i*3+a
                        col_idx = j*3+b
                        if int(out_sudoku[row_idx][col_idx]) in check_list:
                            return False
                        check_list.append(int(out_sudoku[row_idx][col_idx]))
        return True
    except:
        return False

def verify_sudoku(in_sudoku,out_sudoku):
    return verify_sudoku_size(out_sudoku) and verify_sudoku_input(in_sudoku,out_sudoku) and verify_sudoku_solution(out_sudoku)

def strip_string(string_input):
    string_input=string_input.replace("[","").replace("]","").replace(",","").replace(" ","")
    return string_input

def conver_to_list(striped_input_string):
    sud = []
    for i in range(9):
        sud.append([])
        for j in range(9):
            sud[i].append(int(striped_input_string[9*i+j]))
    return sud

def list_to_string(input_list):
    if isinstance(input_list, list):
        inner_strings = [list_to_string(item) for item in input_list]
        return "[" + ", ".join(inner_strings) + "]"
    else:
        return str(input_list)
    
def sudoku_give():
    try:
        input_sudoku = sudokum.generate(mask_rate=0)
        print (input_sudoku)

        output_sudoku = input()
        output_sudoku = strip_string(output_sudoku)
        if len(output_sudoku)!=81:
            print("Bad Job")
            return False

        output_sudoku = conver_to_list(output_sudoku)

        if verify_sudoku(input_sudoku,output_sudoku):
            print("Good Job")
            return True

        return False
    
    except:
        sys.exit(0)


def handle_client(client_socket):
    # Generate a sudoku puzzle
    num_sud = 10
    client_socket.send("Here is your sudoku, Have fun XD\n".encode())
    client_socket.send("Enter Ans in Same Format\n".encode())

    for i in range(num_sud):
        input_sudoku = sudokum.generate(mask_rate=0)

        # Send the puzzle to the client
        client_socket.send(list_to_string(input_sudoku).encode())

        # Receive the solution from the client
        output_sudoku = client_socket.recv(1024).decode().strip()
        output_sudoku = strip_string(output_sudoku)

        if len(output_sudoku)!=81:
            client_socket.send("Incorrect solution. Try again.".encode())
                
        output_sudoku = conver_to_list(output_sudoku)
        # Verify the solution
        if verify_sudoku(input_sudoku,output_sudoku):
            client_socket.send("\nCorrect! Congratulations!\n".encode())
        else:
            client_socket.send("Incorrect solution.".encode())
            client_socket.close()
            break

    client_socket.close()
        # Close the client socket

# Create a TCP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to a host and port
server_socket.bind(('localhost', 12345))

# Listen for incoming connections
server_socket.listen(1000)

print("[*] Listening on localhost:12345")

while True:
    # Accept incoming connection
    client_socket, addr = server_socket.accept()
    print(f"[*] Accepted connection from {addr[0]}:{addr[1]}")

    # Start a new thread to handle the client
    client_handler = threading.Thread(target=handle_client, args=(client_socket,))
    client_handler.start()

# if __name__=='__main__':
#     print("Here is your sudoku, Have fun XD")
#     print ("Enter Ans in Same Format:")
#     count=0
#     num_sudoku = 10
#     for i in range(num_sudoku):
#         if sudoku_give():
#             continue
#         else:
#             print("Try Again, Wrong Ans")
#             sys.exit(0)
#     sys.exit(0)