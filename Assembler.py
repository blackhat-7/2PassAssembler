
class Main:

    literal_table = pseudo_table = mot_table = []
    sym_table = op_table = dict()

    def main(self) :
        self.pass_one()

    def pass_one(self) :
        file = open("input.txt" ,"r")

        location_counter = 0
        self.initialize__tables()

        if file.mode == 'r':

            for line in file :
                length = 0
                op_type = 0
                opcode = ""

                if line[:5] == "START":
                    location_counter = int(line[6:])

                if line[:3] == "END":
                    self.rewind_temp_for_pass_two()
                    self.sort_literal_table()
                    self.remove_redundant_literals()
                    break

                elif self.line_is_no_comment(line):
                    symbol = self.check_for_symbol(line)
                    if symbol is not None:
                        self.enter_new_symbol(symbol ,location_counter)

                    literal = self.check_for_literal(line)
                    if literal is not None:
                        self.enter_new_literal(literal)

                    opcode = self.extract_opcode(line)
                    op_type = self.search_opcode_table(opcode)
                    if op_type < 0:
                        op_type = self.search_pseudo_table(opcode)

                    if op_type == 1:
                        length = 3
                    elif op_type == 2:
                        length = 3 * int(symbol)
                    elif op_type == 3:
                        length = int(symbol)
                    elif op_type == 4:
                        length = 1

                self.write_temp_file(op_type, opcode, length, line)
                location_counter += length

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
                self.op_table[i[:3]] = i[4:]

        self.pseudo_table = ["WORD", "RESW", "RESB", "BYTE"]

    @staticmethod
    def line_is_no_comment(line):
        if line[:2] == "/*":
            return False
        return True

    @staticmethod
    def check_for_symbol(line):
        if line[0] == "L":
            x = line.index(":")
            sym = line[:x]
            return sym
        return None

    def enter_new_symbol(self, symbol, location_counter):
        self.sym_table[symbol] = location_counter

    @staticmethod
    def check_for_literal(line):
        if line[:4] == "    ":
            if line[8] != "L" and line[7] == " " and line[8] != " ":
                return line[8:]
            if line[8] != "L" and line[7] != " ":
                return line[9:]

        return None

    def enter_new_literal(self, literal):
        self.literal_table.append(literal)

    @staticmethod
    def extract_opcode(line):
        if line[4] != "T" and line[4] != " ":
            return line[4:7]
        return None

    def search_opcode_table(self, opcode):
        try:
            op = self.op_table[opcode]
            return 0
        except KeyError:
            return -1

    def search_pseudo_table(self, opcode):
        return self.pseudo_table.index(opcode) + 1

    @staticmethod
    def get_length_of_type(line):
        return 0

    @staticmethod
    def write_temp_file(type, opcode, length, line):
        file = open("op_table.txt", "w")
        if file.mode == 'w':
            file.write(type + " " + opcode + " " + length + " " + line)

    # def rewind_temp_for_pass_two(self):
    #
    # def sort_literal_table(self):
    #
    # def remove_redundant_literals(self):
    #
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
