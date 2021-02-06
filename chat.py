import pandas as pd
from datetime import datetime
import re
import language_tool_python

class Chat():
    '''
    '''
    def __init__(self, path):
        '''
        '''
        data = self.read_data(path)
        self.data = self.build_matrix(data)


    def read_data(self, path):
        '''
        '''
        with open(path, "r", encoding="utf8") as f:
            data = f.read().\
                replace("\n", " \n ").\
                replace("\r", "").\
                replace("\x96", "").\
                replace("<Multimedia omitido>", "").\
                split("\n")

        data = list(map(self.proc_data, data))
        return  list(filter(None, data))

    def proc_data(self, message):
        '''
        First step in data processing. Delete all raw text elements that are
        not text or multimedia messages sent by group members.
        '''
        message = re.sub(r"http\S+", "", message)
        if not (len(message.split(":")) == 3 and\
                message[1] != "[" and\
                message[1] != "+"):
            message = None
        return message


    def get_message_date(self, message):
        '''
        '''
        date = message.split("-")[0]
        date = date.strip(" ")
        try:
            return datetime.strptime(date, '%d/%m/%y %H:%M')
        except:
            pass

    def get_message_name(self, message):
        '''
        '''
        return message.split(":")[1][5:]

    def get_message_content(self, message):
        '''
        '''
        return message.split(":")[2].strip(" ")

    def build_matrix(self, data):
        '''
        '''
        toret =  pd.DataFrame({
            'name': list(map(self.get_message_name, data)),
            'date': list(map(self.get_message_date, data)),
            'content': list(map(self.get_message_content, data))
        })
        toret = toret[toret.content != '']
        toret = toret[toret.name != '']
        return toret

    def get_proofreaded_data(self, lang, users=None):
        '''
        '''
        tool = language_tool_python.LanguageTool(lang)
        toret = self.data
        if users != None:
            toret = toret[toret.name in users]
            toret['content'] = list(map(tool.correct, toret['content'].to_list()))
        else:
            toret['content'] = list(map(tool.correct, toret['content'].to_list()))
        return toret

    def get_users_list(self):
        '''
        '''
        return self.data.name.unique()



if __name__ == '__main__':
    chat = Chat('./data/chat.txt')
    df = chat.get_proofreaded_data('es')
    chat.data.content[chat.data.name == 'Pablo']
    chat.get_users_list()