############################ 분류 작업 만들기
class SortManager():
    def sorting(self, data_list):
        myList_point = sorted(data_list, 
                    key=lambda x: int(x[4].replace('(', '').replace(')', '')) 
                    if x[4].replace('(', '').replace(')', '').isdigit() else 0, 
                    reverse = True)
        return myList_point