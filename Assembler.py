class Assembler:
    label_table, literal_table, firstPassTable = [], [], []
    sym_table,  op_table = dict(), dict()

    @staticmethod
    def main():
        assembler = Assembler()
        assembler.pass_one()

    def pass_one(self):
        input_file = open("input.txt", "r")
        temp_file = open("temp.txt", "w")
        temp_file.close()
        location_counter = 0
        pass1final = []
        symbol = ""
        self.initialize__tables()

        if input_file.mode == 'r':

            for line in input_file:
                pass1Code = []
                length = 0
                op_type = 0
                opcode = ""

                if line[:5] == "START":
                    location_counter = int(line[6:])

                elif line[:3] == "END":
                    # self.rewind_temp_for_pass_two()
                    # self.sort_literal_table()
                    self.remove_redundant_literals()
                    break

                elif self.line_is_no_comment(line):

                    opcode = self.extract_opcode(line)
                    op_type = self.search_opcode_table(opcode)
                    pass1Code.append(['OP', op_type])
                    if int(op_type) < 0:
                        op_type = self.search_pseudo_table(opcode)

                    if op_type == 1:
                        length = 3
                    elif op_type == 2:
                        length = 3 * int(symbol)
                    elif op_type == 3:
                        length = int(symbol)
                    elif op_type == 4:
                        length = 1

                    variable = self.check_for_variable(line)
                    if variable is not None:
                        self.enter_new_variable(variable, location_counter)

                    label = self.check_for_label(line)
                    if label is not None:
                        self.enter_new_label(label, location_counter)
                        pass1Code.append(['ST', label])

                    pass1Code.append(variable)
                    location_counter += 1

                pass1final.append(pass1Code)

        for line in pass1final:
            print(line)
        print(self.sym_table)

    # def pass_two(self) :
    #     more_input = True
    #     line, opcode = ""
    #     location_counter, length, type = 0
    #     END_STATEMENT = -2
    #     MAX_CODE = 16

    #     file = open('temp.txt', 'r')
    #     if (file.mode == 'r') :
    #         for line in file :
    #             type = self.read_type()
    #             opcode = self.read_opcode()
    #             length = self.read_length()
    #             line = self.read_line()

    #             if (type!=0) :
    #                 if (type==1) :
    #                     self.eval_type1(opcode, length, line, code)
    #                 elif (type==2) :
    #                     self.eval_type2(opcode, length, line, code)
    #                 #other case

    #             self.write_output(code)
    #             self.write_listing(code, line)
    #             location_counter += length

    #             if (type=="END_STATEMENT") :
    #                 more_input = False
    #                 finish_up()

    def initialize__tables(self):
        file = open("op_table.txt", "r")
        if file.mode == 'r':
            for i in file.readlines():
                self.op_table[i[:3]] = i[4:-1]

        self.pseudo_table = ["WORD", "RESW", "RESB", "BYTE"]

    @staticmethod
    def line_is_no_comment(line):
        return not (line[0] == ";")

    def check_for_label(self, line):
        if line[0] == "L":
            x = line.index(":")
            lit = line[:x]
            return lit
        return None

    def enter_new_label(self, label, location_counter):
        if label not in self.label_table:
            self.sym_table[label] = ['L', location_counter]

    def check_for_variable(self, line):
        try:
            if line[7] == " " and line[8] != " ":
                x = line[8:-1]
                return x
            if line[7] != " ":
                x = line[9:-1]
                return x
        except IndexError:
            return None
        return None

    def enter_new_variable(self, variable, location_counter):
        if variable is not "" and variable not in self.sym_table.keys():
            if variable[0] != "L":
                self.sym_table[variable] = ['V', location_counter]

    @staticmethod
    def extract_opcode(line):
        if line[4] != "T" and line[4] != " ":
            return line[4:7]
        return None

    def search_opcode_table(self, opcode):
        try:
            op = self.op_table[opcode]
            return op
        except KeyError:
            return -1

    def search_pseudo_table(self, opcode):
        return self.pseudo_table.index(opcode) + 1

    @staticmethod
    def write_temp_file(op_type, opcode, length, line):
        file = open("temp.txt", "a")
        if file.mode == 'a':
            file.write(str(op_type) + " " + opcode + " " + str(length) + " " + line)

    # def rewind_temp_for_pass_two(self):
    #
    # def sort_literal_table(self):
    #
    def remove_redundant_literals(self):
        self.literal_table = list(dict.fromkeys(self.literal_table))
        return self.literal_table

    # def read_type(self):
    #
    # def read_opcode(self):
    #
    # def read_length(self):
    #
    # def read_line(self):
    #
    # def eval_type1(self, opcode, length, line, code):
    #
    # def write_output(self, code):
    #
    # def write_listing(self, code, line):
    #
    # def finish_up(self):


if __name__ == '__main__':
    Assembler.main()
