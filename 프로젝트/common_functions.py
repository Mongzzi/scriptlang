import pickle

def Read_Adress_From_File():
    f = open('adress', 'rb') #pickle 사용을 위해 바이너리 읽기 파일 오픈
    return pickle.load(f) #파일에서 리스트 load

def Get_Name_Val_From_Dict(for_search, adress_dict):
    flag = False
    
    return_lsit = []

    for adress in adress_dict['level_3']:
        if flag: break
        if adress != None and for_search in adress:
            return_lsit.append((adress, adress_dict['level_3'][adress]))
            # flag = TRUE
    
    for adress in adress_dict['level_2']:
        if flag: break
        if adress != None and for_search in adress:
            return_lsit.append((adress, adress_dict['level_2'][adress]))
            # flag = TRUE

    for adress in adress_dict['level_1']:
        if flag: break
        if adress != None and for_search in adress:
            return_lsit.append((adress, adress_dict['level_1'][adress]))
            # flag = TRUE

    return return_lsit