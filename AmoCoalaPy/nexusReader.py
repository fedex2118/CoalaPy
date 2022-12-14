from ete3 import PhyloTree
from collections import defaultdict

import sys
import constants as c

def __fetchPairString(pairString):
    """_summary_ 
    Function called to get [Parasyte,Host] pair and store it into a list.

    Args:
        pairString (_type_ "String"): _description_ line "Parasyte: Host"

    Returns:
        _type_: _description_ A list that contains the name of parasyte on first position
        and the host name in second position:
        [Parasyte, Host]
    """
    nPair = pairString.replace(c.TAB, "").replace(c.SPACE, "").replace(c.COMMA, "").replace(c.NEW_LINE, "")
    return nPair.split(c.COLONS)

def nexusReader(filename):
    """_summary_
    
    THE METHOD AS IT IS RIGHT NOW WORKS UNTIL 'END;' BLOCK IS READ;
    EVERYTHING THAT IS WRITTEN AFTERWARDS WON'T BE READ (JUST TO BE EFFICIENT).
    
    New lines are separators of BEGIN BLOCKS.
    Every other type of separator '\t', words, characters will throw an assertion error.

    Args:
        filename (_type_ '.nex'): _description_ input: a nexus file structured for AmoCoala.

    Returns:
        _type_: _description_ a Tuple
        1) A Tree List containing Host Tree in first position, Parasyte Tree on second position.
        2) A dictionary of strings containing pairs key "Host" :  value ["Parasyte1", "Parasyte2", ...]
    """
    
    assert filename.endswith(c.NEX), "File format must be '.nex'"
    
    with open(filename, 'r') as f:
        
        nTrees = 0 # number of Trees found
        nHTrees = 0 # host Trees found
        nPTrees = 0 # parasite Trees found
        importantLine = False # line to work with
        beginDistribution = False # distribution found
        lookForEndBlock = False # after a Begin there must be an EndBlock;
        lookForEnd = False # after a Range there must be an End;
        numOfNewLinesFound = 0 # Number of single '\n' lines found
        endCounter = 0 # counts how many lines are found after 'END;'
        
        treeList = []   # containing the Trees Host[0], Parasyte[1]
        dictionary = defaultdict(list) # containing key Host, value list of Parasytes
        
        firstLine = f.readline() # firstLine of file
        firstLine = firstLine.replace(c.NEW_LINE, "")
        if(firstLine != c.NEXUS): # Check if the firstline is '#NEXUS'
            assert (firstLine == c.NEXUS), "First line must be '#NEXUS': " + c.ASSERT_WRONG_STRUCTURE
        
        for line in f:
            try:
                if(endCounter >= 1):
                    endCounter += 1 # if we find another line after this one the structure is wrong!
                    assert (endCounter < 2), "There must be only a newline after 'END;', too many lines found! " + c.ASSERT_WRONG_STRUCTURE
                    continue
                if(lookForEnd): # if we are looking for 'END;' inside the file:
                    lookForEnd = False
                    assert (line.startswith(c.END)), "'END;' after 'BEGIN DISTRIBUTION; RANGE' missing: " + c.ASSERT_WRONG_STRUCTURE
                    endCounter += 1 # we reached the end of the file, we can find a newline now...
                    continue
                if(line.startswith(c.END)): # if we reach an 'END;' sooner than expected:
                    # separator before END; was missing:
                    assert (lookForEnd), "Usual '\t;' Separator after RANGE is missing or wrong use of 'END;' word " + c.ASSERT_WRONG_STRUCTURE
                    # something went wrong with distribution BEGIN or RANGE words missing:
                    assert (beginDistribution), "DistributionError: BEGIN or RANGE words missing" + c.ASSERT_WRONG_STRUCTURE
                    break # END; means we won't see anything else in the file
                if(lookForEndBlock): # if we're looking for 'ENDBLOCK;' inside the file
                    lookForEndBlock = False
                    assert (line.startswith(c.ENDBLOCK)), "'ENDBLOCK;' after 'BEGIN' word missing: " + c.ASSERT_WRONG_STRUCTURE
                    continue
                if(beginDistribution): # if BEGIN DISTRIBUTION and RANGE were found:
                    if(not line.__contains__(c.COLONS)): # if we don't find colons we want to find ';'
                        assert (line.__contains__(c.SEMICOLONS)), "Usual ';' after RANGE is missing: " + c.ASSERT_WRONG_STRUCTURE
                        # we found ';' then we end distribution phase and we look for 'END;'
                        beginDistribution = False
                        lookForEnd = True # now look for'END;' on next line
                        continue
                    # ...everything checked, we work on dictionary Host:[Parasytes] now:
                    else: # we found ':' then we work on the strings:
                        # it should not be possible to have semicolons before the end of distribution!
                        assert (not line.__contains__(c.SEMICOLONS)), "';' found on a line 'Parasyte: Host', ';' must be placed at the end of distribution phase " + c.ASSERT_WRONG_STRUCTURE
                        pair = __fetchPairString(line)
                        dictionary[pair[1]].append(pair[0]) # Host: [Parasyte1, Parasyte2, ...]
                        continue
                if(importantLine): # work line found: is it RANGE or TREE?
                    importantLine = False
                    if(line.__contains__(c.RANGE)): # if it's RANGE line then begin distribution...
                        beginDistribution = True
                        continue
                    # ...otherwise it has to be TREE line so we need to...
                    lookForEndBlock = True # ...look for 'ENDBLOCK;' on next line
                    # if there was an error like 'RANGE' wasn't found or the TreeFormat wrong -> assertion
                    # if we don't find '=' or find more than 1 '='  ---> assertion
                    assert(line.count(c.EQUAL) == 1), "Number of '=' should be only one: " + c.ASSERT_WRONG_STRUCTURE
                    lineSplit = line.split(c.EQUAL + c.SPACE)
                    # lineSplit[0] = TREE * Host, lineSplit[1] = the tree in newick format.
                    firstPart = lineSplit[0].lower() # let's lowercase it
                    # throw assertion if "Host" or Parasyte word are not found on this line.
                    assert (any(word.lower() in firstPart for word in c.HOST_WORDS_ALLOWED) or any(word.lower() in firstPart for word in c.PARASYTE_WORDS_ALLOWED)), "'Host' or 'Parasyte' word weren't found after BEGIN line: " + c.ASSERT_WRONG_STRUCTURE
                    newickString = lineSplit[1].replace(c.NEW_LINE, "")
                    
                    # TREE FOUND: is it Host or Parasyte?
                    if(any(word.lower() in firstPart for word in c.HOST_WORDS_ALLOWED)): # Host Tree Found
                        nTrees += 1
                        nHTrees += 1
                        # if number of Host trees is major than requested (2) assertion thrown:
                        assert (not (nHTrees > c.NUM_HOST_TREES)), "There can only be " + (str)(c.NUM_HOST_TREES) + " Host_Trees"
                        treeList.insert(0, PhyloTree(newickString)) # Host is always on first position.
                    else: # Parasite Tree Found
                        nTrees += 1
                        nPTrees += 1
                        # if number of Parasyte trees is major than requested (2) assertion thrown:
                        assert (not (nPTrees > c.NUM_PARASITE_TREES)), "There can only be " + (str)(c.NUM_PARASITE_TREES) + " Parasite_Trees"
                        treeList.append(PhyloTree(newickString)) # Parasyte is always on second position.
                    continue
                if(line.startswith(c.BEGIN)): # if "BEGIN" string found, the next one is important!
                    numOfNewLinesFound = 0 # reset the '\n' lines counter
                    importantLine = True    # (Range? or Tree?)
                    if(nTrees == c.NUM_OF_TREES): # if we found max num of trees allowed it must be 'Begin Distribution':
                        assert (line.startswith(c.BEGIN_DISTRIBUTION)), "BEGIN DISTRIBUTION wasn't found after max number of trees reached: " + c.ASSERT_WRONG_STRUCTURE
                elif(line == c.NEW_LINE): # if we didn't find 'BEGIN' it must be '\n' new line:
                    numOfNewLinesFound += 1
                    assert (numOfNewLinesFound <= c.NUM_OF_NEW_LINES_ALLOWED), "Too many consecutive 'new lines': " + c.ASSERT_WRONG_STRUCTURE
                else: # if it's not a new line then we throw an assertion:
                    assert(not line.__contains__(c.BEGIN)), "BEGIN should be at the beginning of the line and not preceeded by anything: " + c.ASSERT_WRONG_STRUCTURE
                    assert (line == c.NEW_LINE), c.ASSERT_WRONG_STRUCTURE + "Don't use anything else than new lines as separators between BEGIN BLOCKS."
                    
            except AssertionError as msg:
                print(msg)
                sys.exit(1)
        
        try: # if we find less or equal to 1 trees we throw assertion:
            assert (nTrees > 1), "Number of trees must be major than 1! " + c.ASSERT_WRONG_STRUCTURE
        except AssertionError as msg:
            print(msg)
            sys.exit(1)
        finally:
            f.close()
            
        return treeList, dictionary