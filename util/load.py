import pandas as pd
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
        result_value = []
        phase_value = [None]
        train = []
        neotrain = []
        # df = pd.read_excel('./Vp9AaLm_jQ9Q0U90W1S.xlsx', None)
        df = pd.read_excel(self.file, None)
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
                                result_value.append(df['Parameters_Table'].iloc[val_c, 2])
                                tag = df['Parameters_Table'].iloc[val_c, 8]
                                val_c += 1
                                c = 1
                            if c == 1 and i != j:
                                break
                        if tag != 0 and tag > len(phase_value) - 1:
                            phase_value.extend([None] * (tag - len(phase_value) + 1))
                        if tag != -1:
                            phase_value[tag] = result_value
                        c = -1
                        result_value = []
                    # print(item+str(phase_value))
                    if df['Process_Table'].iloc[process_c, 1] == 2:
                        neotrain.append(phase_value)
                        print(item + str(phase_value))
                        # print('phase_id:'+str(phase_id))
                    else:
                        train.append(phase_value)
                    phase_id = []
                    phase_value = [None]
                    record = -1
                    break
        print(neotrain)
        print(len(neotrain))
        if len(neotrain) != 0:
            print(len(neotrain[0]))
        return((train,neotrain))

