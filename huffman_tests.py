import unittest
import filecmp
import subprocess
from huffman import *

class TestList(unittest.TestCase):
    def test_cnt_freq(self):
        freqlist = cnt_freq("file2.txt")
        anslist = [2, 4, 8, 16, 0, 2, 0] 
        self.assertListEqual(freqlist[97:104], anslist)

        freqlist = cnt_freq('empty_file.txt')
        anslist = [0] * 256
        self.assertEqual(freqlist,anslist)

    def test_cnt_freq_error(self):
        with self.assertRaises(FileNotFoundError):
            cnt_freq('ddafd.txt')


    def test_comes_before(self):
        a = HuffmanNode(97,40) #a
        b = HuffmanNode(98,30) #b
        self.assertFalse(comes_before(a,b))
        a = HuffmanNode(113,20) #q
        b = HuffmanNode(101,53) #e
        self.assertTrue(comes_before(a,b))
        a = HuffmanNode(100,30) #d
        b = HuffmanNode(102,30) #f
        self.assertTrue(comes_before(a,b))
        a = HuffmanNode(102,30) #f
        b = HuffmanNode(100,30) #d
        self.assertFalse(comes_before(a,b))
        a = HuffmanNode(105,22) #i
        b = HuffmanNode(104,3567) #h
        self.assertTrue(comes_before(a,b))


    def test_combine(self):
        a = HuffmanNode(97,40) #a
        b = HuffmanNode(98,30) #b
        c = combine(a,b)
        self.assertEqual(c.freq,70)
        self.assertEqual(c.char,97)
        self.assertEqual(c.left.char,98)
        self.assertEqual(c.right.char,97)
        self.assertEqual(c.left.freq,30)
        self.assertEqual(c.right.freq,40)
        a = HuffmanNode(113,20) #q
        b = HuffmanNode(101,53) #e
        c = combine(a,b)
        self.assertEqual(c.freq,73)
        self.assertEqual(c.char,101)
        self.assertEqual(c.left.char,113)
        self.assertEqual(c.right.char,101)
        self.assertEqual(c.left.freq,20)
        self.assertEqual(c.right.freq,53)
        a = HuffmanNode(102,30) #f
        b = HuffmanNode(100,30) #d
        c = combine(a,b)
        self.assertEqual(c.freq,60)
        self.assertEqual(c.char,100)
        self.assertEqual(c.left.char,100)
        self.assertEqual(c.right.char,102)
        self.assertEqual(c.left.freq,30)
        self.assertEqual(c.right.freq,30)
        a = HuffmanNode(105,22) #i
        b = HuffmanNode(104,3567) #h
        c = combine(a,b)
        self.assertEqual(c.freq,3589)
        self.assertEqual(c.char,104)
        self.assertEqual(c.left.char,105)
        self.assertEqual(c.right.char,104)
        self.assertEqual(c.left.freq,22)
        self.assertEqual(c.right.freq,3567)


    def test_create_huff_tree(self):
        freqlist = cnt_freq("file2.txt")
        hufftree = create_huff_tree(freqlist)
        self.assertEqual(hufftree.freq, 32)
        self.assertEqual(hufftree.char, 97)
        left = hufftree.left
        self.assertEqual(left.freq, 16)
        self.assertEqual(left.char, 97)
        right = hufftree.right
        self.assertEqual(right.freq, 16)
        self.assertEqual(right.char, 100)

        freqlist = cnt_freq('empty_file.txt')
        hufftree = create_huff_tree(freqlist)
        self.assertEqual(hufftree, None)

        freqlist = cnt_freq('multiline.txt')
        hufftree = create_huff_tree(freqlist)
        self.assertEqual(hufftree.freq,56)
        self.assertEqual(hufftree.char,10)
        left = hufftree.left
        self.assertEqual(left.freq,24)
        self.assertEqual(left.char,10)
        right = hufftree.right
        self.assertEqual(right.freq,32)
        self.assertEqual(right.char,32)

        freqlist = cnt_freq('declaration.txt')
        hufftree = create_huff_tree(freqlist)
        self.assertEqual(hufftree.freq,8226)
        self.assertEqual(hufftree.char,10)
        left = hufftree.left
        self.assertEqual(left.freq,3529)
        self.assertEqual(left.char,38)
        right = hufftree.right
        self.assertEqual(right.freq,4697)
        self.assertEqual(right.char,10)

        freqlist = cnt_freq('file1.txt')
        hufftree = create_huff_tree(freqlist)
        self.assertEqual(hufftree.freq,13)
        self.assertEqual(hufftree.char,32)
        left = hufftree.left
        self.assertEqual(left.freq,6)
        self.assertEqual(left.char,32)
        right = hufftree.right
        self.assertEqual(right.freq,7)
        self.assertEqual(right.char,97) 

        freqlist = cnt_freq('single_char.txt')
        hufftree = create_huff_tree(freqlist)
        self.assertEqual(hufftree.freq,18)
        self.assertEqual(hufftree.char,100)
        left = hufftree.left
        self.assertEqual(left,None)
        right = hufftree.right
        self.assertEqual(right,None)


    def test_create_header(self):
        freqlist = cnt_freq("file2.txt")
        self.assertEqual(create_header(freqlist), "97 2 98 4 99 8 100 16 102 2")
        
        freqlist = cnt_freq('multiline.txt')
        self.assertEqual(create_header(freqlist),'10 2 32 8 46 1 84 1 97 3 101 5 102 2 104 2 105 7 108 5 109 2 110 4 111 1 112 3 115 3 116 3 117 2 119 1 120 1')

        freqlist = cnt_freq('declaration.txt')
        self.assertEqual(create_header(freqlist),'10 166 32 1225 38 1 39 1 44 109 45 3 46 36 49 1 52 1 54 1 55 2 58 10 59 10 65 22 66 7 67 19 68 5 69 3 70 17 71 15 72 24 73 8 74 5 75 1 76 15 77 3 78 8 79 6 80 23 82 9 83 23 84 15 85 3 87 13 97 466 98 88 99 171 100 253 101 875 102 169 103 116 104 331 105 451 106 12 107 13 108 216 109 144 110 487 111 518 112 116 113 6 114 420 115 460 116 640 117 211 118 74 119 84 120 9 121 82 122 4')

        freqlist = cnt_freq('empty_file.txt')
        self.assertEqual(create_header(freqlist),'')

        freqlist = cnt_freq('file1.txt')
        self.assertEqual(create_header(freqlist),'32 3 97 4 98 3 99 2 100 1')

        freqlist = cnt_freq('single_char.txt')
        self.assertEqual(create_header(freqlist),'100 18')

    def test_create_code(self):
        freqlist = cnt_freq("file2.txt")
        hufftree = create_huff_tree(freqlist)
        codes = create_code(hufftree)
        self.assertEqual(codes[ord('d')], '1')
        self.assertEqual(codes[ord('a')], '0000')
        self.assertEqual(codes[ord('f')], '0001')

        freqlist = cnt_freq('empty_file.txt')
        hufftree = create_huff_tree(freqlist)
        codes = create_code(hufftree)
        self.assertEqual(codes, ['']*256)

        freqlist = cnt_freq('multiline.txt')
        hufftree = create_huff_tree(freqlist)
        codes = create_code(hufftree)
        self.assertEqual(codes, ['', '', '', '', '', '', '', '', '', '', '00101', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '101', '', '', '', '', '', '', '', '', '', '', '', '', '', '011100', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '011101', '', '', '', '', '', '', '', '', '', '', '', '', '0011', '', '', '', '1111', '01111', '', '11000', '100', '', '', '000', '11001', '1101', '111000', '0100', '', '', '0101', '0110', '11101', '', '111001', '00100', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''])

        freqlist = cnt_freq('declaration.txt')
        hufftree = create_huff_tree(freqlist)
        codes = create_code(hufftree)
        self.assertEqual(codes,['', '', '', '', '', '', '', '', '', '', '111100', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '110', '', '', '', '', '', '0100101110000', '0100101110001', '', '', '', '', '000001', '00000000010', '10011101', '', '', '0100101110010', '', '', '0100101110011', '', '0100101110100', '010010111011', '', '', '1011010100', '1011010101', '', '', '', '', '', '101101011', '0100100011', '101101001', '10011100011', '00000000011', '100111001', '010010100', '00000011', '0100101111', '0000000000', '0100101110101', '010010101', '00000000100', '1001110000', '0000000011', '00000001', '', '1011010000', '00000010', '010010110', '00000000101', '', '010010010', '', '', '', '', '', '', '', '', '', '0111', '1111111', '111110', '10010', '001', '111101', '010011', '10111', '0101', '010010000', '010010011', '01000', '101100', '1000', '1010', '100110', '0100100010', '0001', '0110', '1110', '00001', '1001111', '1111110', '1011010001', '1011011', '10011100010', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''])

        freqlist = cnt_freq('file1.txt')
        hufftree = create_huff_tree(freqlist)
        codes = create_code(hufftree)
        self.assertEqual(codes,['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '00', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '11', '01', '101', '100', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''])

        freqlist = cnt_freq('single_char.txt')
        hufftree = create_huff_tree(freqlist)
        codes = create_code(hufftree)
        self.assertEqual(codes, ['']*256)

    def test_given_textfiles(self):
        huffman_encode("file1.txt", "file1_out.txt")
        # capture errors by running 'diff' on your encoded file with a *known* solution file
        err = subprocess.call("diff -wb file1_out.txt file1_soln.txt", shell = True)
        self.assertEqual(err, 0)
        err = subprocess.call("diff -wb file1_out_compressed.txt file1_compressed_soln.txt", shell = True)
        self.assertEqual(err, 0)


        huffman_encode('file2.txt','file2_out.txt')
        err = subprocess.call('diff -wb file2_out.txt file2_soln.txt', shell = True)
        self.assertEqual(err,0)
        err = subprocess.call('diff -wb file2_out_compressed.txt file2_compressed_soln.txt', shell = True)
        self.assertEqual(err,0)

        huffman_encode('multiline.txt','multiline_out.txt')
        err = subprocess.call('diff -wb multiline_out_compressed.txt multiline_compressed_soln.txt', shell = True)
        self.assertEqual(err,0)
        err = subprocess.call('diff -wb multiline_out.txt multiline_soln.txt', shell = True)
        self.assertEqual(err,0)


        huffman_encode('declaration.txt','declaration_out.txt')
        err = subprocess.call('diff -wb declaration_out_compressed.txt declaration_compressed_soln.txt', shell = True)
        self.assertEqual(err,0)
        err = subprocess.call('diff -wb declaration_out.txt declaration_soln.txt', shell = True)
        self.assertEqual(err,0)


    def test_improper_input(self):
        with self.assertRaises(FileNotFoundError):
            huffman_encode('ddafd.txt','ddafd_out.txt')
        with self.assertRaises(FileNotFoundError):
            huffman_encode('asdf.txt','asdf_out.txt')

    def test_my_own_textfiles(self):
        huffman_encode('single_char.txt','single_char_out.txt')
        err = subprocess.call('diff -wb single_char_out_compressed.txt single_char_compressed_soln.txt', shell = True)
        self.assertEqual(err,0)
        err = subprocess.call('diff -wb single_char_out.txt single_char_soln.txt', shell = True)
        self.assertEqual(err,0)

        huffman_encode('empty_file.txt','empty_file_out.txt')
        err = subprocess.call('diff -wb empty_file_out_compressed.txt empty_file_compressed_soln.txt', shell = True)
        self.assertEqual(err,0)
        err = subprocess.call('diff -wb empty_file_out.txt empty_file_soln.txt', shell = True)
        self.assertEqual(err,0)

    def test_01a_test_file1_parse_header(self):
        f = open('file1_compressed_soln.txt', 'rb')
        header = f.readline()        
        f.close()
        expected = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, \
                    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, \
                    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 3, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, \
                    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, \
                    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, \
                    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, \
                    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.compare_freq_counts(parse_header(header), expected)
        
    def compare_freq_counts(self, freq, exp):
        for i in range(256):
            stu = 'Frequency for ASCII ' + str(i) + ': ' + str(freq[i])
            ins = 'Frequency for ASCII ' + str(i) + ': ' + str(exp[i])
            self.assertEqual(stu, ins)
            
    def test_01_test_file1_decode(self):
        huffman_decode("file1_compressed_soln.txt", "file1_decoded.txt")
        err = subprocess.call("diff -wb file1.txt file1_decoded.txt", shell = True)
        self.assertEqual(err, 0)

        huffman_decode('file2_compressed_soln.txt','file2_decoded.txt')
        err = subprocess.call("diff -wb file2.txt file2_decoded.txt", shell = True)
        self.assertEqual(err, 0)

        huffman_decode('declaration_compressed_soln.txt','declaration_decoded.txt')
        err = subprocess.call("diff -wb declaration.txt declaration_decoded.txt", shell = True)
        self.assertEqual(err, 0)

        huffman_decode('empty_file_compressed_soln.txt','empty_file_decoded.txt')
        err = subprocess.call("diff -wb empty_file.txt empty_file_decoded.txt", shell = True)
        self.assertEqual(err, 0)

        huffman_decode('single_char_compressed_soln.txt','single_char_decoded.txt')
        err = subprocess.call("diff -wb single_char.txt single_char_decoded.txt", shell = True)
        self.assertEqual(err, 0)

        huffman_decode('multiline_compressed_soln.txt','multiline_decoded.txt')
        err = subprocess.call("diff -wb multiline.txt multiline_decoded.txt", shell = True)
        self.assertEqual(err, 0)


    def test_decode_errors(self):
        with self.assertRaises(FileNotFoundError):
            huffman_decode('ddafajldfjksldafadffd_compressed_soln.txt','ddaaldsfkjlasdffd_decoded.txt')
        with self.assertRaises(FileNotFoundError):
            huffman_decode('asasdfjlaksdfdf_compressed_soln.txt','asdlasdjfkljasldkff_decoded.txt')
        with self.assertRaises(FileNotFoundError):
            huffman_decode('invalid_compressed_soln.txt','invalid_decoded.txt')


    def test_parse_file(self):
        header = '32 3 97 4 98 3 99 2 100 1'
        self.assertEqual(parse_header(header),[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 3, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])

        header = '10 166 32 1225 38 1 39 1 44 109 45 3 46 36 49 1 52 1 54 1 55 2 58 10 59 10 65 22 66 7 67 19 68 5 69 3 70 17 71 15 72 24 73 8 74 5 75 1 76 15 77 3 78 8 79 6 80 23 82 9 83 23 84 15 85 3 87 13 97 466 98 88 99 171 100 253 101 875 102 169 103 116 104 331 105 451 106 12 107 13 108 216 109 144 110 487 111 518 112 116 113 6 114 420 115 460 116 640 117 211 118 74 119 84 120 9 121 82 122 4'
        self.assertEqual(parse_header(header),[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 166, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1225, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 109, 3, 36, 0, 0, 1, 0, 0, 1, 0, 1, 2, 0, 0, 10, 10, 0, 0, 0, 0, 0, 22, 7, 19, 5, 3, 17, 15, 24, 8, 5, 1, 15, 3, 8, 6, 23, 0, 9, 23, 15, 3, 0, 13, 0, 0, 0, 0, 0, 0, 0, 0, 0, 466, 88, 171, 253, 875, 169, 116, 331, 451, 12, 13, 216, 144, 487, 518, 116, 6, 420, 460, 640, 211, 74, 84, 9, 82, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])

        header = '10 2 32 8 46 1 84 1 97 3 101 5 102 2 104 2 105 7 108 5 109 2 110 4 111 1 112 3 115 3 116 3 117 2 119 1 120 1'
        self.assertEqual(parse_header(header),[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 5, 2, 0, 2, 7, 0, 0, 5, 2, 4, 1, 3, 0, 0, 3, 3, 2, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])

        header = ''
        self.assertEqual(parse_header(header),[0]*256)

        header = '100 18'
        self.assertEqual(parse_header(header),[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 18, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])


if __name__ == '__main__': 
   unittest.main()
