# -*- coding: UTF8 -*-
import requests
import datetime



class BotHandler:
    def __init__(self, token):
            self.token = token
            self.api_url = "https://api.telegram.org/bot{}/".format(token)

    #url = "https://api.telegram.org/bot<token>/"

    def get_updates(self, offset=0, timeout=30):
        method = 'getUpdates'
        params = {'timeout': timeout, 'offset': offset}
        resp = requests.get(self.api_url + method, params)
        result_json = resp.json()['result']
        return result_json

    def send_message(self, chat_id, text):
        params = {'chat_id': chat_id, 'text': text, 'parse_mode': 'HTML'}
        method = 'sendMessage'
        resp = requests.post(self.api_url + method, params)
        return resp

    def get_first_update(self):
        get_result = self.get_updates()

        if len(get_result) > 0:
            last_update = get_result[0]
        else:
            last_update = None

        return last_update


token = 'xxxxxxxxxx' #Token of your bot
My_bot = BotHandler(token) #Your bot's name



def main():
    new_offset = 0
    print('hi, now launching...')
    Welcome_Msg=["أهلا وسهلا","أهلاً وسهلاً","أهلاًوسهلاً","هلا","أهلا","أهلاً","هلاوالله","هلا والله","هاي","اهلا","مرحبا","مرحباً",]


    while True:
        all_updates=My_bot.get_updates(new_offset)

        if len(all_updates) > 0:
            for current_update in all_updates:
                print("current_update = ",current_update)
                first_update_id = current_update['update_id']
                try:
                    current_update['message']
                    add=''
                except:
                    add='edited_'
                if 'text' not in current_update[add+'message']:
                    first_chat_text='New member'
                else:
                    first_chat_text = current_update[add+'message']['text']


                first_chat_id = current_update[add+'message']['chat']['id']
                if 'first_name' in current_update[add+'message']:
                    first_chat_name = current_update[add+'message']['chat']['first_name']
                elif 'new_chat_member' in current_update[add+'message']:
                    first_chat_name = current_update[add+'message']['new_chat_member']['username']
                elif 'from' in current_update[add+'message']:
                    first_chat_name = current_update[add+'message']['from']['first_name']
                else:
                    first_chat_name = "unknown"
            message_type = current_update[add+'message']['chat']['type']
            print('message_type = ',message_type)

            if (message_type == 'group'):
                    try:
                        mention = current_update[add+'message']['entities'][0]['type'] # this is mean the text has a mention to the bot.
                        print("mention=",mention)
                        is_it_mention = True
                    except :
                        print(" it's not mention :) (don't reply)")
                        is_it_mention=False
                        new_offset = first_update_id + 1

                    if (is_it_mention): # maybe I will make the bot reply directly when this True.
                        print("first_chat_text = ",first_chat_text)
                        first_chat_text = first_chat_text.replace(' @rumor1bot','')
                        try:
                            orignal_text = current_update[add+'message']['reply_to_message']['text'] # This is mean it's a reply to a message.
                            print('orignal_text = ',orignal_text)
                            reply=True
                        except:
                            print("it's not a reply")
                            reply = False
                            new_offset = first_update_id + 1

                        if (reply):

                         if (first_chat_text == 'تحقق'): # here we must send the orignal_text to the classifier.
                            My_bot.send_message(first_chat_id, "الخبر : {} \n"
                                                               ""
                                                               "نتيجة التحقق : {}".format(orignal_text,'إشاعة'))
                            new_offset = first_update_id + 1
                         else:
                            print('do nothing :)')
                            new_offset = first_update_id + 1

            else : # this is mean the message is private.
                    if first_chat_text == '/start':
                        My_bot.send_message(first_chat_id,
                                            'مرحباً بك  ' + first_chat_name + " يمكنك الآن البدأ بإرسال الخبر للتحقق منه ")
                        new_offset = first_update_id + 1
                    elif first_chat_text in Welcome_Msg:
                        My_bot.send_message(first_chat_id, "أهلاً وسهلاً , أنا بوت تبيّن يمكنك إرسال الخبر للتحقق منه")
                        new_offset = first_update_id + 1
                    elif first_chat_text == 'كيف حالك':
                        My_bot.send_message(first_chat_id, "الحمد لله أنا بخير , يمكنك الآن إرسال الخبر للتحقق منه")
                        new_offset = first_update_id + 1
                    elif first_chat_text == "السلام عليكم":
                        My_bot.send_message(first_chat_id,
                                            "وعليكم السلام ورحمة الله وبركاته ,أنا بوت تبيّن يمكنك إرسال الخبر للتحقق منه ")
                        new_offset = first_update_id + 1
                    else:
                        My_bot.send_message(first_chat_id, 'هنا المفروض البوت يرد بالنتيجة (إشاعة أو لا)')
                        print("the message text = ", first_chat_text)
                        new_offset = first_update_id + 1



if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()