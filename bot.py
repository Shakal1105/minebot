import python_aternos.aterrors
from python_aternos import Client
import telebot
from configure import info

account_dict = {}
accounts = open("accounts.txt", "r")
for i in accounts.readlines():
    lis = i.replace("\n", "").split(":")
    account_dict[lis[0]] = lis[1]
accounts.close()
Login_first = list(account_dict.keys())[1]

class Aternos():
    def __init__(self, login, passwd):
        client = Client()
        client.login(login, passwd)

        acc = client.account
        self.serv = acc.list_servers()[0]

    def start(self):
        self.serv.start()

    def stop(self):
        self.serv.stop()

class TelegramBot():
    def __init__(self):
        self.check_error=1
        self.log, self.pas = Login_first, account_dict[Login_first]
        print("Starting...")

    def AccountError(self):
        try:
            self.server = Aternos(login=self.log, passwd=self.pas)
            self.start()
        except python_aternos.aterrors.CredentialsError:
            del account_dict[self.log]
            with open("accounts.txt", "w") as f:
                f.write(str(account_dict).replace("{","").replace("}","").replace("'", "").replace(",","\n").replace(" ", ""))
            print(self.AccountError.__name__)
            bot = telebot.TeleBot(data["Token"])
            bot.send_message(chat_id=-1001803120110,text=f"account __[{self.log}]__ ==> has been blocked\ni will check next in list")
            if len(account_dict) > 1:
                self.log, self.pas = list(account_dict.keys())[1], account_dict[list(account_dict.keys())[1]]
                self.AccountError()
            else:
                bot = telebot.TeleBot(data["Token"])
                bot.send_message(chat_id=-1001803120110, text="List accounts is EMPTY")
                exit()

    def start(self):
        if self.check_error == 1:
            self.check_error = 0
            self.AccountError()
        else:
            print("bot started!")
            self.admin = [1087968824, 697798016, ]
            self.user = []
            self.bot = telebot.TeleBot(data["Token"])

            Button = telebot.types.KeyboardButton
            self.addKeyboard = telebot.types.ReplyKeyboardMarkup()
            self.delKeyboard = telebot.types.ReplyKeyboardRemove()
            self.addKeyboard.row(Button(text="/server"), Button(text="/start_server"), Button(text="/stop_server")).row(
                Button(text="/help"), Button(text="/chat_help"), Button(text="/game_info")).add(
                Button(text="/hide keyboard"), Button(text="join server"))

            @self.bot.message_handler(commands=["server"])
            def server(m):
                self.bot.send_message(m.chat.id, f"[[[ {data["link"]} ]]]")

            @self.bot.message_handler(commands=["hide"])
            def server(m):
                self.bot.send_message(m.chat.id, "Keyboard is hide, use /start fot show again",
                                      reply_markup=self.delKeyboard)

            @self.bot.message_handler(commands=["start", "help"])
            def servstart(m):
                self.bot.send_chat_action(chat_id=m.chat.id, action="typing")
                self.bot.send_message(chat_id=m.chat.id,
                                      text=f"Hello, for more info you can use /help,/start\n/start_server game\n/stop_server game\n/chat_help\n/game_info",
                                      reply_markup=self.addKeyboard)

            @self.bot.message_handler(commands=["chat_help"])
            def servstart(m):
                self.bot.send_chat_action(chat_id=m.chat.id, action="typing")
                self.bot.send_message(chat_id=m.chat.id,
                                      text="use {| `add` |} in chat for adding info, use {| `name` |} for getting info,use {| `***` |} for delete info, use {| `list` |} for get list",
                                      parse_mode="Markdown")

            @self.bot.message_handler(commands=["game_info"])
            def servstart(m):
                self.bot.send_chat_action(chat_id=m.chat.id, action="typing")
                self.bot.send_message(chat_id=m.chat.id,
                                      text=f"Address(HOST) ==> {data['Server_address']}\nPORT ==> {data['Server_port']}\nVersion ==> {data['version']}\nEdition ==> {data['edition']}")

            @self.bot.message_handler(commands=["start_server"])
            def servstart(m):
                if m.from_user.id not in self.admin:
                    self.bot.send_message(m.chat.id, "YOU NOT HAVE PERMISSION")
                else:
                    self.bot.send_chat_action(chat_id=m.chat.id, action="typing")
                    try:
                        self.server.start()
                    except Exception:
                        pass
                    self.bot.send_message(chat_id=-1001803120110,
                                          text=f"Server ==> {data['Server_address']}:{data['Server_port']} <== minecraft has been STARTED")

            @self.bot.message_handler(commands=["stop_server"])
            def servstart(m):
                if m.from_user.id not in self.admin:
                    self.bot.send_message(m.chat.id, "YOU NOT HAVE PERMISSION")
                else:
                    self.bot.send_chat_action(chat_id=m.chat.id, action="typing")
                    try:
                        self.server.stop()
                    except Exception:
                        pass
                    self.bot.send_message(chat_id=-1001803120110,
                                          text=f"Server ==> {data['Server_address']}:{data['Server_port']} <== minecraft has been STOPED")

            @self.bot.message_handler(content_types=["text"])
            def text(m):
                chat_id, user_id, text = m.chat.id, m.from_user.id, m.text.lower()
                if text == "join server":
                    self.bot.send_message(chat_id, f"TAP ==> {data["add"]} <== TAP")
                elif int(user_id) not in self.admin and int(user_id) not in self.user:
                    print(user_id)
                    if text == "+":
                        self.user.append(int(user_id))
                    else:
                        self.bot.send_message(chat_id, "only users can use chat command if you user write + in chat")
                else:
                    if "add" in text:
                        if len(text.split()) >= 3:
                            with open("configure.py", "r") as f:
                                config = f.read()
                            with open("configure.py", "w") as file:
                                arr = text.split()
                                if arr[1] in info:
                                    self.bot.send_message(chat_id, "change other name")
                                else:
                                    txt = ""
                                    for i in arr[2:]:
                                        txt = txt + i + " "
                                    info[arr[1]] = txt
                                    information = config.replace("}", "\t") + "'" + arr[1] + "'" + ":" + "'" + txt + "',\n}"
                                    file.write(information)
                                    self.bot.send_message(chat_id, f"header [{arr[1]}] title [{info[arr[1]]}] added")
                        elif text[:3] == "add" or len(text) < 5:
                            self.bot.send_message(chat_id=chat_id,
                                                  text="if you want add position write next\nadd name x/y/z Example: add Home 12/0/-103 or add wood i_need_woods!64")
                    elif "del" in text:
                        if len(text.split()) == 2:
                            arr = text.split()
                            if not arr[1] in info:
                                self.bot.send_message(chat_id, f"{arr[1]} not in list use `list'", parse_mode="Markdown")
                            elif arr[1] == "HEADER" or arr[1] == "name":
                                self.bot.send_message(chat_id, "CAN NOT DELETE MAIN NOTE")
                            else:
                                del info[arr[1]]
                                self.bot.send_message(chat_id, f"{arr[1]} has been deleted")
                                list = str(info).replace("{", "info = {\n\t").replace(",", ",\n\t").replace("}", ",\n}")
                                with open("configure.py", "w") as f:
                                    f.write(list)
                        else:
                            self.bot.send_message(chat_id, "Example ss in list del ss for remove from list")
                    if text in info:
                        self.bot.send_message(chat_id=chat_id, text=f"_____/[{text}]\_____\n{info[text]}")
                    if text == "list":
                        lists = info.keys()
                        list = ""
                        for l in lists:
                            list = list + str(l) + "\n"
                        self.bot.send_message(chat_id=chat_id, text=list)

            self.bot.polling(none_stop=True, timeout=60)



if __name__ == "__main__":
    Bot = TelegramBot()
    data = {
        "Token": "6693525212:AAH15wKF0AzN0g1raU6EtbFjzz--vgaOJ5k",
        "Server_address": "lpsh1.aternos.org",
        "Server_port": 35064,
        "version":"1.20.12.01",
        "edition":"bedrock(mine pocket edotion)",
        "add":"https://add.aternos.org/lpsh1",
        "link":"https://aternos.org/servers/"
    }

    Bot.start()
