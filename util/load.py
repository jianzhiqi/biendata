import pandas as pd
import numpy as np
# df = pd.read_excel('./Vp9AaLm_jQ9Q0U90W1S.xlsx',None)
# df = pd.read_excel('./Vp3AaLm_jQU9Uzpzp0u.xlsx',None)
# print('df: \n',df)

class DataPre(object):

    def __init__(self,path):

        self.file = path

    def load(self):
        phase_id = []
        phase_c = 0
        # phase_s = 0
        val_c = 0
        tag = -1
        c = -1
        record = -1

        prev = None
        prev_s = None
        k = 0
        d = 0
        cur = [0]
        ma = [0]

        result_value = []
        phase_value = [np.nan]
        train = []
        neotrain = []
        # df = pd.read_excel('./Vp9AaLm_jQ9Q0U90W1S.xlsx', None)
        df = pd.read_excel(self.file, None)


        for s in df['Parameters_Table'].iloc[:, 8]:
            if s != 0 and s > (len(cur) - 1):
                cur.extend([0] * (s - len(cur) + 1))
                ma.extend([0] * (s - len(ma) + 1))
            if s == prev and df['Parameters_Table'].iloc[d, 0] == prev_s:
                cur[s] += 1
            else:
                prev = s
                prev_s = df['Parameters_Table'].iloc[d, 0]
                cur[s] = 1
            ma[s] = max((cur[s], ma[s]))
            # if cur[s] > ma[s]:
            #     ma[s] = cur[s]
            #     print(str(d)+ ':' +str(s) + ':' + str(ma[s]))
            d += 1

        print("test:" + str(len(ma)) + str(ma))


        for process_c, item in enumerate(df['Process_Table'].iloc[:, 0]):
            for process in df['Phase_Table'].iloc[phase_c:, 0]:
                if process == item:
                    phase_id.append(df['Phase_Table'].iloc[phase_c, 1])
                    phase_c += 1
                else:
                    record = 0
                if record == 0:
                    for j in phase_id:
                        # for param_c, i in enumerate(df['Parameters_Table'].iloc[:,0]):
                        for i in df['Parameters_Table'].iloc[val_c:, 0]:
                            if i == j:
                                tag = df['Parameters_Table'].iloc[val_c, 8]
                                if len(result_value) == 0:
                                    result_value = [np.nan] * ma[tag]
                                    k = 0
                                result_value[k] = df['Parameters_Table'].iloc[val_c, 2]
                                k += 1
                                # result_value.append(df['Parameters_Table'].iloc[val_c, 2])
                                val_c += 1
                                c = 1
                            if c == 1 and i != j:
                                break
                        if tag != 0 and tag > len(phase_value) - 1:
                            phase_value.extend([np.nan] * (tag - len(phase_value) + 1))
                        if tag != -1:
                            phase_value[tag] = result_value
                        c = -1
                        tag = -1
                        result_value = []
                    # print(item+str(phase_value))
                    if df['Process_Table'].iloc[process_c, 1] == 2:
                        neotrain.append(phase_value)
                        print(item + ':' + str(len(phase_value)) +str(phase_value))
                        # print('phase_id:'+str(phase_id))
                    else:
                        train.append(phase_value)
                    phase_id = []
                    phase_value = [np.nan]
                    record = -1
                    break
        print(neotrain)
        print(len(neotrain))
        if len(neotrain) != 0:
            print(len(neotrain[0]))
        return((train,neotrain))

# DataPre('../INSPEC_Data/INSPEC_train/VWpAaLm_jQU9pUW9pQO.xlsx').load()
# DataPre('../INSPEC_Data/INSPEC_train/VpWAaLm_jQU999p9zWB.xlsx').load()