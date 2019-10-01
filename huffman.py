from huffman_bit_writer import *
from huffman_bit_reader import *
class HuffmanNode:
    def __init__(self, char, freq):
        self.char = char   # stored as an integer - the ASCII character code value
        self.freq = freq   # the freqency associated with the node
        self.left = None   # Huffman tree (node) to the left
        self.right = None  # Huffman tree (node) to the right

    def set_left(self, node):
        self.left = node

    def set_right(self, node):
        self.right = node


def comes_before(a, b):
    """Returns True if tree rooted at node a comes before tree rooted at node b, False otherwise"""
    if a.freq < b.freq:
        return True
    elif a.freq == b.freq:
        if a.char < b.char:
            return True
        else:
            return False
    return False


def combine(a, b):
    """Creates and returns a new Huffman node with children a and b, with the "lesser node" on the left
    The new node's frequency value will be the sum of the a and b frequencies
    The new node's char value will be the lesser of the a and b char ASCII values"""
    if a.freq < b.freq:
        if a.char < b.char:
            c = HuffmanNode(a.char,a.freq+b.freq)
        elif b.char < a.char:
            c = HuffmanNode(b.char,a.freq+b.freq)
        c.set_left(a)
        c.set_right(b)
    elif b.freq < a.freq:
        if a.char < b.char:
            c = HuffmanNode(a.char,a.freq+b.freq)
        #elif b.char < a.char:
            #c = HuffmanNode(b.char,a.freq+b.freq)
        c.set_left(b)
        c.set_right(a)
    elif a.freq == b.freq:
        if a.char < b.char:
            c = HuffmanNode(a.char,a.freq+b.freq)
            c.set_left(a)
            c.set_right(b)
        elif b.char < a.char:
            c = HuffmanNode(b.char,a.freq+b.freq)
            c.set_left(b)
            c.set_right(a)
    return c

    #simpler way if a always less than b
    '''c = HuffmanNode(a.char,a.freq+b.freq)
    c.set_left(a)
    c.set_right(b)
    return c'''


def cnt_freq(filename):
    """Opens a text file with a given file name (passed as a string) and counts the 
    frequency of occurrences of all the characters within that file"""
    try:
        fin = open(filename,'r')
        final = [0]*256
        for line in fin:
            for char in line:
                final[ord(char)] += 1
        fin.close()
        return final
    except:
        raise FileNotFoundError


def create_huff_tree(char_freq):
    """Create a Huffman tree for characters with non-zero frequency
    Returns the root node of the Huffman tree"""
    
    tree = []
    for i in range(len(char_freq)):
        if char_freq[i] != 0:
            tree.append(HuffmanNode(i,char_freq[i]))
    if len(tree) == 0:
        return None
    else:
        tree.sort(key=lambda x: x.freq, reverse = False)
        while len(tree) > 1:
            new = combine(tree[0],tree[1])
            tree.append(new)
            tree.pop(0)
            tree.pop(0)
            tree.sort(key=lambda x: (x.freq,x.char), reverse = False)

    final_tree = tree[0]
    return final_tree 


def create_code(node):
    """Returns an array (Python list) of Huffman codes. For each character, use the integer ASCII representation 
    as the index into the arrary, with the resulting Huffman code for that character stored at that location"""
    codes = [''] * 256
    if node is None:
        return codes
    create_code_helper('', node, codes)
    return codes


def create_code_helper(code,current,codes):
    if current.right is not None and current.left is not None:
        create_code_helper(code + '0', current.left, codes)
        create_code_helper(code + '1', current.right, codes)
    else:
        codes[current.char] = code


def create_header(freqs):
    """Input is the list of frequencies. Creates and returns a header for the output file
    Example: For the frequency list asscoaied with "aaabbbbcc, would return “97 3 98 4 99 2” """
    temp = []
    for i in range(len(freqs)):
        if freqs[i] != 0:
            temp.append(str(i))
            temp.append(str(freqs[i]))
    return ' '.join(temp)


def huffman_encode(in_file, out_file):
    """Takes inout file name and output file name as parameters - both files will have .txt extensions
    Uses the Huffman coding process on the text from the input file and writes encoded text to output file
    Also creates a second output file which adds _compressed before the .txt extension to the name of the file.
    This second file is actually compressed by writing individual 0 and 1 bits to the file using the utility methods 
    provided in the huffman_bits_io module to write both the header and bits.
    Take not of special cases - empty file and file with only one unique character"""
    try:
        fin = open(in_file,'r')
        fout = open(out_file,'w')
    except:
        raise FileNotFoundError
    char_freq = cnt_freq(in_file)
    tree = create_huff_tree(char_freq)
    codes = create_code(tree)
    header = create_header(char_freq)
    if tree is None:
        fin.close()
        fout.close()
        compfilename = ''
        i = 0
        while out_file[i] != '.':
            compfilename += out_file[i]
            i += 1
        compfilename += '_compressed.txt'

        bit = HuffmanBitWriter(compfilename)
        bit.close()

    elif tree.left is None and tree.right is None and tree is not None:
        fout.write(header)
        fout.write('\n')
        fin.close()
        fout.close()
        compfilename = ''
        i = 0
        while out_file[i] != '.':
            compfilename += out_file[i]
            i += 1
        compfilename += '_compressed.txt'
        bit = HuffmanBitWriter(compfilename)
        bit.write_str(header)
        bit.write_str('\n')
        bit.close()

    else:
        fout.write(header)
        fout.write('\n')
        stringz = ''
        for line in fin:
            for char in line:
                val = ord(char)
                fout.write(codes[val])
                stringz += codes[val]

        compfilename = ''
        i = 0
        while out_file[i] != '.':
            compfilename += out_file[i]
            i += 1
        compfilename += '_compressed.txt'
        
        bit = HuffmanBitWriter(compfilename)
        bit.write_str(header)
        bit.write_str('\n')
        bit.write_code(stringz)
        bit.close()


        fin.close()
        fout.close()


def parse_header(header_string):
    freqs = [0] * 256
    header = header_string.split()
    i = 0
    while i<len(header):
        temp = header[i]
        temp = int(temp)
        freqs[temp] = int(header[(i+1)])
        i += 2
    return freqs


def huffman_decode(encoded_file,decode_file):
    try:
        fin = open(encoded_file,'r')
        fout = open(decode_file,'w')
    except:
        raise FileNotFoundError

    bit = HuffmanBitReader(encoded_file)
    header_string = str(bit.read_str())
    header_string = str(header_string[2:-3])
    freqs = parse_header(header_string)
    tree = create_huff_tree(freqs)

    if tree is None:
        fin.close()
        bit.close()
        fout.close()

    elif tree.left is None and tree.right is None and tree is not None:
        char_num = 0
        for val in range(len(freqs)):
            char_num += freqs[val]
            if freqs[val] != 0:
                ascii_val = val
        final = chr(ascii_val) * char_num
        fout.write(final)
        fin.close()
        bit.close()
        fout.close()

    elif tree.left is not None and tree.right is not None:
        char_num = 0
        for val in freqs:
            char_num += val
        final = ''
        i = 0
        while i < char_num:
            current = tree
            while current.left is not None and current.right is not None:
                temp = bit.read_bit()
                if temp is True:
                    current = current.right
                elif temp is False:
                    current = current.left
            final += str(chr(current.char))
            i += 1
        fout.write(final)
        fout.close()
        bit.close()
        fin.close()
