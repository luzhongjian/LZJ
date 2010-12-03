QUESTION_TYPE_TAG = u'[t]'
INDEX_TAG = u'[i]'
QUESTION_TAG = u'[q]'
CHOICE_NUM_TAG = u'[n]'
CHOICE_TAG = u'[c]'
VALUE_TAG = u'[v]'

import re

RE_QUESTION_TYPE_TAG = re.compile('^\[t\]')
RE_INDEX_TAG = re.compile('^\[i\]')
RE_QUESTION_TAG = re.compile('^\[q\]')
RE_CHOICE_NUM_TAG = re.compile('^\[n\]')
RE_CHOICE_TAG = re.compile('^\[c\]')
RE_VALUE_TAG = re.compile('^\[v\]')

save_seq = ('t','n','v','i','q','c')


def getline(fileName):
    return fileName.readline()

def getChunk(fileName, startTag, endTag, needFirstLine, needLastLine):
    """get one block from file fileName according to tags startTand and endTag"""
    chunk = []
    reach_current_chunk = False
    reach_next_chunk = False
    while True:
        if reach_next_chunk:
            break
        sourceFileOffset = fileName.tell()
        line = getline(fileName)
        if len(line) != 0:
            if line == u'\r\n' or line == u'\n':
               continue
            else:
                if line.startswith(startTag):
                    if not reach_current_chunk:
                        if needFirstLine:
                            chunk.extend([line.strip()])
                            #print line
                        reach_current_chunk = True
                    else:
                        reach_next_chunk = True
                elif endTag and line.startswith(endTag):
                    if needLastLine:
                        chunk.extend([line.strip()])
                    break
                else:
                    if reach_current_chunk:
                        chunk.extend([line.strip()])
                        #print line
        else:
            break
    #print chunk
    return chunk

def line_parse(line):
    if line.startswith(QUESTION_TYPE_TAG):
        return 't'
    elif line.startswith(INDEX_TAG):
        return 'i'
    elif line.startswith(QUESTION_TAG):
        return 'q'
    elif line.startswith(CHOICE_NUM_TAG):
        return 'n'
    elif line.startswith(CHOICE_TAG):
        return 'c'
    elif line.startswith(VALUE_TAG):
        return 'v'

    #if re.match(RE_QUESTION_TYPE_TAG, line):
    #    return 't'
    #elif re.match(RE_INDEX_TAG, line):
    #    return 'i'
    #elif re.match(RE_QUESTION_TAG, line):
    #    return 'q'
    #elif re.match(RE_CHOICE_NUM_TAG, line):
    #    print "n"
    #    return 'n'
    #elif re.match(RE_CHOICE_TAG, line):
    #    return 'c'
    #elif re.match(RE_VALUE_TAG, line):
    #    return 'v'

from struct import pack  
def chunk_transmit_and_save(genFile, chunk):
    n = 0
    iterater = 0
    qType = 'c'
    offset = 0
    indexLen = 0
    questionLen = 1
    valueLen = 0
    choices = []
    choiceLen = []
    removedPackChunk = []
    #tempLine = ''
    
    for line in chunk:
        tag = line_parse(line)
        if tag == 't':
            tempLine = line.lstrip(QUESTION_TYPE_TAG)
            qType = tempLine[0]
            #removedPackChunk.extend(tempLine)
        elif tag == 'n':
            tempLine = line.lstrip(CHOICE_NUM_TAG)
            n = int(tempLine)
            #removedPackChunk.extend(tempLine)
        elif tag == 'i':
            tempLine = line.lstrip(INDEX_TAG)
            indexLen = len(tempLine) * 2
            removedPackChunk.extend([tempLine])
        elif tag == 'q':
            tempLine = line.lstrip(QUESTION_TAG)
            questionLen = len(tempLine) * 2
            removedPackChunk.extend([tempLine])
            print removedPackChunk
        elif tag == 'c':
            tempLine = line.lstrip(CHOICE_TAG)
            choices.extend([tempLine])
            choiceLen.extend([len(tempLine) * 2])
            removedPackChunk.extend([tempLine])
        elif tag == 'v':
            tempLine = line.lstrip(VALUE_TAG)
            if not len(tempLine):
                valueLen = 0
            else:
                valueLen = int(tempLine)
            removedPackChunk.extend([tempLine])
            
    offset = 8 * 2 + 4 * n
    for tag in save_seq:
        if tag == 't':
            genFile.write(pack('H',ord(qType)))
            print ord(qType)
        elif tag == 'n':
            genFile.write(pack('H', n))
            print n
        elif tag == 'i':
            genFile.write(pack('HH', offset, indexLen))
            offset += indexLen
        elif tag == 'q':
            genFile.write(pack('HH', offset, questionLen))
            offset += questionLen
        elif tag == 'c':
            while iterater < n:
                genFile.write(pack('HH', offset, choiceLen[iterater]))
                offset += choiceLen[iterater]
                iterater += 1
        elif tag == 'v':
            genFile.write(pack('HH', offset, valueLen))
            offset += valueLen
    #print chunk
    removedPackChunk = ''.join(removedPackChunk)
    #genFile.write(''.join(removedPackChunk))
    genFile.write(removedPackChunk.encode('utf-16le'))

import codecs
def generate_exercise_file():
    source_f = codecs.open(r'E:\MerlionColor Related\exercise.txt', 'r', 'utf-16')
    result_f = open(r'E:\MerlionColor Related\exerciseResult.bin', 'wb')
    index_f = open(r'E:\MerlionColor Related\exerciseIndex.bin', 'wb')

    questionN = 0
    index_f.seek(4, 0)
    block = getChunk(source_f, u'<h>', u'<\h>', False, False)
    block = ''.join(block)
    result_f.write(block.encode('utf-16le'))
    
    #result_f.write(''.join(block))
    block = getChunk(source_f, u'[t]', u'[e]', True, False)    
    while block:
        result_file_offset = result_f.tell()
        str_offset = pack('i', result_file_offset)
        index_f.write(str_offset)
        chunk_transmit_and_save(result_f, block)
        questionN += 1
        block = getChunk(source_f, u'[t]', u'[e]', True, False)
    #print block

    index_f.seek(0, 0)
    str_QN = pack('i', questionN)
    index_f.write(str_QN)
    
    source_f.close()
    result_f.close()
    index_f.close()

def test_look_result(i):
    result_f = open(r'E:\MerlionColor Related\exerciseResult.txt', 'r')
    index_f = open(r'E:\MerlionColor Related\exerciseIndex.txt', 'r')
    offset = index_f.read(4)
    #if EOFError == offset
    print offset
    result_f.close()
    index_f.close()
    
if __name__ == '__main__':
    generate_exercise_file()
    #test_look_result(1)
    
