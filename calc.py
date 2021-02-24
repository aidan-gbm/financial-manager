from difflib import SequenceMatcher

def similarity(str1:str, str2:str, threshold=0.8):
    ratio = SequenceMatcher(None, str1, str2).quick_ratio()
    return False if ratio < threshold else ratio

def findMatches(val:str, aliases:dict):
    matches = []
    for key, name_list in aliases.items():
        for name in name_list:
            if False != (s := similarity(val, name)):
                if s >= 0.95:
                    return key
                matches.append(key)
    return sorted(matches)
