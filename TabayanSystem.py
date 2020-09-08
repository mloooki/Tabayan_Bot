# -*- coding: UTF8 -*-
import requests
import pickle
import csv
import datetime as date
import telebot
import json

#from telegram.ext import Updater, CommandHandler
#from telegram import ReplyKeyboardMarkup


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
        params = {'chat_id': chat_id, 'text': text,'parse_mode': 'HTML'}
        method = 'sendMessage'
        resp = requests.post(self.api_url + method, params)
        return resp
    def send_message2(self, chat_id, text):
        reply_markup = {"keyboard": [["-أرسل تاريخ اليوم"], ["-أرسل تاريخ أمس"], ["-لا أعرف التاريخ"],["-إدخال التاريخ بشكل يدوي"]], "one_time_keyboard": True,'resize_keyboard' : True,}
        params = {'chat_id': chat_id, 'text': text, 'reply_markup':json.dumps(reply_markup) ,'parse_mode': 'HTML'}
        method = 'sendMessage'
        resp = requests.post(self.api_url + method, params)
        return resp
    def send_message3(self, chat_id, text):
        reply_markup = {"inline_keyboard": ["تجربه"],"url": "https://twitter.com/?lang=ar"}
        params = {'chat_id': chat_id, 'text': text, 'reply_markup':json.dumps(reply_markup) ,'parse_mode': 'HTML'}
        method = 'sendMessage'
        resp = requests.post(self.api_url + method, params)
        return resp


    def send_reply(self, chat_id, text,reply_to_message_id):

        params = {'chat_id': chat_id, 'text': text, 'reply_to_message_id' : reply_to_message_id	 ,'parse_mode': 'HTML'}
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

#Token of your bot
token='xxxxxxxx' # For @TabayanBot
oldtoken = 'xxxxxxx' # For @Tabayan_test1_bot

My_bot = BotHandler(token) #Your bot's name


def test(sample,model):
    return model.predict([sample.replace(',', ' ').replace('"""', ' ').replace('""', ' ').replace('   ', ' ').replace('  ', ' ')])

def initialize():
    import pandas as pd
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.feature_selection import SelectKBest
    from sklearn.svm import LinearSVC
    from sklearn.feature_selection import chi2
    from imblearn.pipeline import Pipeline

    data = pd.read_csv('all without duplicates.csv', sep=',', )

    Targets_list = data['Target'].values.astype('U')
    features = (data['tweet_w_EOL'] + " " + data['created_at']).values.astype('U')

    pipeline = Pipeline([('vect', TfidfVectorizer(ngram_range=(1, 1), sublinear_tf=True)),
                         # ('chi', SelectKBest(chi2, k=5)),
                         ('clf', LinearSVC(C=1.0, penalty='l1', max_iter=1000, dual=False))])

    model= pipeline.fit(features, Targets_list)
    # save the classifier
    with open('my_dumped_classifier.pkl', 'wb') as fid:
        pickle.dump(model, fid)



def TabayanModel():
    # load the model again
    with open('my_dumped_classifier.pkl', 'rb') as fid:
        model_loaded = pickle.load(fid)
    return model_loaded

def main():
    new_offset = 0
    print('Now launching...')
    # initialize()  # No need to run this function more than one time ; through this function, we have been trained the model and save it to the disk
    trainedmodel = TabayanModel()
    verify=False
    getdate=False

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
            try:
                message_id = current_update[add+'message']['reply_to_message']['message_id']
                print('message id = ', message_id)
            except:
                print("Error :)")
                #message_id=first_chat_id
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
                        first_chat_text = first_chat_text.replace('@TabayanBot','').replace('  ','')
                        print("first_chat_text = ", first_chat_text)

                        try:
                            orignal_text = current_update[add+'message']['reply_to_message']['text'] # This is mean it's a reply to a message.
                            reply=True
                        except:
                            print("it's not a reply")
                            orignal_text=''
                            reply = False

                        new_offset = first_update_id + 1

                        if (reply):
                             if ('تحقق' in first_chat_text): # here we must send the orignal_text to the classifier.
                                 if('الرجاء التحقق من التالي:' in first_chat_text):
                                     first_chat_text = first_chat_text.replace('الرجاء التحقق من التالي:', '')
                                     if(len(first_chat_text)<=8):
                                         newstext = orignal_text
                                     else:
                                         newstext= first_chat_text
                                 else :  # therfore, it's in first_chat_text)
                                     orignal_text = orignal_text.replace('الرجاء التحقق من التالي:', '')
                                     newstext = orignal_text

                                 detectionResult = test(newstext, trainedmodel)
                                 if (detectionResult[0] == 'Non-rumor'):
                                     message = 'ليست شائعة ✅'
                                 else:
                                     message = 'شائعة ❌'

                                 My_bot.send_reply(first_chat_id, "الخبر : {} \n"
                                                                    "نتيجة التحقق : {}".format(orignal_text, message),message_id)
                                 new_offset = first_update_id + 1

                             else:
                                My_bot.send_message(first_chat_id," الرجاء تضمين كلمة 'تحقق' إن كنت تود التحقق من الخبر المشار إليه .." +('\n@'+current_update[add+'message']['from']['username']+'\n'))
                                print('do nothing :)')
                                new_offset = first_update_id + 1
                        else:

                            if ('الرجاء التحقق من التالي:' in first_chat_text):
                                first_chat_text = first_chat_text.replace('الرجاء التحقق من التالي:', '')
                                detectionResult = test(first_chat_text, trainedmodel)
                                if (detectionResult[0] == 'Non-rumor'):
                                    message = 'ليست شائعة ✅'
                                else:
                                    message = 'شائعة ❌'

                                My_bot.send_reply(first_chat_id,  " الخبر : {} \n"
                                                                   
                                                                   "نتيجة التحقق : {}".format(first_chat_text, message) +('\n@'+current_update[add+'message']['from']['username']+'\n'),message_id)
                                new_offset = first_update_id + 1
                            elif ("السلام عليكم" in first_chat_text or "سلام" in first_chat_text ) and ( len(first_chat_text) < 20):
                                My_bot.send_message(first_chat_id, 'وعليكم السلام ورحمة الله وبركاته' +('\n@'+current_update[add+'message']['from']['username']+'\n'))
                                print("the message text = ", first_chat_text)
                                new_offset = first_update_id + 1
                            elif ("مشكور" in first_chat_text or "شكرا" in first_chat_text ) and  len(first_chat_text) < 20 :
                                My_bot.send_message(first_chat_id, 'اهلاً وسهلاً 😊🤍' +('\n@'+current_update[add+'message']['from']['username']+'\n'))
                                print("the message text = ", first_chat_text)
                                new_offset = first_update_id + 1

                            elif ("اهلا" in first_chat_text or "أهلا" in first_chat_text ) and len(first_chat_text) < 20 :
                                My_bot.send_message(first_chat_id, 'أهلاً وسهلاً بك 🤍' +('\n@'+current_update[add+'message']['from']['username']+'\n'))
                                print("the message text = ", first_chat_text)
                                new_offset = first_update_id + 1
                            elif ("هلا" in first_chat_text or "مرحبا" in first_chat_text) and ( len(first_chat_text) < 20):
                                My_bot.send_message(first_chat_id, 'أهلاً وسهلا ً' +('\n@'+current_update[add+'message']['from']['username']+'\n'))
                                print("the message text = ", first_chat_text)
                                new_offset = first_update_id + 1
                            elif ("حياك" in first_chat_text) and ( len(first_chat_text) < 20):
                                My_bot.send_message(first_chat_id, 'الله يحييك' +('\n@'+current_update[add+'message']['from']['username']+'\n'))
                                print("the message text = ", first_chat_text)
                                new_offset = first_update_id + 1
                            elif ("اخبارك" in first_chat_text or "أخبارك" in first_chat_text ) and ( len(first_chat_text) < 20):
                                My_bot.send_message(first_chat_id, 'فرحان فيكم🤍' +('\n@'+current_update[add+'message']['from']['username']+'\n'))
                                print("the message text = ", first_chat_text)
                                new_offset = first_update_id + 1
                            elif ("كيف حالك" in first_chat_text or "كيف الحال" in first_chat_text) and ( len(first_chat_text) < 20):
                                My_bot.send_message(first_chat_id, 'عال العال' +('\n@'+current_update[add+'message']['from']['username']+'\n'))
                                print("the message text = ", first_chat_text)
                                new_offset = first_update_id + 1
                            elif ((("عرف بنفسك" in first_chat_text or "عرفنا بنفسك" in first_chat_text or "عرف عن نفسك" in first_chat_text or "من أنت" in first_chat_text or "من انت" in first_chat_text or "مين أنت" in first_chat_text or "مين انت" in first_chat_text) and ( len(first_chat_text) < 25)) or len(first_chat_text) < 2):
                                My_bot.send_message(first_chat_id,
                                                    "السلام عليكم ورحمة الله وبركاته , أنا تبيّن، مكتشف الشائعات !\n للتحقق من خبر ما إن كان شائعة أم لا، أشر إلى الحساب الخاص بي 'Reply' مع  كلمة 'تحقق' للرسالة التي تتضمن الخبر الذي تود التحقق منه أو،\n أشر إلى الحساب مع تضمين 'الرجاء التحقق من التالي:' في بداية الرسالة لتفعيل خدمة التحقق. "
                                                    "\n"
                                                    "ملاحظة: يفضّل تضمين تاريخ نشر الخبر مع الخبر للحصول على أفضل النتائج.."
                                                    "\n\n"
                                                    "هذا كل شيء، شكراً لاستخدامكم نظام تبيّن. 😊"
                                                    +('\n@'+current_update[add+'message']['from']['username']+'\n'))
                                new_offset = first_update_id + 1
                            else:
                                print('Unexpected message:', first_chat_text)
                                if first_chat_text != '/start':
                                    f.write(first_chat_text + ",\r\n")
                                new_offset = first_update_id + 1


            else : # this is mean the message is private.

                    if first_chat_text == '/start':
                        My_bot.send_message(first_chat_id, ' مرحباً بك في نظام تبيّن !' + first_chat_name )
                        new_offset = first_update_id + 1
                    elif verify:
                        newstext=first_chat_text
                        My_bot.send_message2(first_chat_id," ماهو تاريخ نشر الخبر؟  ")
                        new_offset = first_update_id + 1
                        verify=False
                        getdate=True

                    elif getdate:

                        newstext += " "+ first_chat_text

                        detectionResult = test(newstext, trainedmodel)
                        print(detectionResult)
                        print(detectionResult[0])
                        if (detectionResult[0] == 'Non-rumor'):
                            message = 'ليست شائعة ✅'
                        else:
                            message = 'شائعة ❌'

                        #newstext = newstext.replace(first_chat_text,'')   # remove the date
                        My_bot.send_message(first_chat_id, "الخبر : {} \n"
                                                           "\n"
                                                           "نتيجة التحقق : {}".format(newstext, message))
                        with open("Classifier_results.csv",'a', newline='',encoding="UTF-8") as file :
                            write_to_csv = csv.writer(file)
                            #write_to_csv.writerow(["Target","tweet_w_EOL","created_at"])
                            write_to_csv.writerow(["{}".format(detectionResult[0]),"{}".format(newstext),"{}".format(date.datetime.today())])


                        new_offset = first_update_id + 1
                        getdate=False

                    elif 'أهلا' in first_chat_text or 'هلا' in first_chat_text or 'اهلا وسهلا' in first_chat_text and (len(first_chat_text) < 20):
                        My_bot.send_message(first_chat_id, "أهلاً وسهلاً بك , أنا تبيّن، مكتشف الشائعات !\n للتحقق من خبر ما إن كان شائعة أم لا، أرسل  كلمة 'تحقق' لتفعيل خدمة التحقق. "
                                                    
                                                    "\n\n"
                                                    "أما إن وددت الخروج،فأرسل 'انهاء'.."
                                                    "\n"
                                                    "هذا كل شيء، شكراً لاستخدامكم نظام تبيّن. 😊")

                        new_offset = first_update_id + 1
                    elif 'تحقق' in first_chat_text and (len(first_chat_text) < 7):
                        My_bot.send_message(first_chat_id, "الرجاء إرسال الخبر الذي تود التحقق منه")
                        new_offset = first_update_id + 1
                        verify = True
                    elif (("السلام عليكم" in first_chat_text or "سلام" in first_chat_text or "عرف بنفسك" in first_chat_text or "عرفنا بنفسك" in first_chat_text or "عرف عن نفسك" in first_chat_text or "من أنت" in first_chat_text or "من انت" in first_chat_text or "مين أنت" in first_chat_text or "مين انت" in first_chat_text) and ( len(first_chat_text) < 25)) or len(first_chat_text) < 2 :
                        My_bot.send_message(first_chat_id,"وعليكم السلام ورحمة الله وبركاته , أنا تبيّن، مكتشف الشائعات !\n للتحقق من خبر ما إن كان شائعة أم لا،أرسل  كلمة 'تحقق' لتفعيل خدمة التحقق. "
                                                    "\n\n"
                                                    "أما إن وددت الخروج،فأرسل 'انهاء'.."
                                                    "\n"
                                                    "هذا كل شيء، شكراً لاستخدامكم نظام تبيّن. 😊")
                        new_offset = first_update_id + 1
                    elif ("كيف حالك" in first_chat_text or "كيف الحال" in first_chat_text) and (len(first_chat_text) < 20):
                        My_bot.send_message(first_chat_id, 'عال العال')
                        print("the message text = ", first_chat_text)
                        new_offset = first_update_id + 1
                    elif ("اخبارك" in first_chat_text or "أخبارك" in first_chat_text) and (len(first_chat_text) < 20):
                        My_bot.send_message(first_chat_id, 'بخير عساك بخير 🤍')
                        print("the message text = ", first_chat_text)
                        new_offset = first_update_id + 1
                    elif ("حياك" in first_chat_text) and (len(first_chat_text) < 20):
                        My_bot.send_message(first_chat_id, 'الله يحييك')
                        new_offset = first_update_id + 1
                        print("the message text = ", first_chat_text)

                    elif 'انهاء' in first_chat_text and (len(first_chat_text) < 13):
                        My_bot.send_message(first_chat_id, 'شكراً لك لاستخدامك نظام تبيّن، نأمل أن يكون حاز على رضاك واستحسانك.')
                        new_offset = first_update_id + 1
                        print("the message text = ", first_chat_text)

                    elif ("مشكور" in first_chat_text or "شكرا" in first_chat_text ) and  len(first_chat_text) < 20 :
                        My_bot.send_message(first_chat_id, 'اهلاً وسهلاً 😊🤍.')
                        print("the message text = ", first_chat_text)
                        new_offset = first_update_id + 1
                    else:
                        print("Unexpected message:", first_chat_text)
                        if first_chat_text!='/start':
                            f.write(first_chat_text + ",\r\n")
                        new_offset = first_update_id + 1



if __name__ == '__main__':
    try:
        f = open("UnexpectedMessages.txt", "a+")# To save unexpected messages in order to enhance Tabayan performance
        main()
        f.close()
        print('Done !')
    except KeyboardInterrupt:
        exit()