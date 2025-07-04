# These are the modules used for running the program:

# The Random module randomly generates numbers and makes choices. This allows the program to scramble the cube and
# decide what side to start on when solving it. The Platform module allows changes based on what system the program is
# being run on.
import random, platform

# The Tkinter module opens windows and places shapes, text, and colors on them. All of the graphics run through Tkinter.
import tkinter as tk

# Sets the font size of text in the program.
font_size = 15

# principal() acts as the program's main function, and it is called at the very end of the script after everything else
# is defined. It creates a hexadecimal numbering system, runs the class, and keeps the window open until you close it
def principal():
    global hexadecimal
    hexadecimal = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C", "D", "E", "F"]
    program = RubiksCube()
    program.window.mainloop()


# Rounds decimals to whole numbers
def round_number(number):
    if abs(number - int(number)) < 0.5:
        response = int(number)
    elif number > 0:
        response = int(number)+1
    else:
        response = int(number)-1
    return response


# Finds the factorial of a number, which is used in the sine and cosine functions that follow
def factorial(number):
    response = 1
    for zero in range(2, number+1):
        response *= zero
    return response


# Finds the sine of a number using a Taylor polynomial
def sine(number):
    number = number % 6.283185307179586
    response = number
    power = 3
    coefficient = -1
    while power < 60:
        response += coefficient * number ** power / factorial(power)
        power += 2
        coefficient *= -1
    return response


# Finds the cosine of a number using a Taylor polynomial
def cos(number):
    number = number % 6.283185307179586
    response = 1
    power = 2
    coefficient = -1
    while power < 60:
        response += coefficient * number ** power / factorial(power)
        power += 2
        coefficient *= -1
    return response


# This function multiplies 3 quaternions together. Quaternions are essinetially 4-dimensional complex numbers that do a
# fantastic job portraying 3-dimensional objects. Additionally, multiplying specific quaternions can imitate 3D
# rotation. To learn more, I highly recommend 3Blue1Brown's content on YouTube. Just know that this tiny function is the
# crux of anything involving rotation.
def quaternion(c, point, c_1):
    product = [c[0]*point[0] - c[1]*point[1] - c[2]*point[2] - c[3]*point[3],
                c[0]*point[1] + c[1]*point[0] + c[2]*point[3] - c[3]*point[2],
                c[0]*point[2] + c[2]*point[0] - c[1]*point[3] + c[3]*point[1],
                c[0]*point[3] + c[3]*point[0] + c[1]*point[2] - c[2]*point[1]]
    response = [0, product[0]*c_1[1] + product[1]*c_1[0] + product[2]*c_1[3] - product[3]*c_1[2],
                product[0]*c_1[2] + product[2]*c_1[0] - product[1]*c_1[3] + product[3]*c_1[1],
                product[0]*c_1[3] + product[3]*c_1[0] + product[1]*c_1[2] - product[2]*c_1[1]]
    return response


# This function changes the color of a square sticker based on its direction. It is responsible for the animated
# "shadow" effect.
def luz(color, vector):
    i = 0.3922322702763681
    j = 0.5883484054145521
    k = 0.7071067811865476
    number = round_number((i * vector[1] - j * vector[2] - k * vector[3]) * 63)
    r = max(hexadecimal.index(color[1]) * 16 + hexadecimal.index(color[2]) + number, 0)
    v = max(hexadecimal.index(color[3]) * 16 + hexadecimal.index(color[4]) + number, 0)
    a = max(hexadecimal.index(color[5]) * 16 + hexadecimal.index(color[6]) + number, 0)
    r = hexadecimal[r // 16] + hexadecimal[r % 16]
    v = hexadecimal[v // 16] + hexadecimal[v % 16]
    a = hexadecimal[a // 16] + hexadecimal[a % 16]
    return "#"+r+v+a



# Ir() is a class that creates the cube and allows you to interact with it.
class RubiksCube():

    # This is the first function in the class, and it sets everything up. It creates the cube, the background, and the
    # interface. The functions self.system(), self.primary_button(), and self.button() are found at the end, and they can
    # show you more of what exactly is being set up.
    def __init__(self):
        
        self.system()
        self.window = tk.Tk()
        self.window.protocol("WM_DELETE_WINDOW", self.terminal)
        self.window.configure(bg="#83D9D9", width=512, height=640)
        self.window.title("The Cube of Rubik")
        self.case = tk.Frame(self.window, bg="#83D9D9", height=512, width=512)
        self.alternate_position = tk.Frame(self.window, bg="#000000")
        self.frame = tk.Frame(self.alternate_position, bg="#00A8C0", height=127, width=508)
        self.space = tk.Canvas(self.case, bg="#83D9D9", borderwidth=0, highlightthickness=0, height=512, width=512)
        self.case.grid(row=0, column=0)
        self.alternate_position.grid(row=1, column=0, sticky="WE")
        self.frame.grid(padx=2, pady=2)
        self.space.pack()
        x_coordinate = int(self.window.winfo_screenwidth() / 2 - self.window.winfo_reqwidth() / 2)
        y_coordinate = int(64 * self.window.winfo_screenheight() / 900)
        self.window.geometry("+{}+{}".format(x_coordinate, y_coordinate))
        self.rotate(-0.3926990816987241, 0, 1)
        self.rotate(0.2855993321445267, 1, 0)
        self.create()
        self.primary_button()
        self.button()



    #           ORGANIZATION AND ANIMATION

    # This function allows multiple animations to happen at once, such as rotating a side while orienting the entire
    # cube. It also paces the program and prevents it from crashing.
    def update_value(self):
        declaration = True
        if self.rg != None:
            self.rotate(self.rg[0], self.rg[1], self.rg[2])
            self.rg = None
            declaration = False
        if self.ra != None:
            if self.interval != 0 and self.min_size:
                self.animate_size(self.ra[0], self.ra[1])
            else:
                self.rotate_side(self.ra[0], self.ra[1])
                self.ra = None
                if not self.min_size:
                    self.min_size = True
            declaration = False
        if declaration:
            self.step_sequence = True
        elif self.open:
            self.create()
            if self.open:
                self.window.after(0, self.update_value)


    # This uses information about the cube to create a step_sequences of shapes. Because it is so precise, these shapes come
    # together to look like a 3D cube. The shapes must be created in order from farthest to closest to yield a cohesive
    # image.
    def create(self):
        self.square = [[self.vertex[0], self.vertex[2], self.vertex[6], self.vertex[4]],
                       [self.vertex[0], self.vertex[1], self.vertex[3], self.vertex[2]],
                       [self.vertex[0], self.vertex[1], self.vertex[5], self.vertex[4]],
                       [self.vertex[1], self.vertex[3], self.vertex[7], self.vertex[5]],
                       [self.vertex[4], self.vertex[5], self.vertex[7], self.vertex[6]],
                       [self.vertex[2], self.vertex[3], self.vertex[7], self.vertex[6]]]
        if True in self.transition:
            self.layer_three = [[self.v_temp[0], self.v_temp[2], self.v_temp[6], self.v_temp[4]],
                           [self.v_temp[0], self.v_temp[1], self.v_temp[3], self.v_temp[2]],
                           [self.v_temp[0], self.v_temp[1], self.v_temp[5], self.v_temp[4]],
                           [self.v_temp[1], self.v_temp[3], self.v_temp[7], self.v_temp[5]],
                           [self.v_temp[4], self.v_temp[5], self.v_temp[7], self.v_temp[6]],
                           [self.v_temp[2], self.v_temp[3], self.v_temp[7], self.v_temp[6]]]
            current_choice = self.transition.index(True)
            for zero in range(6):
                for one in range(4):
                    if self.vertex[self.faces[current_choice][one]] in self.square[zero]:
                        two_temp = self.square[zero].index(self.vertex[self.faces[current_choice][one]])
                        self.square[zero][two_temp] = self.edge[self.block[current_choice][one]]
            for zero in range(6):
                for one in range(4):
                    if self.v_temp[self.faces[(current_choice+3)%6][one]] in self.layer_three[zero]:
                        two_temp = self.layer_three[zero].index(self.v_temp[self.faces[(current_choice+3)%6][one]])
                        self.layer_three[zero][two_temp] = self.f_temp[self.block[current_choice][one]]
            self.organize(current_choice)
            self.space.delete("all")
            for zero in self.todos:
                if zero[0] == 0:
                    list = []
                    for one in self.square[zero[1]]:
                        list.append(256 + round_number(720 * one[1] / (one[3] + 4)))
                        list.append(256 + round_number(720 * one[2] / (one[3] + 4)))
                    self.space.create_polygon(list, fill="#000000", outline="#000000", width=1)
                    for one in range(9):
                        declaration = True
                        if zero[1] == current_choice:
                            declaration = False
                        elif zero[1] in self.right_side[current_choice]:
                            term = self.right_side[current_choice].index(zero[1])
                            if one in self.from_right_side[current_choice][term]:
                                declaration = False
                        if declaration:
                            fractions = self.positions[zero[1]][one]
                            list = []
                            for two in fractions:
                                list.append(256 + round_number(720 * two[0] / (two[2] + 4)))
                                list.append(256 + round_number(720 * two[1] / (two[2] + 4)))
                            if self.contrast:
                                new_color = luz(self.conversion[self.robot_cube[zero[1]][one]],
                                                                  self.vectors[zero[1]])
                            else:
                                new_color = self.conversion[self.robot_cube[zero[1]][one]]
                            self.space.create_polygon(list, fill=new_color, width=0)
                else:
                    list = []
                    for one in self.layer_three[zero[1]]:
                        list.append(256 + round_number(720 * one[1] / (one[3] + 4)))
                        list.append(256 + round_number(720 * one[2] / (one[3] + 4)))
                    self.space.create_polygon(list, fill="#000000", outline="#000000", width=1)
                    for one in range(9):
                        declaration = False
                        if zero[1] == current_choice:
                            declaration = True
                        elif zero[1] in self.right_side[current_choice]:
                            term = self.right_side[current_choice].index(zero[1])
                            if one in self.from_right_side[current_choice][term]:
                                declaration = True
                        if declaration:
                            fractions = self.ubi_temp[zero[1]][one]
                            list = []
                            for two in fractions:
                                list.append(256 + round_number(720 * two[0] / (two[2] + 4)))
                                list.append(256 + round_number(720 * two[1] / (two[2] + 4)))
                            if self.contrast:
                                if zero[1] == current_choice:
                                    new_color = luz(self.conversion[self.robot_cube[zero[1]][one]],
                                                  self.vectors[current_choice])
                                else:
                                    new_color = luz(self.conversion[self.robot_cube[zero[1]][one]],
                                                      self.vec_temp[self.right_side[current_choice].index(zero[1])])
                            else:
                                new_color = self.conversion[self.robot_cube[zero[1]][one]]
                            self.space.create_polygon(list, fill=new_color, width=0)
        else:
            self.organize(None)
            self.space.delete("all")
            for zero in self.flag:
                list = []
                for one in self.square[zero]:
                    list.append(256 + round_number(720 * one[1] / (one[3] + 4)))
                    list.append(256 + round_number(720 * one[2] / (one[3] + 4)))
                self.space.create_polygon(list, fill="#000000", outline="#000000", width=1)
                for one in range(9):
                    fractions = self.positions[zero][one]
                    list = []
                    for two in fractions:
                        list.append(256 + round_number(720 * two[0] / (two[2] + 4)))
                        list.append(256 + round_number(720 * two[1] / (two[2] + 4)))
                    if self.contrast:
                        new_color = luz(self.conversion[self.robot_cube[zero][one]], self.vectors[zero])
                    else:
                        new_color = self.conversion[self.robot_cube[zero][one]]
                    self.space.create_polygon(list, fill=new_color, width=0)
        if self.open:
            self.window.update()
        if self.rule == 3:
            self.rule = 1


    # Determines which sides of the cube are closest and which are farthest. This information is used by self.create(),
    # self.manual_control(), and other functions.
    def organize(self, current_choice):
        list = []
        for zero in range(6):
            number = 0
            for one in self.square[zero]:
                number += one[3]
            if len(list) == 0 or list[len(list)-1][1] <= number:
                list.append([zero, number])
            else:
                var = 0
                while list[var][1] < number:
                    var += 1
                list.insert(var, [zero, number])
        self.flag = [list[2][0], list[1][0], list[0][0]]
        if current_choice != None:
            grand_list = []
            for zero in range(6):
                number = 0
                for one in self.layer_three[zero]:
                    number += one[3]
                if len(grand_list) == 0 or grand_list[len(grand_list) - 1][1] <= number:
                    grand_list.append([zero, number])
                else:
                    var = 0
                    while grand_list[var][1] < number:
                        var += 1
                    grand_list.insert(var, [zero, number])
            if self.vectors[current_choice][3] > -0.023841473169660888:
                self.todos = [[1, grand_list[2][0]], [1, grand_list[1][0]], [1, grand_list[0][0]],
                              [0, list[2][0]], [0, list[1][0]], [0, list[0][0]]]
            else:
                self.todos = [[0, list[2][0]], [0, list[1][0]], [0, list[0][0]],
                              [1, grand_list[2][0]], [1, grand_list[1][0]], [1, grand_list[0][0]]]
            if not [0, current_choice] in self.todos:
                self.todos.insert(0, [0, current_choice])
            answer = (current_choice+3)%6
            if not [1, answer] in self.todos:
                self.todos.insert(0, [1, answer])


    # Determines which side is above and which is to the left of the closest side. This is used for manual controls (key
    # presses).
    def manual_control(self):
        next_move = self.flag[2]
        list = []
        for zero in range(4):
            number = self.square[next_move][zero][2]
            if len(list) == 0 or list[len(list) - 1][1] <= number:
                list.append([zero, number])
            else:
                var = 0
                while list[var][1] < number:
                    var += 1
                list.insert(var, [zero, number])
        point_a = self.faces[self.flag[2]][list[0][0]]
        point_b = self.faces[self.flag[2]][list[1][0]]
        face = 0
        if face == next_move:
            face+=1
        while not (point_a in self.faces[face] and point_b in self.faces[face]):
            face+=1
            if face == next_move:
                face += 1
        self.facemba = face
        self.ay = self.right_side[next_move][(self.right_side[next_move].index(face)-1)%4]


    # Ensures no errors occur when closing the window
    def terminal(self):
        if not self.open:
            self.window.destroy()
        else:
            self.open = False
            self.window.after(17, self.terminal)



    #           ROTATION

    # This function rotates every point on the cube using quaternions. It orients it in certain directions but does not
    # rotate individual sides.
    def rotate(self, angle, v, h):
        r_del_r = [cos(angle/2), v * sine(angle/2), h * sine(angle/2), 0]
        reciprical = [cos(angle/2), v * sine(-angle/2), h * sine(-angle/2), 0]
        for zero in range(8):
            self.vertex[zero] = quaternion(r_del_r, self.vertex[zero], reciprical)
        for zero in range(24):
            list = self.edge[zero]
            far = (list[1]**2 + list[2]**2 + list[3]**2)**0.5
            number = quaternion(r_del_r, [0, list[1] / far, list[2] / far, list[3] / far], reciprical)
            self.edge[zero] = [0, far * number[1], far * number[2], far * number[3]]
        for zero in range(6):
            for one in range(9):
                for two in range(4):
                    list = self.positions[zero][one][two]
                    far = (list[0]**2 + list[1]**2 + list[2]**2)**0.5
                    number = quaternion(r_del_r, [0, list[0] / far, list[1] / far, list[2] / far], reciprical)
                    self.positions[zero][one][two] = [far * number[1] , far * number[2], far * number[3]]
        for zero in range(6):
            self.vectors[zero] = quaternion(r_del_r, self.vectors[zero], reciprical)
        if True in self.transition:
            for zero in range(8):
                self.v_temp[zero] = quaternion(r_del_r, self.v_temp[zero], reciprical)
            for zero in range(24):
                list = self.f_temp[zero]
                far = (list[1] ** 2 + list[2] ** 2 + list[3] ** 2) ** 0.5
                number = quaternion(r_del_r, [0, list[1] / far, list[2] / far, list[3] / far], reciprical)
                self.f_temp[zero] = [0, far * number[1], far * number[2], far * number[3]]
            for zero in range(6):
                if self.ubi_temp[zero] != None:
                    for one in range(9):
                        for two in range(4):
                            list = self.ubi_temp[zero][one][two]
                            far = (list[0] ** 2 + list[1] ** 2 + list[2] ** 2) ** 0.5
                            number = quaternion(r_del_r, [0, list[0]/far, list[1]/far, list[2]/far], reciprical)
                            self.ubi_temp[zero][one][two] = [far * number[1], far * number[2], far * number[3]]
            for zero in range(4):
                self.vec_temp[zero] = quaternion(r_del_r, self.vec_temp[zero], reciprical)


    # This function rotates the sides on an informational level, so that the computer knows how the cube should look.
    def rotate_side(self, face, piece):
        new = [self.robot_cube[0][:], self.robot_cube[1][:], self.robot_cube[2][:],
                 self.robot_cube[3][:], self.robot_cube[4][:], self.robot_cube[5][:]]
        declaration = (face == 0) or (face == 1) or (face == 5)
        if (piece and declaration) or not (piece or declaration):
            self.robot_cube[face][0] = new[face][6]
            self.robot_cube[face][1] = new[face][3]
            self.robot_cube[face][2] = new[face][0]
            self.robot_cube[face][3] = new[face][7]
            self.robot_cube[face][5] = new[face][1]
            self.robot_cube[face][6] = new[face][8]
            self.robot_cube[face][7] = new[face][5]
            self.robot_cube[face][8] = new[face][2]
        else:
            self.robot_cube[face][6] = new[face][0]
            self.robot_cube[face][3] = new[face][1]
            self.robot_cube[face][0] = new[face][2]
            self.robot_cube[face][7] = new[face][3]
            self.robot_cube[face][1] = new[face][5]
            self.robot_cube[face][8] = new[face][6]
            self.robot_cube[face][5] = new[face][7]
            self.robot_cube[face][2] = new[face][8]
        cycle = self.right_side[face]
        squares = self.from_right_side[face]
        if piece:
            for zero in range(3):
                self.robot_cube[cycle[0]][squares[0][zero]] = new[cycle[3]][squares[3][zero]]
                self.robot_cube[cycle[1]][squares[1][zero]] = new[cycle[0]][squares[0][zero]]
                self.robot_cube[cycle[2]][squares[2][zero]] = new[cycle[1]][squares[1][zero]]
                self.robot_cube[cycle[3]][squares[3][zero]] = new[cycle[2]][squares[2][zero]]
        else:
            for zero in range(3):
                self.robot_cube[cycle[0]][squares[0][zero]] = new[cycle[1]][squares[1][zero]]
                self.robot_cube[cycle[1]][squares[1][zero]] = new[cycle[2]][squares[2][zero]]
                self.robot_cube[cycle[2]][squares[2][zero]] = new[cycle[3]][squares[3][zero]]
                self.robot_cube[cycle[3]][squares[3][zero]] = new[cycle[0]][squares[0][zero]]
        if self.rule == 2:
            self.rule = 3


    # This function provides the information necessary for animating side rotations. It also uses quaternion
    # multiplication for this purpose. Note that this function is never used during a "Quick Solve".
    def animate_size(self, face, piece):
        if self.circumference == 0:
            self.v_temp = []
            for zero in self.vertex:
                self.v_temp.append(zero[:])
            self.f_temp = []
            for zero in self.edge:
                self.f_temp.append(zero[:])
            self.ubi_temp = []
            for zero in range(6):
                if zero != (face + 3) % 6:
                    self.ubi_temp.append([])
                    for one in range(9):
                        self.ubi_temp[zero].append([])
                        for two in range(4):
                            self.ubi_temp[zero][one].append(self.positions[zero][one][two][:])
                else:
                    self.ubi_temp.append(None)
            self.vec_temp = []
            for zero in self.right_side[face]:
                self.vec_temp.append(self.vectors[zero][:])
            self.transition[face] = True
        if self.circumference < 16:
            if piece:
                angle = -0.09817477042468103
            else:
                angle = 0.09817477042468103
            v = self.vectors[face][1]
            h = self.vectors[face][2]
            a = self.vectors[face][3]
            r_del_r = [cos(angle/2), v * sine(angle/2), h * sine(angle/2), a * sine(angle/2)]
            reciprical = [cos(angle/2), v * sine(-angle/2), h * sine(-angle/2), a * sine(-angle/2)]
            for zero in self.faces[face]:
                self.v_temp[zero] = quaternion(r_del_r, self.v_temp[zero], reciprical)
            for zero in self.block[face]:
                list = self.f_temp[zero]
                far = ((list[1])**2 + (list[2])**2 + (list[3])**2)**0.5
                number = quaternion(r_del_r, [0, (list[1]) / far, (list[2]) / far, (list[3]) / far], reciprical)
                self.f_temp[zero] = [0, far * number[1], far * number[2], far * number[3]]
            for zero in range(6):
                if self.ubi_temp[zero] != None:
                    for one in range(9):
                        for two in range(4):
                            list = self.ubi_temp[zero][one][two]
                            far = (list[0] ** 2 + list[1] ** 2 + list[2] ** 2) ** 0.5
                            number = quaternion(r_del_r, [0, list[0]/far, list[1]/far, list[2]/far], reciprical)
                            self.ubi_temp[zero][one][two] = [far * number[1], far * number[2], far * number[3]]
            for zero in range(4):
                self.vec_temp[zero] = quaternion(r_del_r, self.vec_temp[zero], reciprical)
            self.circumference += 1
        else:
            self.transition = [False] * 6
            self.circumference = 0
            self.rotate_side(face, piece)
            self.ra = None



    #           ARTIFICIAL INTELLIGENCE / COMPUTER SOLVING

    # When a side is rotated, the AI has to be temporarily interrupted. This function checks the status of the rotation
    # frequently. When the rotation is complete, it returns to whatever step the AI was on.
    def PendingMoves(self):
        if self.rule == 0 and self.open:
            if self.ra == None:
                func = self.undo
                number = self.interval
                self.undo = None
            else:
                func = self.PendingMoves
                if self.interval == 0:
                    number = 2
                else:
                    number = 16
            if self.open:
                self.window.after(number, func)


    # Algorithms can be stored in the list, self.record. This function executes those algorithms then returns to
    # whatever step the AI was on.
    def algorithm(self):
        if self.rule == 0:
            if len(self.record) > 1:
                finish_1, finish_2 = self.record[0]
                self.ra = (finish_1, finish_2)
                if self.record != []:
                    self.record.pop(0)
                self.undo = self.algorithm
                func = self.PendingMoves
                if self.step_sequence:
                    self.step_sequence = False
                    self.update_value()
            else:
                func = self.record[0]
                self.record = []
            if self.open:
                self.window.after(0, func)


    # This is where the AI sequence starts. The function checks to see how solved the Rubik's Cube is. If a certain step
    # is already complete, it will automatically scramble the cube. Then it selects which side will act as the top face
    # and proceeds to the next step, self.FirstStep().
    def start(self):
        self.rule = 0
        self.rule_mini = True
        declaration = False
        for zero in range(6):
            subdeclaration = True
            if self.robot_cube[zero][1] != zero:
                subdeclaration = False
            elif self.robot_cube[zero][3] != zero:
                subdeclaration = False
            elif self.robot_cube[zero][5] != zero:
                subdeclaration = False
            elif self.robot_cube[zero][7] != zero:
                subdeclaration = False
            for one in range(4):
                norma = self.right_side[zero][one]
                if norma != self.robot_cube[self.right_side[zero][one]][self.from_right_side[zero][one][1]]:
                    subdeclaration = False
            if subdeclaration:
                declaration = True
        if declaration:
            self.rule = 0
            for zero in range(144):
                self.rotate_side(random.randrange(6), random.choice([True, False]))
            self.create()
        self.base = random.randrange(6)
        self.util = self.right_side[self.base]
        if self.interval == 0:
            number = 0
        else:
            number = 500
        if self.open:
            self.window.after(number, self.FirstStep)


    # Determines whether rotating the top face would place an edge piece in the right location
    def FirstStep(self):
        if self.rule == 0:
            zero = 0
            while zero < 12:
                if self.base in self.p_a[2*zero]:
                    if self.p_a[2*zero].index(self.base) == 0:
                        if self.robot_cube[self.base][self.p_a[2*zero+1][0]] == self.base:
                            self.valid = (zero, 1)
                            zero = 13
                    else:
                        if self.robot_cube[self.base][self.p_a[2*zero+1][1]] == self.base:
                            self.valid = (zero, 0)
                            zero = 13
                zero+=1
            if zero == 14:
                self.idle = self.p_a[2*self.valid[0]][self.valid[1]]
                self.accurate = self.p_a[2*self.valid[0]+1][self.valid[1]]
                self.color = self.robot_cube[self.idle][self.accurate]
                func = self.first_edge
            else:
                self.move_counter = 0
                self.color = self.util[0]
                func = self.last_edge
            if self.open:
                self.window.after(0, func)


    # This function is only used if rotating the top face does in fact place an edge piece in the right location.
    def first_edge(self):
        if self.rule == 0:
            if self.color != self.idle:
                self.idle = self.util[(self.util.index(self.idle) + 1) % 4]
                if (self.base, self.idle) in self.p_a:
                    self.accurate = self.p_a[self.p_a.index((self.base, self.idle)) + 1][1]
                else:
                    self.accurate = self.p_a[self.p_a.index((self.idle, self.base)) + 1][0]
                self.ra = (self.base, True)
                self.undo = self.first_edge
                func = self.PendingMoves
                if self.step_sequence:
                    self.step_sequence = False
                    self.update_value()
            else:
                self.move_counter = 0
                self.color = self.util[0]
                func = self.last_edge
            if self.open:
                self.window.after(0, func)


    # Places all the edge pieces that belong on the top face where they should be
    def last_edge(self):
        if self.rule == 0:
            declaration = True
            if self.record != []:
                for zero in range(len(self.record)):
                    if declaration:
                        self.record[zero][0] -= 1
                        if self.record[zero][0] == 0:
                            declaration = False
                            rotate = (self.record[zero][1], self.record[zero][2])
                            self.record.pop(zero)
            if declaration:
                zero = 0
                while zero < 24:
                    if self.robot_cube[self.p_a[zero][0]][self.p_a[zero + 1][0]] == self.base and \
                            self.robot_cube[self.p_a[zero][1]][self.p_a[zero + 1][1]] == self.color:
                        self.current_position = self.p_a[zero][0]
                        self.idle = self.p_a[zero][1]
                        zero = 24
                    elif self.robot_cube[self.p_a[zero][0]][self.p_a[zero + 1][0]] == self.color and \
                            self.robot_cube[self.p_a[zero][1]][self.p_a[zero + 1][1]] == self.base:
                        self.idle = self.p_a[zero][0]
                        self.current_position = self.p_a[zero][1]
                        zero = 24
                    else:
                        zero += 2
                if self.current_position == self.base:
                    if self.idle != self.color:
                        self.ra = (self.idle, True)
                        self.undo = self.last_edge
                        func = self.PendingMoves
                        if self.step_sequence:
                            self.step_sequence = False
                            self.update_value()
                    else:
                        if self.move_counter < 3:
                            self.move_counter += 1
                            self.color = self.util[self.move_counter]
                            func = self.last_edge
                        else:
                            self.move_counter = 0
                            self.color = self.util[0]
                            self.crayon = self.util[1]
                            func = self.final_vertices
                elif self.idle == self.base:
                    self.ra = (self.current_position, True)
                    self.undo = self.last_edge
                    func = self.PendingMoves
                    if self.step_sequence:
                        self.step_sequence = False
                        self.update_value()
                elif self.current_position == (self.base+3)%6:
                    if self.idle != self.color:
                        self.ra = (self.current_position, True)
                    else:
                        self.ra = (self.idle, True)
                    self.undo = self.last_edge
                    func = self.PendingMoves
                    if self.step_sequence:
                        self.step_sequence = False
                        self.update_value()
                elif self.idle == (self.base+3)%6:
                    if self.current_position == self.util[(self.util.index(self.color)-1)%4]:
                        self.ra = (self.current_position, True)
                        self.record.append([2, self.current_position, False])
                    else:
                        self.ra = (self.idle, True)
                    self.undo = self.last_edge
                    func = self.PendingMoves
                    if self.step_sequence:
                        self.step_sequence = False
                        self.update_value()
                else:
                    if self.idle == self.color:
                        if self.current_position == self.util[(self.util.index(self.idle)+1)%4]:
                            self.ra = (self.idle, True)
                        else:
                            self.ra = (self.idle, False)
                    else:
                        if self.current_position == self.util[(self.util.index(self.idle)+1)%4]:
                            self.ra = (self.idle, False)
                            self.record.append([2, self.idle, True])
                        else:
                            self.ra = (self.idle, True)
                            self.record.append([2, self.idle, False])
                    self.undo = self.last_edge
                    func = self.PendingMoves
                    if self.step_sequence:
                        self.step_sequence = False
                        self.update_value()
            else:
                self.ra = (rotate[0], rotate[1])
                self.undo = self.last_edge
                func = self.PendingMoves
                if self.step_sequence:
                    self.step_sequence = False
                    self.update_value()
            if self.open:
                self.window.after(0, func)


    # Places all the corner pieces that belong on the top face where they should be
    def final_vertices(self):
        if self.rule == 0:
            zero = 0
            while zero < 16:
                group = (self.robot_cube[self.p_v[zero][0]][self.p_v[zero + 1][0]],
                         self.robot_cube[self.p_v[zero][1]][self.p_v[zero + 1][1]],
                         self.robot_cube[self.p_v[zero][2]][self.p_v[zero + 1][2]])
                if self.base in group and self.color in group and self.crayon in group:
                    faces = (self.p_v[zero][0], self.p_v[zero][1], self.p_v[zero][2])
                    self.current_position = faces[group.index(self.base)]
                    self.idle = faces[group.index(self.color)]
                    self.accurate = faces[group.index(self.crayon)]
                    zero = 16
                else:
                    zero+=2
            if self.current_position == self.base and self.idle == self.color and self.accurate == self.crayon:
                if self.move_counter < 3:
                    self.move_counter += 1
                    self.color = self.util[self.move_counter]
                    self.crayon = self.util[(self.move_counter+1)%4]
                    func = self.final_vertices
                else:
                    self.move_counter = 0
                    self.color = self.util[0]
                    self.crayon = self.util[1]
                    self.base = (self.base + 3) % 6
                    func = self.middle
            elif self.current_position == self.base or self.idle == self.base or self.accurate == self.base:
                if self.current_position == self.base:
                    if self.idle == self.util[(self.util.index(self.accurate) + 1) % 4]:
                        self.valid = self.idle
                    else:
                        self.valid = self.accurate
                elif self.idle == self.base:
                    if self.current_position == self.util[(self.util.index(self.accurate) + 1) % 4]:
                        self.valid = self.current_position
                    else:
                        self.valid = self.accurate
                else:
                    if self.idle == self.util[(self.util.index(self.current_position) + 1) % 4]:
                        self.valid = self.idle
                    else:
                        self.valid = self.current_position
                self.record.append((self.valid, True))
                self.record.append(((self.base+3)%6, True))
                self.record.append(((self.base+3)%6, True))
                self.record.append((self.valid, False))
                self.record.append(self.final_vertices)
                func = self.algorithm
            elif self.current_position == (self.base+3)%6:
                if self.idle == self.crayon and self.accurate == self.color:
                    if self.idle == self.util[(self.util.index(self.accurate) + 1) % 4]:
                        self.valid = self.idle
                    else:
                        self.valid = self.accurate
                    self.record.append((self.valid, True))
                    self.record.append(((self.base+3)%6, True))
                    self.record.append(((self.base+3)%6, True))
                    self.record.append((self.valid, False))
                    self.record.append(self.final_vertices)
                    func = self.algorithm
                else:
                    self.ra = ((self.base + 3) % 6, True)
                    self.undo = self.final_vertices
                    func = self.PendingMoves
                    if self.step_sequence:
                        self.step_sequence = False
                        self.update_value()
            else:
                if self.idle == (self.base+3)%6:
                    self.valid = self.accurate
                    self.controller = self.crayon
                else:
                    self.valid = self.idle
                    self.controller = self.color
                if self.valid == self.controller:
                    if self.current_position == self.util[(self.util.index(self.valid) + 1) % 4]:
                        self.record.append(((self.base+3)%6, False))
                        self.record.append((self.valid, False))
                        self.record.append(((self.base+3)%6, True))
                        self.record.append((self.valid, True))
                        self.record.append(self.final_vertices)
                        func = self.algorithm
                    else:
                        self.record.append(((self.base+3)%6, True))
                        self.record.append((self.valid, True))
                        self.record.append(((self.base+3)%6, False))
                        self.record.append((self.valid, False))
                        self.record.append(self.final_vertices)
                        func = self.algorithm
                else:
                    self.ra = ((self.base + 3) % 6, True)
                    self.undo = self.final_vertices
                    func = self.PendingMoves
                    if self.step_sequence:
                        self.step_sequence = False
                        self.update_value()
            if self.open:
                self.window.after(0, func)


    # Places edge pieces that belong on the middle layer where they should go
    def middle(self):
        if self.rule == 0:
            zero = 0
            while zero < 24:
                if self.robot_cube[self.p_a[zero][0]][self.p_a[zero + 1][0]] == self.crayon and \
                        self.robot_cube[self.p_a[zero][1]][self.p_a[zero + 1][1]] == self.color:
                    self.accurate = self.p_a[zero][0]
                    self.idle = self.p_a[zero][1]
                    zero = 24
                elif self.robot_cube[self.p_a[zero][0]][self.p_a[zero + 1][0]] == self.color and \
                        self.robot_cube[self.p_a[zero][1]][self.p_a[zero + 1][1]] == self.crayon:
                    self.idle = self.p_a[zero][0]
                    self.accurate = self.p_a[zero][1]
                    zero = 24
                else:
                    zero += 2
            if self.idle == self.base or self.accurate == self.base:
                if self.idle == self.base:
                    self.valid = self.accurate
                    self.controller = self.crayon
                    self.other = self.color
                else:
                    self.valid = self.idle
                    self.controller = self.color
                    self.other = self.crayon
                if self.valid == self.controller:
                    if self.other == self.util[(self.util.index(self.controller) + 1) % 4]:
                        self.record.append((self.base, True))
                        self.record.append((self.other, True))
                        self.record.append((self.base, False))
                        self.record.append((self.other, False))
                        self.record.append((self.base, False))
                        self.record.append((self.controller, False))
                        self.record.append((self.base, True))
                        self.record.append((self.controller, True))
                        self.record.append(self.middle)
                    else:
                        self.record.append((self.base, False))
                        self.record.append((self.other, False))
                        self.record.append((self.base, True))
                        self.record.append((self.other, True))
                        self.record.append((self.base, True))
                        self.record.append((self.controller, True))
                        self.record.append((self.base, False))
                        self.record.append((self.controller, False))
                        self.record.append(self.middle)
                    func = self.algorithm
                else:
                    self.ra = (self.base, True)
                    self.undo = self.middle
                    func = self.PendingMoves
                    if self.step_sequence:
                        self.step_sequence = False
                        self.update_value()
            else:
                if self.idle != self.color or self.accurate != self.crayon:
                    if self.idle == self.util[(self.util.index(self.accurate) + 1) % 4]:
                        self.controller = self.accurate
                        self.other = self.idle
                    else:
                        self.controller = self.idle
                        self.other = self.accurate
                    self.record.append((self.base, True))
                    self.record.append((self.other, True))
                    self.record.append((self.base, False))
                    self.record.append((self.other, False))
                    self.record.append((self.base, False))
                    self.record.append((self.controller, False))
                    self.record.append((self.base, True))
                    self.record.append((self.controller, True))
                    self.record.append(self.middle)
                    func = self.algorithm
                else:
                    if self.move_counter < 3:
                        self.move_counter += 1
                        self.color = self.util[self.move_counter]
                        self.crayon = self.util[(self.move_counter + 1) % 4]
                        func = self.middle
                    else:
                        func = self.cross
            if self.open:
                self.window.after(0, func)


    # Makes a cross with the edges on the bottom face
    def cross(self):
        if self.rule == 0:
            p_1 = self.robot_cube[self.base][1]
            p_3 = self.robot_cube[self.base][3]
            p_5 = self.robot_cube[self.base][5]
            p_7 = self.robot_cube[self.base][7]
            if p_1 == p_3 == p_5 == p_7:
                func = self.corners
            elif p_1 == p_7 or p_3 == p_5:
                if p_1 == p_7:
                    self.valid = self.a_d[(self.base, 3)]
                else:
                    self.valid = self.a_d[(self.base, 1)]
                self.other = self.util[(self.util.index(self.valid) + 1) % 4]
                self.record.append((self.valid, True))
                self.record.append((self.other, True))
                self.record.append((self.base, True))
                self.record.append((self.other, False))
                self.record.append((self.base, False))
                self.record.append((self.valid, False))
                self.record.append(self.cross)
                func = self.algorithm
            else:
                if p_1 == p_3:
                    if self.a_d[(self.base, 1)] == self.util[(self.util.index(self.a_d[(self.base, 3)]) + 1) % 4]:
                        self.valid = self.a_d[(self.base, 5)]
                    else:
                        self.valid = self.a_d[(self.base, 7)]
                elif p_5 == p_7:
                    if self.a_d[(self.base, 5)] == self.util[(self.util.index(self.a_d[(self.base, 7)]) + 1) % 4]:
                        self.valid = self.a_d[(self.base, 1)]
                    else:
                        self.valid = self.a_d[(self.base, 3)]
                elif p_3 == p_7:
                    if self.a_d[(self.base, 3)] == self.util[(self.util.index(self.a_d[(self.base, 7)]) + 1) % 4]:
                        self.valid = self.a_d[(self.base, 1)]
                    else:
                        self.valid = self.a_d[(self.base, 5)]
                elif p_1 == p_5:
                    if self.a_d[(self.base, 1)] == self.util[(self.util.index(self.a_d[(self.base, 5)]) + 1) % 4]:
                        self.valid = self.a_d[(self.base, 3)]
                    else:
                        self.valid = self.a_d[(self.base, 7)]
                else:
                    self.valid = (self.base + 1) % 6
                self.other = self.util[(self.util.index(self.valid) + 1) % 4]
                self.record.append((self.valid, True))
                self.record.append((self.base, True))
                self.record.append((self.other, True))
                self.record.append((self.base, False))
                self.record.append((self.other, False))
                self.record.append((self.valid, False))
                self.record.append(self.cross)
                func = self.algorithm
            if self.open:
                self.window.after(0, func)


    # Solves the bottom face so that it is one color
    def corners(self):
        if self.rule == 0:
            p_0 = self.robot_cube[self.base][0]
            p_2 = self.robot_cube[self.base][2]
            p_6 = self.robot_cube[self.base][6]
            p_8 = self.robot_cube[self.base][8]
            if p_0 == p_2 == p_6 == p_8:
                func = self.penultimate
            else:
                self.move_counter = 0
                if p_0 == self.base:
                    self.move_counter+=1
                if p_2 == self.base:
                    self.move_counter+=1
                if p_6 == self.base:
                    self.move_counter+=1
                if p_8 == self.base:
                    self.move_counter+=1
                if self.move_counter == 2:
                    zero = 0
                    while zero < 4:
                        face_1 = self.right_side[self.base][zero]
                        face_2 = self.right_side[self.base][(zero+1)%4]
                        one = 0
                        while one < 16:
                            if face_1 in self.p_v[one] and face_2 in self.p_v[one] and self.base in self.p_v[one]:
                                finish = self.p_v[one+1][self.p_v[one].index(face_1)]
                                one = 16
                            else:
                                one += 2
                        if self.robot_cube[face_1][finish] == self.base:
                            zero = 4
                            self.valid = (face_2 + 3) % 6
                        else:
                            zero += 1
                elif self.move_counter == 0:
                    zero = 0
                    while zero < 4:
                        face_1 = self.right_side[self.base][zero]
                        face_2 = self.right_side[self.base][(zero-1)%4]
                        one = 0
                        while one < 16:
                            if face_1 in self.p_v[one] and face_2 in self.p_v[one] and self.base in self.p_v[one]:
                                finish = self.p_v[one+1][self.p_v[one].index(face_1)]
                                one = 16
                            else:
                                one += 2
                        if self.robot_cube[face_1][finish] == self.base:
                            zero = 4
                            self.valid = (face_1 + 3) % 6
                        else:
                            zero += 1
                elif p_0 == self.base:
                    self.valid = (self.v_d[(self.base, 0)][0] + 3) % 6
                elif p_2 == self.base:
                    self.valid = (self.v_d[(self.base, 2)][0] + 3) % 6
                elif p_6 == self.base:
                    self.valid = (self.v_d[(self.base, 6)][0] + 3) % 6
                else:
                    self.valid = (self.v_d[(self.base, 8)][0] + 3) % 6
                self.record.append((self.valid, True))
                self.record.append((self.base, True))
                self.record.append((self.valid, False))
                self.record.append((self.base, True))
                self.record.append((self.valid, True))
                self.record.append((self.base, True))
                self.record.append((self.base, True))
                self.record.append((self.valid, False))
                self.record.append(self.corners)
                func = self.algorithm
            if self.open:
                self.window.after(0, func)


    # Places the corner pieces that are on the bottom layer where they belong
    def penultimate(self):
        if self.rule == 0:
            list = []
            self.move_counter = 0
            for zero in range(4):
                face = self.right_side[self.base][zero]
                if self.robot_cube[face][self.from_right_side[self.base][zero][0]] == face:
                    self.move_counter += 1
                    list.append(face)
                if self.robot_cube[face][self.from_right_side[self.base][zero][2]] == face:
                    self.move_counter += 1
                    list.append(face)
            if self.move_counter == 8:
                func = self.Ultimate
            elif self.move_counter > 3:
                if list.count(list[0]) == 2:
                    self.valid = list[0]
                elif list.count(list[1]) == 2:
                    self.valid = list[1]
                elif list.count(list[2]) == 2:
                    self.valid = list[2]
                else:
                    self.valid = list[3]
                self.other = self.util[(self.util.index(self.valid) - 1) % 4]
                self.record.append((self.other, False))
                self.record.append(((self.valid + 3) % 6, True))
                self.record.append((self.other, False))
                self.record.append((self.valid, True))
                self.record.append((self.valid, True))
                self.record.append((self.other, True))
                self.record.append(((self.valid + 3) % 6, False))
                self.record.append((self.other, False))
                self.record.append((self.valid, True))
                self.record.append((self.valid, True))
                self.record.append((self.other, True))
                self.record.append((self.other, True))
                self.record.append((self.base, False))
                self.record.append(self.penultimate)
                func = self.algorithm
            else:
                self.ra = (self.base, True)
                self.undo = self.penultimate
                func = self.PendingMoves
                if self.step_sequence:
                    self.step_sequence = False
                    self.update_value()
            if self.open:
                self.window.after(0, func)


    # Places the edge pieces that are on the bottom layer where they belong. This complete's the Rubiks Cube.
    def Ultimate(self):
        if self.rule == 0:
            list = []
            move_counter = 0
            for zero in range(4):
                face = self.right_side[self.base][zero]
                if self.robot_cube[face][self.from_right_side[self.base][zero][1]] == face:
                    move_counter += 1
                    list.append(face)
            if move_counter == 4:
                self.interval = 180
                self.resolver.configure(text="Solve")
                self.rapid.configure(bg="#A0FFFF", relief="raised")
                self.rule = 1
            else:
                if move_counter == 0:
                    valid = self.util[0]
                    other = self.util[1]
                    declaration = True
                else:
                    valid = (list[0] + 3) % 6
                    other = self.util[(self.util.index(valid) + 1) % 4]
                    position = self.right_side[self.base].index(other)
                    declaration = (valid == self.robot_cube[other][self.from_right_side[self.base][position][1]])
                self.record.append((valid, True))
                self.record.append((valid, True))
                self.record.append((self.base, declaration))
                self.record.append(((other+3)%6, True))
                self.record.append((other, False))
                self.record.append((valid, True))
                self.record.append((valid, True))
                self.record.append(((other+3)%6, False))
                self.record.append((other, True))
                self.record.append((self.base, declaration))
                self.record.append((valid, True))
                self.record.append((valid, True))
                self.record.append(self.Ultimate)
                if self.open:
                    self.window.after(0, self.algorithm)



    #           BUTTONS AND CONTROLS

    # Decides what function to call based on where the screen is clicked. It is responsible for determining whether the
    # user is dragging the cube as well as any button clicks (when the Instruction menu is closed).
    def mouse(self, event):
        if self.open:
            x_coordinate = self.window.winfo_pointerx() - self.window.winfo_rootx()
            y_coordinate = self.window.winfo_pointery() - self.window.winfo_rooty()
            if -1 < x_coordinate < 512 and -1 < y_coordinate < 512:
                if self.activate:
                    self.activate = False
                    self.window.unbind("<Motion>")
                else:
                    self.activate = True
                    self.x = self.window.winfo_pointerx()
                    self.y = self.window.winfo_pointery()
                    self.window.bind("<Motion>", self.interpretor)
            elif 559 < y_coordinate < 595:
                declaration = False
                if 51 < x_coordinate < 168:
                    declaration = True
                    self.intstructions.configure(bg="#70C8C8", relief="flat")
                    func = self.mini_i
                elif 217 < x_coordinate < 288:
                    declaration = True
                    self.resolver.configure(bg="#70C8C8", relief="flat")
                    func = self.Intro
                elif 338 < x_coordinate < 459 and self.rule == 1:
                    declaration = True
                    self.rapid.configure(bg="#70C8C8", relief="flat")
                    func = self.rapid
                if declaration and self.open:
                    self.window.after(144, func)


    # This is the "drag" function. It rotates the cube based on the direction in which the mouse moves.
    def interpretor(self, event):
        if self.open:
            if self.rg == None and ((abs(self.x - self.window.winfo_pointerx()) >= 2 or
                                     abs(self.y - self.window.winfo_pointery()) >= 2)):
                self.rule_mini = False
                length_x = self.window.winfo_pointerx() - self.x
                length_y = self.window.winfo_pointery() - self.y
                self.x = self.window.winfo_pointerx()
                self.y = self.window.winfo_pointery()
                if length_x != 0:
                    if length_x < 0:
                        conv_x = 1
                    else:
                        conv_x = -1
                    if length_y < 0:
                        conv_y = -1
                    else:
                        conv_y = 1
                    far = (length_y ** 2 + length_x ** 2) ** 0.5
                    self.rg = (0.05, conv_y * abs(length_y/far), conv_x * abs(length_x/far))
                elif length_y < 0:
                    self.rg = (0.05, -1, 0)
                else:
                    self.rg = (0.05, 1, 0)
                self.rule_mini = True
                if self.step_sequence and self.open:
                    self.step_sequence = False
                    self.window.after(0, self.update_value)


    # Opens and closes the Instruction menu. Also activates and deactivates buttons and key presses accordingly.
    def intstructions(self):
        if self.rule_mini and self.open:
            self.rule = 1
            self.interval = 180
            self.record = []
            self.resolver.configure(text="Solve")
            self.rapid.configure(bg="#A0FFFF", relief="raised")
            self.activate = False
            self.window.unbind("<Motion>")
            self.window.unbind("<Button-1>")
            self.window.unbind("<space>")
            self.window.unbind("<Return>")
            self.window.unbind("2")
            self.window.unbind("3")
            self.window.unbind("c")
            self.window.unbind("x")
            self.window.unbind("r")
            self.window.unbind("f")
            self.window.unbind("q")
            self.window.unbind("a")
            self.window.unbind("e")
            self.window.unbind("w")
            self.window.unbind("d")
            self.window.unbind("s")
            self.window.unbind("@")
            self.window.unbind("#")
            self.window.unbind("C")
            self.window.unbind("X")
            self.window.unbind("R")
            self.window.unbind("F")
            self.window.unbind("Q")
            self.window.unbind("A")
            self.window.unbind("E")
            self.window.unbind("W")
            self.window.unbind("D")
            self.window.unbind("S")
            self.space.delete("all")
            self.window.bind("<Button-1>", self.advance)
            self.space.pack_forget()
            self.s_som.place_forget()
            self.p_som.place_forget()
            self.resolver.place_forget()
            self.rapid.place_forget()
            self.texts.configure(text=self.page_1)
            self.button_de_page.configure(text="Next")
            self.beyond.place(height=482, width=482, y=15, x=15)
            self.perfil.place(height=480, width=480, y=16, x=16)
            self.texts.place(height=464, width=464, y=24, x=24)
            self.before_limit.place(height=466, width=466, y=23, x=23)
            self.perfil.lift()
            self.before_limit.lift()
            self.texts.lift()
            self.button_de_page.place(height=31, width=55, y=436, x=408)
            self.button_de_page.lift()
            self.i_som.place(height=37, width=78, y=45, x=215)
            self.intstructions.place(height=35, width=76, y=46, x=216)
            self.intstructions.configure(text="Return")
            self.window.update()
            self.rule_mini = False
        elif self.open:
            self.beyond.place_forget()
            self.perfil.place_forget()
            self.texts.place_forget()
            self.before_limit.place_forget()
            self.button_de_page.place_forget()
            if self.button_de_page["text"] == "Back":
                self.typing_0.place_forget()
                self.typing_1.place_forget()
                self.typing_2.place_forget()
                self.typing_3.place_forget()
            self.space.pack()
            self.window.unbind("<Button-1>")
            self.button()
            self.i_som.place(height=37, width=116, y=45, x=50)
            self.s_som.place(height=37, width=70, y=45, x=216)
            self.p_som.place(height=37, width=122, y=45, x=336)
            self.intstructions.place(height=35, width=114, y=46, x=51)
            self.intstructions.lift()
            self.resolver.place(height=35, width=68, y=46, x=217)
            self.resolver.lift()
            self.rapid.place(height=35, width=120, y=46, x=337)
            self.rapid.lift()
            self.intstructions.configure(text="Instructions")
            self.create()
            self.window.update()
            self.rule_mini = True


    # Determines what button is clicked when the Instruction menu is up
    def advance(self, event):
        if self.open:
            x_coordinate = self.window.winfo_pointerx() - self.window.winfo_rootx()
            y_coordinate = self.window.winfo_pointery() - self.window.winfo_rooty()
            declaration = False
            if 435 < y_coordinate < 467 and 407 < x_coordinate < 463:
                declaration = True
                self.button_de_page.configure(bg="#00D0D0")
                func = self.mini_bdp
            elif 559 < y_coordinate < 595 and 217 < x_coordinate < 294:
                declaration = True
                self.intstructions.configure(bg="#70C8C8", relief="flat")
                func = self.mini_i
            if declaration and self.open:
                self.window.after(144, func)


    # Changes the page when the "Next" or "Back" button is clicked
    def mini_bdp(self):
        self.button_de_page.configure(bg="#00FFFF")
        if self.button_de_page["text"] == "Next" and self.open:
            self.texts.configure(text=self.page_2)
            self.button_de_page.configure(text="Back")
            self.typing_0.lift()
            self.typing_1.lift()
            self.typing_2.lift()
            self.typing_3.lift()
            self.typing_0.place(x=225, y=77)
            self.typing_1.place(x=183, y=107)
            self.typing_2.place(x=183, y=137)
            self.typing_3.place(x=225, y=167)
            self.window.update()
        elif self.open:
            self.texts.configure(text=self.page_1)
            self.button_de_page.configure(text="Next")
            self.typing_0.place_forget()
            self.typing_1.place_forget()
            self.typing_2.place_forget()
            self.typing_3.place_forget()


    # Closes the instruction menu after "Return" is clicked
    def mini_i(self):
        self.intstructions.configure(bg="#A0FFFF", relief="raised")
        if self.open:
            self.window.after(0, self.intstructions)


    # Activates when "Solve" is clicked. Starts the AI solving process (with animation).
    def Intro(self):
        self.resolver.configure(bg="#A0FFFF", relief="raised")
        if self.rule == 0 and self.resolver["text"] == "Stop":
            self.rule = 1
            if self.interval == 0:
                self.min_size = False
                self.interval = 180
            self.record = []
            self.resolver.configure(text="Solve")
            self.rapid.configure(bg="#A0FFFF", relief="raised")
        elif self.rule == 1:
            self.resolver.configure(text="Stop")
            self.rapid.configure(bg="#70C8C8", relief="flat")
            if self.open:
                self.window.after(0, self.start)


    # Activates when "Quick Solve" is clicked. Starts the AI solving process (without animation).
    def rapid(self):
        self.resolver.configure(text="Stop")
        self.interval = 0
        if self.open:
            self.window.after(0, self.start)


    # Scrambles the cube when the space key is pressed
    def Scramble(self, event):
        if self.rule == 1:
            self.rule = 0
            for zero in range(144):
                self.rotate_side(random.randrange(6), random.choice([True, False]))
            if self.step_sequence:
                self.create()
            self.rule = 1


    # Changes the lighting effects when the Enter key is pressed
    def Brightness(self, event):
        if self.contrast:
            self.contrast = False
            self.conversion = ["#FFFFFF", "#0080FF", "#FF0000", "#FFFF00", "#00FF80", "#FF9000"]
        else:
            self.contrast = True
            self.conversion = ["#C0C0C0", "#0060C0", "#C00000", "#C0C000", "#00C060", "#C06C00"]
        if self.step_sequence and self.open:
            self.window.after(0, self.create)


    # The following twelve commands are named after their respective keys. The instructions explain what they do.

    def E(self, event):
        if self.rule == 1 and self.ra == None:
            self.rule = 2
            number = self.flag[2]
            self.ra = (number, True)
            if self.step_sequence and self.open:
                self.window.after(0, self.update_value)

    def W(self, event):
        if self.rule == 1 and self.ra == None:
            self.rule = 2
            number = self.flag[2]
            self.ra = (number, False)
            if self.step_sequence and self.open:
                self.window.after(0, self.update_value)

    def D(self, event):
        if self.rule == 1 and self.ra == None:
            self.rule = 2
            number = (self.flag[2] + 3) % 6
            self.ra = (number, False)
            if self.step_sequence and self.open:
                self.window.after(0, self.update_value)

    def S(self, event):
        if self.rule == 1 and self.ra == None:
            self.rule = 2
            number = (self.flag[2] + 3) % 6
            self.ra = (number, True)
            if self.step_sequence and self.open:
                self.window.after(0, self.update_value)

    def X(self, event):
        if self.rule == 1 and self.ra == None:
            self.rule = 2
            self.manual_control()
            number = self.ay
            self.ra = (number, True)
            if self.step_sequence and self.open:
                self.window.after(0, self.update_value)

    def N2(self, event):
        if self.rule == 1 and self.ra == None:
            self.rule = 2
            self.manual_control()
            number = self.ay
            self.ra = (number, False)
            if self.step_sequence and self.open:
                self.window.after(0, self.update_value)

    def N3(self, event):
        if self.rule == 1 and self.ra == None:
            self.rule = 2
            self.manual_control()
            number = (self.ay + 3) % 6
            self.ra = (number, True)
            if self.step_sequence and self.open:
                self.window.after(0, self.update_value)

    def C(self, event):
        if self.rule == 1 and self.ra == None:
            self.rule = 2
            self.manual_control()
            number = (self.ay + 3) % 6
            self.ra = (number, False)
            if self.step_sequence and self.open:
                self.window.after(0, self.update_value)

    def Q(self, event):
        if self.rule == 1 and self.ra == None:
            self.rule = 2
            self.manual_control()
            number = self.facemba
            self.ra = (number, True)
            if self.step_sequence and self.open:
                self.window.after(0, self.update_value)

    def R(self, event):
        if self.rule == 1 and self.ra == None:
            self.rule = 2
            self.manual_control()
            number = self.facemba
            self.ra = (number, False)
            if self.step_sequence and self.open:
                self.window.after(0, self.update_value)

    def F(self, event):
        if self.rule == 1 and self.ra == None:
            self.rule = 2
            self.manual_control()
            number = (self.facemba + 3) % 6
            self.ra = (number, True)
            if self.step_sequence and self.open:
                self.window.after(0, self.update_value)

    def A(self, event):
        if self.rule == 1 and self.ra == None:
            self.rule = 2
            self.manual_control()
            number = (self.facemba + 3) % 6
            self.ra = (number, False)
            if self.step_sequence and self.open:
                self.window.after(0, self.update_value)



    #           SETUP

    # Assigns commands to onscreen buttons and creates text boxes. It is only called once at the beginning.
    def primary_button(self):
        color = "#A0FFFF"
        crayon = "#FFFFFF"
        self.intstructions = tk.Label(self.frame, font = ("Helvetica", font_size), bg=color, relief="raised", bd=3,
                                      text="Instructions")
        self.resolver = tk.Label(self.frame, font=("Helvetica", font_size), bg=color, text="Solve", relief="raised", bd=3)
        self.rapid = tk.Label(self.frame, font=("Helvetica", font_size), text="Quick Solve", bg=color, relief="raised", bd=3)
        self.i_som = tk.Label(self.frame, bg="#000000")
        self.i_som.place(height=37, width=116, y=45, x=50)
        self.s_som = tk.Label(self.frame, bg="#000000")
        self.s_som.place(height=37, width=70, y=45, x=216)
        self.p_som = tk.Label(self.frame, bg="#000000")
        self.p_som.place(height=37, width=122, y=45, x=336)
        self.intstructions.place(height=35, width=114, y=46, x=51)
        self.intstructions.lift()
        self.resolver.place(height=35, width=68, y=46, x=217)
        self.resolver.lift()
        self.rapid.place(height=35, width=120, y=46, x=337)
        self.rapid.lift()
        self.beyond = tk.Label(self.case, bg="#000000")
        self.before_limit = tk.Label(self.case, bg="#000000")
        self.button_de_page = tk.Label(self.case, font=("Helvetica", 15), bg="#00FFFF", bd=2, relief="raised")
        self.perfil = tk.Label(self.case, bg="#FFA000")
        self.typing_0 = tk.Label(self.case, font=("Courier", 15), bg=crayon, text="2  3")
        self.typing_1 = tk.Label(self.case, font=("Courier", 15), bg=crayon, text="Q  W  E  R")
        self.typing_2 = tk.Label(self.case, font=("Courier", 15), bg=crayon, text="A  S  D  F")
        self.typing_3 = tk.Label(self.case, font=("Courier", 15), bg=crayon, text="X  C")
        self.texts = tk.Label(self.case, font=("Helvetica", 14), bg=crayon, fg="#000000", justify=tk.LEFT)

    # Assigns commands to key presses and the screen click. It is called once at the beginning and whenever the
    # instruction menu is closed.
    def button(self):
        self.window.bind("<Button-1>", self.mouse)
        self.window.bind("<space>", self.Scramble)
        self.window.bind("<Return>", self.Brightness)
        self.window.bind("2", self.N2)
        self.window.bind("3", self.N3)
        self.window.bind("c", self.C)
        self.window.bind("x", self.X)
        self.window.bind("r", self.R)
        self.window.bind("f", self.F)
        self.window.bind("q", self.Q)
        self.window.bind("a", self.A)
        self.window.bind("e", self.E)
        self.window.bind("w", self.W)
        self.window.bind("d", self.D)
        self.window.bind("s", self.S)
        self.window.bind("@", self.N2)
        self.window.bind("#", self.N3)
        self.window.bind("C", self.C)
        self.window.bind("X", self.X)
        self.window.bind("R", self.R)
        self.window.bind("F", self.F)
        self.window.bind("Q", self.Q)
        self.window.bind("A", self.A)
        self.window.bind("E", self.E)
        self.window.bind("W", self.W)
        self.window.bind("D", self.D)
        self.window.bind("S", self.S)


    # Creates and stores data required for the program, most of which is numerical. It is only called once at the
    # beginning. Note that locations of points on the cube are recorded as quaternions, with i, j, k values acting as
    # x, y, z coordinates. Sometimes a real value of 0 will precede these coordinates; this only occurs when doing so
    # aids in quaternion multiplication. The instructions are also written here.
    def system(self):
        self.open = True
        self.step_sequence = True
        self.rg = None
        self.ra = None
        self.undo = None
        self.rule = 1
        self.rule_mini = True
        self.min_size = True
        self.contrast = True
        self.activate = False
        self.circumference = 0
        self.interval = 180
        self.record = []
        self.conversion = ["#C0C0C0", "#0060C0", "#C00000", "#C0C000", "#00C060", "#C06C00"]
        self.robot_cube = [[0]*9, [1]*9, [2]*9, [3]*9, [4]*9, [5]*9]
        self.transition = [False]*6
        self.faces = [[0, 2, 6, 4], [0, 1, 3, 2], [0, 1, 5, 4], [1, 3, 7, 5], [4, 5, 7, 6], [2, 3, 7, 6]]
        self.block = [[0, 6, 18, 12], [2, 5, 11, 8], [1, 4, 16, 13], [3, 9, 21, 15], [14, 17, 23, 20], [7, 10, 22, 19]]
        self.right_side = [[1, 2, 4, 5], [3, 2, 0, 5], [0, 1, 3, 4], [5, 4, 2, 1], [5, 0, 2, 3], [4, 3, 1, 0]]
        self.from_right_side = [[[2, 1, 0], [0, 1, 2], [0, 1, 2], [2, 1, 0]],
                               [[6, 3, 0], [6, 3, 0], [0, 3, 6], [0, 3, 6]],
                               [[2, 1, 0], [0, 3, 6], [0, 1, 2], [6, 3, 0]],
                               [[6, 7, 8], [8, 7, 6], [8, 7, 6], [6, 7, 8]],
                               [[2, 5, 8], [2, 5, 8], [8, 5, 2], [8, 5, 2]],
                               [[2, 5, 8], [8, 7, 6], [8, 5, 2], [6, 7, 8]]]
        self.p_a = ((0, 1), (3, 1), (0, 2), (1, 1), (0, 4), (5, 1), (0, 5), (7, 1), (1, 2), (3, 3), (1, 5), (5, 3),
                    (4, 2), (3, 5), (4, 5), (5, 5), (3, 1), (3, 7), (3, 2), (1, 7), (3, 4), (5, 7), (3, 5), (7, 7))
        self.p_v = ((0, 1, 2), (0, 0, 0), (3, 1, 2), (0, 6, 6), (0, 4, 2), (2, 0, 2), (3, 4, 2), (2, 6, 8),
                    (0, 1, 5), (6, 2, 0), (3, 1, 5), (6, 8, 6), (0, 4, 5), (8, 2, 2), (3, 4, 5), (8, 8, 8))
        self.a_d = {(0, 3): 1, (1, 1): 0, (0, 1): 2, (2, 1): 0, (0, 5): 4, (4, 1): 0, (0, 7): 5, (5, 1): 0,
                    (1, 3): 2, (2, 3): 1, (1, 5): 5, (5, 3): 1, (4, 3): 2, (2, 5): 4, (4, 5): 5, (5, 5): 4,
                    (3, 3): 1, (1, 7): 3, (3, 1): 2, (2, 7): 3, (3, 5): 4, (4, 7): 3, (3, 7): 5, (5, 7): 3}
        self.v_d = {(0, 0): (2, 1), (1, 0): (0, 2), (2, 0): (1, 0), (3, 0): (1, 2), (1, 6): (2, 3), (2, 6): (3, 1),
                    (0, 2): (4, 2), (4, 0): (2, 0), (2, 2): (0, 4), (3, 2): (2, 4), (4, 6): (3, 2), (2, 8): (4, 3),
                    (0, 6): (1, 5), (1, 2): (5, 0), (5, 0): (0, 1), (3, 6): (5, 1), (1, 8): (3, 5), (5, 6): (1, 3),
                    (0, 8): (5, 4), (4, 2): (0, 5), (5, 2): (4, 0), (3, 8): (4, 5), (4, 8): (5, 3), (5, 8): (3, 4)}
        self.vectors = [[0, 0, 0, -1], [0, -1, 0, 0], [0, 0, -1, 0], [0, 0, 0, 1], [0, 1, 0, 0], [0, 0, 1, 0]]
        self.centro = 0.3840410272734564
        b = 0.5773502691896257
        i = 0.5464207904830386
        m = 0.2165063509461097
        c = 0.1649572197684645
        g = 0.1907317853572871
        self.vertex = []
        self.edge = []
        for zero in range(-1, 2, 2):
            for one in range(-1, 2, 2):
                for two in range(-1, 2, 2):
                    self.vertex.append([0, zero * b, one * b, two * b])
                    self.edge.append([0, zero * b, one * b, two * g])
                    self.edge.append([0, zero * b, one * g, two * b])
                    self.edge.append([0, zero * g, one * b, two * b])
        self.positions = [[
                [[-i, -i, -b], [-m, -i, -b], [-m, -m, -b], [-i, -m, -b]],
                [[-c, -i, -b], [c, -i, -b], [c, -m, -b], [-c, -m, -b]],
                [[i, -i, -b], [m, -i, -b], [m, -m, -b], [i, -m, -b]],
                [[-i, -c, -b], [-m, -c, -b], [-m, c, -b], [-i, c, -b]],
                [[-c, -c, -b], [c, -c, -b], [c, c, -b], [-c, c, -b]],
                [[i, -c, -b], [m, -c, -b], [m, c, -b], [i, c, -b]],
                [[-i, i, -b], [-m, i, -b], [-m, m, -b], [-i, m, -b]],
                [[-c, i, -b], [c, i, -b], [c, m, -b], [-c, m, -b]],
                [[i, i, -b], [m, i, -b], [m, m, -b], [i, m, -b]]
            ], [
                [[-b, -i, -i], [-b, -m, -i], [-b, -m, -m], [-b, -i, -m]],
                [[-b, -c, -i], [-b, c, -i], [-b, c, -m], [-b, -c, -m]],
                [[-b, i, -i], [-b, m, -i], [-b, m, -m], [-b, i, -m]],
                [[-b, -i, -c], [-b, -m, -c], [-b, -m, c], [-b, -i, c]],
                [[-b, -c, -c], [-b, c, -c], [-b, c, c], [-b, -c, c]],
                [[-b, i, -c], [-b, m, -c], [-b, m, c], [-b, i, c]],
                [[-b, -i, i], [-b, -m, i], [-b, -m, m], [-b, -i, m]],
                [[-b, -c, i], [-b, c, i], [-b, c, m], [-b, -c, m]],
                [[-b, i, i], [-b, m, i], [-b, m, m], [-b, i, m]]
            ], [
                [[-i, -b, -i], [-m, -b, -i], [-m, -b, -m], [-i, -b, -m]],
                [[-c, -b, -i], [c, -b, -i], [c, -b, -m], [-c, -b, -m]],
                [[i, -b, -i], [m, -b, -i], [m, -b, -m], [i, -b, -m]],
                [[-i, -b, -c], [-m, -b, -c], [-m, -b, c], [-i, -b, c]],
                [[-c, -b, -c], [c, -b, -c], [c, -b, c], [-c, -b, c]],
                [[i, -b, -c], [m, -b, -c], [m, -b, c], [i, -b, c]],
                [[-i, -b, i], [-m, -b, i], [-m, -b, m], [-i, -b, m]],
                [[-c, -b, i], [c, -b, i], [c, -b, m], [-c, -b, m]],
                [[i, -b, i], [m, -b, i], [m, -b, m], [i, -b, m]]
            ], [
                [[-i, -i, b], [-m, -i, b], [-m, -m, b], [-i, -m, b]],
                [[-c, -i, b], [c, -i, b], [c, -m, b], [-c, -m, b]],
                [[i, -i, b], [m, -i, b], [m, -m, b], [i, -m, b]],
                [[-i, -c, b], [-m, -c, b], [-m, c, b], [-i, c, b]],
                [[-c, -c, b], [c, -c, b], [c, c, b], [-c, c, b]],
                [[i, -c, b], [m, -c, b], [m, c, b], [i, c, b]],
                [[-i, i, b], [-m, i, b], [-m, m, b], [-i, m, b]],
                [[-c, i, b], [c, i, b], [c, m, b], [-c, m, b]],
                [[i, i, b], [m, i, b], [m, m, b], [i, m, b]]
            ], [
                [[b, -i, -i], [b, -m, -i], [b, -m, -m], [b, -i, -m]],
                [[b, -c, -i], [b, c, -i], [b, c, -m], [b, -c, -m]],
                [[b, i, -i], [b, m, -i], [b, m, -m], [b, i, -m]],
                [[b, -i, -c], [b, -m, -c], [b, -m, c], [b, -i, c]],
                [[b, -c, -c], [b, c, -c], [b, c, c], [b, -c, c]],
                [[b, i, -c], [b, m, -c], [b, m, c], [b, i, c]],
                [[b, -i, i], [b, -m, i], [b, -m, m], [b, -i, m]],
                [[b, -c, i], [b, c, i], [b, c, m], [b, -c, m]],
                [[b, i, i], [b, m, i], [b, m, m], [b, i, m]]
            ], [
                [[-i, b, -i], [-m, b, -i], [-m, b, -m], [-i, b, -m]],
                [[-c, b, -i], [c, b, -i], [c, b, -m], [-c, b, -m]],
                [[i, b, -i], [m, b, -i], [m, b, -m], [i, b, -m]],
                [[-i, b, -c], [-m, b, -c], [-m, b, c], [-i, b, c]],
                [[-c, b, -c], [c, b, -c], [c, b, c], [-c, b, c]],
                [[i, b, -c], [m, b, -c], [m, b, c], [i, b, c]],
                [[-i, b, i], [-m, b, i], [-m, b, m], [-i, b, m]],
                [[-c, b, i], [c, b, i], [c, b, m], [-c, b, m]],
                [[i, b, i], [m, b, i], [m, b, m], [i, b, m]]
            ]]
        self.page_1 = \
"""Click the screen to start dragging the cube. Click again
to stop. (Drag at a fairly slow pace for better results.)

Click "Solve" to tell the computer to solve the cube
while showing every move it makes.

Click "Quick Solve" to tell the computer to solve the
cube in seconds. The methods used by "Solve" and
"Quick Solve" are the same, but "Quick Solve" does
not create complex animations.

Press the Space key to scramble the cube.

Press the Enter key to change the lighting effects. One
version creates a shadow, while the other only displays
bright colors.

See the next page for rotating each face of the cube
manually.\n\n"""
        self.page_2 = \
"""It may help to think of the following keys as forming a   
grid on your keyboard:\n\n\n\n\n\n
2:  turns the left side up
3:  turns the right side up
Q:  turns the top side left
W:  turns the front face counter-clockwise
E:  turns the front face clockwise
R:  turns the top side right
A:  turns the bottom side left
S:  turns the back face counter-clockwise
D:  turns the back face clockwise
F:  turns the bottom side right
X:  turns the left side down
C:  turns the right side down\n"""



# Calls the function at the very top of the script, which sets everything into motion.
principal()
