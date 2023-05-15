from ete3 import PhyloTree
from collections import defaultdict
from sys import exit

import constants as c

def __fetch_pair_string(pair_string):
    """_summary_ 
    Function called to get [Parasyte,Host] pair and store it into a list.

    Args:
        pairString (_type_ "String"): _description_ line "Parasyte: Host"

    Returns:
        _type_: _description_ A list that contains the name of parasyte on first position
        and the host name in second position:
        [Parasyte, Host]
    """
    n_pair = pair_string.replace(c.TAB, "").replace(c.SPACE, "").replace(c.COMMA, "").replace(c.NEW_LINE, "")
    return n_pair.split(c.COLONS)

def nexus_reader(filename):
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
        
        n_trees = 0 # number of Trees found
        nH_trees = 0 # host Trees found
        nP_trees = 0 # parasite Trees found
        important_line = False # line to work with
        begin_distribution = False # distribution found
        look_for_end_block = False # after a Begin there must be an EndBlock;
        look_for_end = False # after a Range there must be an End;
        num_of_new_lines_found = 0 # Number of single '\n' lines found
        end_counter = 0 # counts how many lines are found after 'END;'
        begin_host = False # BEGIN_HOST line indicator
        begin_parasyte = False # BEGIN_PARASYTE line indicator
        
        tree_list = []   # containing the Trees Host[0], Parasyte[1]
        dictionary = defaultdict(list) # containing key Host, value list of Parasytes
        
        first_line = f.readline() # firstLine of file
        first_line = first_line.replace(c.NEW_LINE, "")
        if(first_line != c.NEXUS): # Check if the firstline is '#NEXUS'
            assert (first_line == c.NEXUS), "First line must be '#NEXUS': " + c.ASSERT_WRONG_STRUCTURE
        
        for line in f:
            try:
                if(end_counter >= 1):
                    end_counter += 1 # if we find another line after this one the structure is wrong!
                    assert (end_counter < 2), "There must be only a newline after 'END;', too many lines found! " + c.ASSERT_WRONG_STRUCTURE
                    continue
                if look_for_end: # if we are looking for 'END;' inside the file:
                    look_for_end = False
                    assert (line.startswith(c.END)), "'END;' after 'BEGIN DISTRIBUTION; RANGE' missing: " + c.ASSERT_WRONG_STRUCTURE
                    end_counter += 1 # we reached the end of the file, we can find a newline now...
                    continue
                if(line.startswith(c.END)): # if we reach an 'END;' sooner than expected:
                    # separator before END; was missing:
                    assert look_for_end, "Usual '\t;' Separator after RANGE is missing or wrong use of 'END;' word " + c.ASSERT_WRONG_STRUCTURE
                    # something went wrong with distribution BEGIN or RANGE words missing:
                    assert begin_distribution, "DistributionError: BEGIN or RANGE words missing" + c.ASSERT_WRONG_STRUCTURE
                    break # END; means we won't see anything else in the file
                if look_for_end_block: # if we're looking for 'ENDBLOCK;' inside the file
                    look_for_end_block = False
                    assert (line.startswith(c.ENDBLOCK)), "'ENDBLOCK;' after 'BEGIN' word missing: " + c.ASSERT_WRONG_STRUCTURE
                    continue
                if begin_distribution: # if BEGIN DISTRIBUTION and RANGE were found:
                    if(not line.__contains__(c.COLONS)): # if we don't find colons we want to find ';'
                        assert (line.__contains__(c.SEMICOLONS)), "Usual ';' after RANGE is missing: " + c.ASSERT_WRONG_STRUCTURE
                        # we found ';' then we end distribution phase and we look for 'END;'
                        begin_distribution = False
                        look_for_end = True # now look for'END;' on next line
                        continue
                    # ...everything checked, we work on dictionary Host:[Parasytes] now:
                    else: # we found ':' then we work on the strings:
                        # it should not be possible to have semicolons before the end of distribution!
                        assert (not line.__contains__(c.SEMICOLONS)), "';' found on a line 'Parasyte: Host', ';' must be placed at the end of distribution phase " + c.ASSERT_WRONG_STRUCTURE
                        pair = __fetch_pair_string(line)
                        dictionary[pair[1]].append(pair[0]) # Host: [Parasyte1, Parasyte2, ...]
                        continue
                if important_line: # work line found: is it RANGE or TREE?
                    important_line = False
                    if(line.__contains__(c.RANGE)): # if it's RANGE line then begin distribution...
                        begin_distribution = True
                        continue
                    # ...otherwise it has to be TREE line so we need to...
                    look_for_end_block = True # ...look for 'ENDBLOCK;' on next line
                    # if there was an error like 'RANGE' wasn't found or the TreeFormat wrong -> assertion
                    # if we don't find '=' or find more than 1 '='  ---> assertion
                    assert(line.count(c.EQUAL) == 1), "On a line that follows BEGIN HOST or BEGIN PARASITE there must be '=' before a newick tree. '==' or more '=' are not allowed: " + c.ASSERT_WRONG_STRUCTURE
                    line_split = line.split(c.EQUAL)
                    # lineSplit[0] = TREE * Host, lineSplit[1] = the tree in newick format.
                    newick_string = line_split[1].replace(c.NEW_LINE, "")
                    
                    # TREE FOUND
                    if(begin_host): # Host Tree Found
                        begin_host = False
                        n_trees += 1
                        nH_trees += 1
                        # if number of Host trees is major than requested (2) assertion thrown:
                        assert (not (nH_trees > c.NUM_HOST_TREES)), "There can only be " + (str)(c.NUM_HOST_TREES) + " Host_Trees"
                        tree_list.insert(0, PhyloTree(newick_string)) # Host is always on first position.
                    elif(begin_parasyte): # Parasite Tree Found
                        begin_parasyte = False
                        n_trees += 1
                        nP_trees += 1
                        # if number of Parasyte trees is major than requested (2) assertion thrown:
                        assert (not (nP_trees > c.NUM_PARASITE_TREES)), "There can only be " + (str)(c.NUM_PARASITE_TREES) + " Parasite_Trees"
                        tree_list.append(PhyloTree(newick_string)) # Parasyte is always on second position.
                    continue
                if(line.startswith(c.BEGIN)): # if "BEGIN" string found, the next one is important!
                    num_of_new_lines_found = 0 # reset the '\n' lines counter
                    important_line = True    # (Range? or Tree?)
                    if(n_trees == c.NUM_OF_TREES): # if we found max num of trees allowed it must be 'Begin Distribution':
                        assert (line.startswith(c.BEGIN_DISTRIBUTION)), "BEGIN DISTRIBUTION wasn't found after max number of trees reached: " + c.ASSERT_WRONG_STRUCTURE
                    uppercase_line = line.upper()
                    if uppercase_line.__contains__(c.HOST): # check if it's host tree
                        begin_host = True # host tree found
                    if uppercase_line.__contains__(c.PARASITE) or uppercase_line.__contains__(c.PARASYTE): # check if it's parasyte tree
                        begin_parasyte = True # parasyte tree found
                elif(line == c.NEW_LINE): # if we didn't find 'BEGIN' it must be '\n' new line:
                    num_of_new_lines_found += 1
                    assert (num_of_new_lines_found <= c.NUM_OF_NEW_LINES_ALLOWED), "Too many consecutive 'new lines': " + c.ASSERT_WRONG_STRUCTURE
                else: # if it's not a new line then we throw an assertion:
                    assert(not line.__contains__(c.BEGIN)), "BEGIN should be at the beginning of the line and not preceeded by anything: " + c.ASSERT_WRONG_STRUCTURE
                    assert (line == c.NEW_LINE), c.ASSERT_WRONG_STRUCTURE + "Don't use anything else than new lines as separators between BEGIN BLOCKS."
                    
            except AssertionError as msg:
                print(msg)
                exit(1)
        
        try: # if we find less or equal to 1 trees we throw assertion:
            assert (n_trees > 1), "Number of trees must be major than 1! " + c.ASSERT_WRONG_STRUCTURE
        except AssertionError as msg:
            print(msg)
            exit(1)
        finally:
            f.close()
            
        return tree_list, dictionary