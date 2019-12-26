

class iBin():
    bin=0;
    bits=[];

    def __init__(self, b_int=0):
        self.reset;
        self.bits = [];
        if b_int > 0: 
            self.bin = b_int;
        else: self.bin = 0;
        

    def reset(self):
        self.bin = 0;
        self.bits.clear();
    
    def get_bin(self):
        return self.bin;

    def get_binary_rep(self):
        return bin(self.bin)

    def get_set_count(self):
        return bin(self.bin).count("1");
    
    def get_bit_length(self):
        return self.bin.bit_length();
    
    def set_bit(self, bit_position):
        self.bits.append(bit_position)
        
        if (bit_position > 40):
            pos = bit_position - 40;            

        else: pos = bit_position;
        bit_posn = 40 - pos;

        mask = 1 << bit_posn

        self.bin = self.bin | mask;
    
    def is_set(self, bit_position):
        is_set = False;

    def to_string(self):
        return '{0:040b}'.format(self.bin)
