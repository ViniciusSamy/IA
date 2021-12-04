
def bottom_up(KB, ask):
    C = []
    size_C = None

    while len(C) != size_C:
        size_C = len(C)
        for key in KB.keys():
            valid = False
            for rules in KB[key]:
                valid = valid or all([a in C for a in rules])
            
            if valid and (not key in C):
                C.append(key)

    return ask in C

def top_down(KB, ask):

    derivation = KB[ask][0]

    while derivation:
        print(derivation)
        rule = KB[derivation.pop(0)][0]
        for a in rule:
            derivation.append(a)
        
    print(derivation)   
    return True





if __name__ == "__main__":

    KB = {
            "a": [["b", "c"]],
            "b": [["e"], ["d"]],
            "c": [[]],
            "d": [["h"]],
            "e": [[]],
            "g": [["a", "b", "c"]],
            "f": [["h", "b"]]
        }    

    top_down(KB,"a")