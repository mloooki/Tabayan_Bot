
# -*- coding: UTF8 -*-

# Tabayan developers:
# Rawan Mohammed Alowaymir,
# Abdulmalik Sulaiman Alaqel.

#Libraries
import requests
import pickle
import csv
import datetime
import json

class BotHandler:

    #Class methods:

    def __init__(self, token):
        self.token = token
        self.api_url = "https://api.telegram.org/bot{}/".format(token)

    # url = "https://api.telegram.org/bot<token>/"

    # get_updates: receives messages
    def get_updates(self, offset=0, timeout=30):
        method = 'getUpdates'
        params = {'timeout': timeout, 'offset': offset}
        resp = requests.get(self.api_url + method, params)
        result_json = resp.json()['result']
        return result_json

    # send_message: sends an original message/response to a specified chat id
    def send_message(self, chat_id, text, reply_markup=None):
        params = {'chat_id': chat_id, 'text': text, 'reply_markup': reply_markup}
        method = 'sendMessage'
        resp = requests.post(self.api_url + method, params)
        return resp

    # send_multipleChoiceMessage: sends multi-choices message/response to a specified chat id
    def send_multipleChoiceMessage(self, chat_id, text, choiceslist):
        # ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
        reply_markup = {'keyboard': [choiceslist], 'one_time_keyboard': True, 'resize_keyboard': True}
        params = {'chat_id': chat_id, 'text': text, 'reply_markup': json.dumps(reply_markup), 'parse_mode': 'HTML'}
        method = 'sendMessage'
        resp = requests.post(self.api_url + method, params)
        return resp

    # send_reply: replies on a message to a specified chat id
    def send_reply(self, chat_id, text, reply_to_message_id):
        params = {'chat_id': chat_id, 'text': text, 'reply_to_message_id': reply_to_message_id, 'parse_mode': 'HTML'}
        method = 'sendMessage'
        resp = requests.post(self.api_url + method, params)
        return resp

#static methods:

#addScore: upgrades system rating scores
def addScore(scoreNum):
    with open('QayemniStats.txt', 'r') as file:
        lines=file.read().split('\n')
        QayemniHeader=lines[0].split(',')
        scores=lines[1].split(',')

    if (scoreNum == 4):
        scores[0]='{}'.format(int(scores[0]) + 1)

    elif scoreNum == 3:
        scores[1]='{}'.format( int(scores[1]) + 1 )

    elif scoreNum == 2:
        scores[2]='{}'.format( int(scores[2]) + 1 )

    elif scoreNum == 1:
        scores[3]='{}'.format( int(scores[3]) + 1 )

    scores[4]='{}'.format( int(scores[4]) + 1 )

    with open('QayemniStats.txt', 'w') as file:
        file.write(QayemniHeader[0]+','+QayemniHeader[1]+','+QayemniHeader[2]+','+QayemniHeader[3]+','+QayemniHeader[4]+'\n')
        file.write(scores[0]+','+scores[1]+','+scores[2]+','+scores[3]+','+scores[4]+'\n')

#getStat: prints out system rating scores
def getStat():

    with open('QayemniStats.txt', 'r') as file:
        lines=file.read().split('\n')
        QayemniHeader=lines[0].split(',')
        scores=lines[1].split(',')
    all = int(scores[4])

    if all == 0:
        all = 1

    print('\n-------------In getStat()-------------:')
    print(QayemniHeader[0], (int(scores[0]) / all) * 100, '%')
    print(QayemniHeader[1], (int(scores[1]) / all) * 100, '%')
    print(QayemniHeader[2], (int(scores[2]) / all) * 100, '%')
    print(QayemniHeader[3], (int(scores[3]) / all) * 100, '%')
    print('Where total scores:', all)
    print('---------------------------------------\n\n')

#test: receives a sample for analyze and returns analysis result
def test(sample, model):
    return model.predict(
        [sample.replace(',', ' ').replace('"""', ' ').replace('""', ' ').replace('   ', ' ').replace('  ', ' ')])

#initialize: trains the classifier using Linear SVM and by the specified dataset (csv file) and saves it then on disk
def initialize():
    import pandas as pd
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.svm import LinearSVC
    from imblearn.pipeline import Pipeline

    data = pd.read_csv('all without duplicates.csv', sep=',', )

    Targets_list = data['Target'].values.astype('U')
    features = (data['tweet_w_EOL'] + " " + data['created_at']).values.astype('U')

    pipeline = Pipeline([('vect', TfidfVectorizer(ngram_range=(1, 1), sublinear_tf=True)),
                         ('clf', LinearSVC(C=1.0, penalty='l1', max_iter=1000, dual=False))])

    model = pipeline.fit(features, Targets_list)
    # save the classifier
    with open('my_dumped_classifier.pkl', 'wb') as fid:
        pickle.dump(model, fid)

# TabayanModel: loads the trained model
def TabayanModel():

    with open('my_dumped_classifier.pkl', 'rb') as fid:
        model_loaded = pickle.load(fid)
    return model_loaded



# Token of bot
token='1357395762:AAGJs1Jg3TjSRsUFfDtfDbIQdM6qnbpa7Po' # For @TabayanBot
token1='1121491338:AAHmC3Rx1Z976mw6k23eR-mv61s4iKw0jwA' # For @Tabayantest2bot

#Defining bot object
My_bot = BotHandler(token)  # Bot's name

def main():
    new_offset = 0
    print('Now launching...')
    # initialize()  # Through this method, we have been trained the model and save it to the disk ->  No need to run this method more than one time
    trainedmodel = TabayanModel()

    # Status leaders
    verify = False
    getdate = False
    qayemni = False
    suggestion = False
    isSuggested = False
    analyze=False

    # Lists
    newsdatelist = ['لا أعلم', 'حدد تاريخ النشر']
    suggestionlist = ['لا شكراً', 'أود تقديم مقترح']
    Qayemnilist = ['غير راض جداً', 'غير راض', 'راض', 'راض جداً']
    def_msgs = ["عرف بنفسك", "عرفنا بنفسك", "عرف عن نفسك", "عرفنا عن نفسك", "كلمنا عن نفسك", "حدثنا عن نفسك",
                "تحدث عن نفسك", "تكلم عن نفسك", "من أنت", "من انت", "مين أنت","من تكون" ,"مين انت"]

    while True:
        all_updates = My_bot.get_updates(new_offset)
        # Following lines (in while loop) will be compiled once a message has been received

        if len(all_updates) > 0:

            for current_update in all_updates:
                print("current_update = ", current_update)
                first_update_id = current_update['update_id']
                
                # Defines if the message is original or edited message
                try:
                    current_update['message']
                    add = ''
                except:
                    add = 'edited_'

                # Defines message text
                if 'text' not in current_update[add + 'message']:
                    first_chat_text = 'New member'
                else:
                    first_chat_text = current_update[add + 'message']['text']

                # Defines message id
                first_chat_id = current_update[add + 'message']['chat']['id']

                # Defines message sender
                if 'first_name' in current_update[add + 'message']:
                    first_chat_name = current_update[add + 'message']['chat']['first_name']
                elif 'from' in current_update[add + 'message']:
                    first_chat_name = current_update[add + 'message']['from']['first_name']
                else:
                    first_chat_name = "unknown"

            # Defines message source ( Group || private chat)
            message_source = current_update[add + 'message']['chat']['type']
            print('message_source = ', message_source)



            if (message_source == 'group'):

                try:
                    # Defines message type ( mention || Reply || ...)
                    type = current_update[add + 'message']['entities'][0]['type']  # this is mean the text has a mention to the bot.
                    print("type=", type)

                    if type == 'mention' and '@TabayanBot' in first_chat_text: #  === Is it mention to the bot?
                        mention = True
                        first_chat_text = first_chat_text.replace('@TabayanBot','').replace('  ', ' ')

                    else:
                        mention = False
                except:
                    print("Not mention")
                    mention = False

                try:
                    # If ['reply_to_message'] is existed through 'message' properties ->  Reply message
                    orignal_text = current_update[add + 'message']['reply_to_message']['text']
                    reply = True
                except:
                    print("Not reply")
                    orignal_text = ''
                    reply = False

                if (mention or reply):

                    print("first_chat_text = ", first_chat_text, 'and its length:', len(first_chat_text))
                    if ('الرجاء التحقق من التالي' in first_chat_text):

                        first_chat_text = first_chat_text.replace('الرجاء التحقق من التالي','').replace('  ', ' ')

                        if (len(first_chat_text) > 13):

                            detectionResult = test(first_chat_text, trainedmodel)
                            print('Prediction:', detectionResult[0], ',News text:', first_chat_text)

                            if (detectionResult[0] == 'Non-rumor'):
                                message = 'ليست إشاعة ✅'
                            else:
                                message = 'إشاعة ❌'

                            My_bot.send_reply(first_chat_id, "الخبر : {} \n"
                                                             ""
                                                             "نتيجة التحقق : {}".format(first_chat_text, message),
                                              current_update[add + 'message']['message_id'])

                            # Saving classifier results on disk (For improvement purpose)
                            with open('Classifiers_results.csv', 'a') as file:
                                wr = csv.writer(file)

                                wr.writerow(["{}".format(detectionResult[0]), "{}".format(first_chat_text)])
                            ###########################################################

                        elif (reply and len(orignal_text) > 13 and current_update[add + 'message']['reply_to_message']['from']['username'] != 'TabayanBot'):

                            detectionResult = test(orignal_text, trainedmodel)
                            print('Prediction:', detectionResult[0], ',News text:', orignal_text)

                            if (detectionResult[0] == 'Non-rumor'):
                                message = 'ليست إشاعة ✅'
                            else:
                                message = 'إشاعة ❌'

                            My_bot.send_reply(first_chat_id, "الخبر : {} \n"
                                                             ""
                                                             "نتيجة التحقق : {}".format(orignal_text, message),
                                              current_update[add + 'message']['message_id'])

                            # Saving classifier results on disk (For improvement purpose)
                            with open('Classifiers_results.csv', 'a') as file:
                                wr = csv.writer(file)

                                wr.writerow(["{}".format(detectionResult[0]), "{}".format(orignal_text)])
                            ###########################################################

                        else:
                            My_bot.send_reply(first_chat_id, "يهدف تبيّن إلى مساعدة مرتادي منصة التلقرام عن طريق توفير خدمة تمكنهم من التحقق من صحة الأخبار، ولتحقيق هذا الغرض، يرجى استخدام أوامر التحقق للإشارة إلى الأخبار فقط !",current_update[add + 'message']['message_id'])


                    elif ('تحقق' in first_chat_text):

                        if(not reply):#mention only
                            My_bot.send_reply(first_chat_id, "مع الإشارة إليّ، يرجى الرد على الخبر 'Reply' مع تضمين 'تحقق'، أو، ابدأ الخبر المراد التحقق منه بـ'الرجاء التحقق من التالي:'..\n",current_update[add + 'message']['message_id'])
                        elif len(orignal_text)<13 or current_update[add + 'message']['reply_to_message']['from']['username'] == 'TabayanBot' :
                            My_bot.send_reply(first_chat_id, "يهدف تبيّن إلى مساعدة مرتادي منصة التلقرام عن طريق توفير خدمة تمكنهم من التحقق من صحة الأخبار، ولتحقيق هذا الغرض، يرجى استخدام أوامر التحقق عند الإشارة إلى الأخبار فقط !",current_update[add + 'message']['message_id'])
                        else:

                            detectionResult = test(orignal_text, trainedmodel)
                            print('Prediction:', detectionResult[0], ',News text:', orignal_text)

                            if (detectionResult[0] == 'Non-rumor'):
                                message = 'ليست إشاعة ✅'
                            else:
                                message = 'إشاعة ❌'

                            My_bot.send_reply(first_chat_id, "الخبر : {} \n"
                                                             ""
                                                             "نتيجة التحقق : {}".format(orignal_text, message),
                                              current_update[add + 'message']['message_id'])

                            # Saving classifier results on disk (For improvement purpose)
                            with open('Classifiers_results.csv', 'a') as file:
                                wr = csv.writer(file)

                                wr.writerow(["{}".format(detectionResult[0]), "{}".format(orignal_text)])
                            ###########################################################

                    elif len(first_chat_text)<3:
                        if (not reply): #Mention only
                            My_bot.send_reply(first_chat_id,
                                              "السلام عليكم ورحمة الله وبركاته , أنا تبيّن، مكتشف الشائعات !\n للتحقق من خبر ما إن كان إشاعة أم لا، أشر إلى الحساب الخاص بي 'Reply' مع  كلمة 'تحقق' للرسالة التي تتضمن الخبر الذي تود التحقق منه أو،\n أشر إلى الحساب مع تضمين 'الرجاء التحقق من التالي' في بداية الرسالة لتفعيل خدمة التحقق. "
                                              "\n"
                                              "ملاحظة: يفضّل تضمين تاريخ نشر الخبر مع الخبر للحصول على أفضل النتائج.."
                                              "\n\n"
                                              "هذا كل شيء، شكراً لاستخدامكم تبيّن. 😊"
                                              , current_update[add + 'message']['message_id'])

                        else:
                            My_bot.send_reply(first_chat_id," الرجاء تضمين كلمة 'تحقق' إن كنت تود التحقق من الخبر المشار إليه ..",current_update[add + 'message']['message_id'])

                    elif (("سلام" in first_chat_text and len(first_chat_text) < 13) or "السلام عليكم" in first_chat_text) and (len(first_chat_text) < 50):
                            My_bot.send_reply(first_chat_id, 'وعليكم السلام ورحمة الله وبركاته',current_update[add + 'message']['message_id'])

                    elif ("مشكور" in first_chat_text or "شكرا" in first_chat_text) and len(first_chat_text) < 40:
                            My_bot.send_reply(first_chat_id, 'أهلاً وسهلاً 🤍، '
                                                             '\n'
                                                             'نأمل أن يكون حاز على رضاك واستحسانك 😊.',current_update[add + 'message']['message_id'])

                    elif ("اهلا" in first_chat_text or "أهلا" in first_chat_text) and len(first_chat_text) < 35:
                            My_bot.send_reply(first_chat_id, 'أهلاً وسهلاً بك 🤍',current_update[add + 'message']['message_id'])

                    elif ("هلا" == first_chat_text or "مرحبا" in first_chat_text) and (len(first_chat_text) < 30):
                            My_bot.send_reply(first_chat_id, 'أهلاً وسهلا ً',current_update[add + 'message']['message_id'])

                    elif ("حياك" in first_chat_text) and (len(first_chat_text) < 20):
                            My_bot.send_reply(first_chat_id, 'الله يحييك',current_update[add + 'message']['message_id'])

                    elif ("اخبارك" in first_chat_text or "أخبارك" in first_chat_text) and (len(first_chat_text) < 30):
                            My_bot.send_reply(first_chat_id, 'فرحان فيكم🤍',current_update[add + 'message']['message_id'])

                    elif ("كيف حالك" in first_chat_text or "كيف الحال" in first_chat_text) and (len(first_chat_text) < 30):
                            My_bot.send_reply(first_chat_id, 'عال العال', current_update[add + 'message']['message_id'])  # To mention: ('\n@'+current_update[add+'message']['from']['username']+'\n')

                    elif ("صباح ال" in first_chat_text) and len(first_chat_text) < 40:
                            My_bot.send_message(first_chat_id, 'صباح النور والسرور ياهلا !')

                    elif ("مساء ال" in first_chat_text) and len(first_chat_text) < 40:
                            My_bot.send_message(first_chat_id, 'مساء النور أهلاً وسهلاً !')

                    elif ((any(i in first_chat_text for i in def_msgs) and (len(first_chat_text) < 40)) or len(first_chat_text) < 2):
                            My_bot.send_reply(first_chat_id,
                                              "السلام عليكم ورحمة الله وبركاته , أنا تبيّن، مكتشف الشائعات !\n للتحقق من خبر ما إن كان إشاعة أم لا، أشر إلى الحساب الخاص بي 'Reply' مع  كلمة 'تحقق' للرسالة التي تتضمن الخبر الذي تود التحقق منه أو،\n أشر إلى الحساب مع تضمين 'الرجاء التحقق من التالي' في بداية الرسالة لتفعيل خدمة التحقق. "
                                              "\n"
                                              "ملاحظة: يفضّل تضمين تاريخ نشر الخبر مع الخبر للحصول على أفضل النتائج.."
                                              "\n\n"
                                              "هذا كل شيء، شكراً لاستخدامكم تبيّن. 😊"
                                              , current_update[add + 'message']['message_id'])
                    else:

                        if len(first_chat_text) > 5 and first_chat_text != '/start' and first_chat_text not in Qayemnilist and first_chat_text not in suggestionlist and first_chat_text not in newsdatelist:
                            with open('UnexpectedMessages.txt', 'a') as file:
                                file.write(first_chat_text + ",\r\n")
                            print("Unexpected message has been added to UnexpectedMessages.txt")

                    new_offset = first_update_id + 1

                else:# Not 'mention' nor 'Reply'
                    new_offset = first_update_id + 1


            else:  # Message from a private chat.

                if first_chat_text == '/start':
                    My_bot.send_message(first_chat_id, first_chat_name + ' !\n'
                                        "مرحباً بك في تبيّن ، مكتشف الشائعات !\nللتحقق من خبر ما إن كان إشاعة أم لا، أرسل كلمة 'تحقق' أما إن وددت الخروج، فأرسل 'إنهاء'..  "
                                        "\n"
                                        "ملاحظة: يفضّل تضمين تاريخ نشر الخبر مع الخبر للحصول على أفضل النتائج."
                                        "\n\n"
                                        "\n"
                                        "هذا كل شيء، شكراً لاستخدامك تبيّن. 😊")


                elif verify:
                    newstext = first_chat_text
                    
                    if (len(newstext) < 13):
                        My_bot.send_message(first_chat_id,
                                            "يهدف تبيّن إلى مساعدة مرتادي منصة التلقرام عن طريق توفير خدمة تمكنهم من التحقق من صحة الأخبار، ولتحقيق هذا الغرض، يرجى استخدام أوامر التحقق عند الإشارة إلى الأخبار فقط !")
                    
                    else:
                        My_bot.send_multipleChoiceMessage(first_chat_id, "في أي تاريخ تم نشر الخبر؟ ", newsdatelist)
                        getdate = True
                    
                    
                    verify = False
                        
                elif getdate:

                    getdate = False
                    analyze = True

                    if first_chat_text == 'حدد تاريخ النشر':
                        My_bot.send_message(first_chat_id, "إذاً، من فضلك أدخل تاريخ النشر باستخدام الصيغة التالية: "
                                                           "yyyy-mm-dd"
                                                           "\n\n"
                                                           "مثال: 16-07-2020")

                        knwondate = True

                    else:
                        knwondate = False
                        continue

                elif analyze:


                    if knwondate:
                        newstext += " " + first_chat_text
                        print('date:',first_chat_text)

                    detectionResult = test(newstext, trainedmodel)
                    print('Prediction:',detectionResult[0],',News text:',newstext)

                    if (detectionResult[0] == 'Non-rumor'):
                        message = 'ليست إشاعة ✅'
                    else:
                        message = 'إشاعة ❌'

                    newstext= newstext[:len(newstext) - len(first_chat_text)]

                    My_bot.send_message(first_chat_id, "الخبر : {} \n"
                                                       "\n"
                                                       "نتيجة التحقق : {}".format(newstext, message))

                    # Saving classifier results on disk (For improvement purpose)
                    with open('Classifiers_results.csv', 'a') as file:
                        wr = csv.writer(file)
                        if knwondate:
                            date=first_chat_text
                        else:
                            date=datetime.datetime.today().strftime("%d-%B-%Y %H:%M:%S")

                        wr.writerow(["{}".format(detectionResult[0]), "{}".format(newstext),"{}".format(date)])
                    ###########################################################

                    analyze = False

                elif qayemni:

                    isParticipated = True
                    # ['غير راض جداً', 'غير راض', 'راض', 'راض جداً']
                    if first_chat_text == 'غير راض جداً':
                        addScore(1)
                    elif first_chat_text == 'راض جداً':
                        addScore(4)
                    elif first_chat_text == 'راض':
                        addScore(3)
                    elif first_chat_text == 'غير راض':
                        addScore(2)
                    else:
                        print('Unexpected score:', first_chat_text)
                        isParticipated = False

                        My_bot.send_message(first_chat_id, "شاكرين لك استخدامك تبيّن،"
                                                           "\n"
                                                           "إلى اللقاء 😊💛."
                                                           "\n")


                    getStat()

                    if isParticipated:
                        My_bot.send_multipleChoiceMessage(first_chat_id, 'شكراً لك، نقدر لك هذا..'
                                                                         '\n'
                                                                         'كما نسعد بأي اقتراحات إن وددت، ستكون محل اهتمامنا بكل تأكيد.',suggestionlist)
                        suggestion = True

                    qayemni = False
                    print("the message text = ", first_chat_text)

                elif suggestion:
                    if first_chat_text == 'أود تقديم مقترح':
                        My_bot.send_message(first_chat_id, "تفضل !")
                        isSuggested = True
                    else:
                        My_bot.send_message(first_chat_id, "حسناً !"
                                                           "\n"
                                                           "شكراً لاستخدامك تبيّن، إلى اللقاء 😊💛."
                                                           "\n")

                    suggestion = False

                elif isSuggested:

                    if first_chat_text != '/start' and len(first_chat_text) > 5:
                        with open('Suggestions.txt', 'a') as file:
                            file.write(first_chat_text + ",\r\n")

                    My_bot.send_message(first_chat_id, "شاكرين ومقدرين لك إسهامك في تحسين تبيّن، شكراً لك !"
                                                       "\n\n")

                    isSuggested = False

                elif first_chat_text == 'أود تقديم مقترح':
                    suggestion = True
                    continue

                elif ('أهلا' in first_chat_text or 'اهلا' in first_chat_text or 'اهلا وسهلا' in first_chat_text or 'هلا' == first_chat_text or "مرحبا" in first_chat_text) and (len(first_chat_text) < 40):
                    My_bot.send_message(first_chat_id,("أهلاً وسهلاً بك "+first_chat_name+" 🤍، إن لم تكن على معرفة بيّ، فيمكنك سؤالي عن من أكون.. \nمثل، من تكون؟، من أنت؟، عرفني عن نفسك! \n\n\n"))

                elif 'تحقق' in first_chat_text and (len(first_chat_text) < 13):
                    My_bot.send_message(first_chat_id, "الرجاء إرسال الخبر الذي تود التحقق منه")
                    verify = True

                elif (first_chat_text == 'مساعدة' or (any(i in first_chat_text for i in def_msgs) and (len(first_chat_text) < 25))):
                    My_bot.send_message(first_chat_id,
                                        "السلام عليكم ورحمة الله وبركاته، أنا تبيّن، مكتشف الشائعات !\nللتحقق من خبر ما إن كان إشاعة أم لا، أرسل كلمة 'تحقق' أما إن وددت الخروج، فأرسل 'إنهاء'..  "
                                        "\n"
                                        "ملاحظة: يفضّل تضمين تاريخ نشر الخبر مع الخبر للحصول على أفضل النتائج."
                                        "\n\n"
                                        "\n"
                                        "هذا كل شيء، شكراً لاستخدامك تبيّن 😊🤍.")
                elif (("السلام عليكم" in first_chat_text or "سلام" == first_chat_text) and (len(first_chat_text) < 25)) or len(first_chat_text) < 2:
                   My_bot.send_message(first_chat_id,('وعليكم السلام ورحمة الله وبركاته،أهلاً وسهلاً بك '+first_chat_name+'🤍، إن لم تكن على معرفة بيّ، فيمكنك سؤالي عن من أكون.. \nمثل، من تكون؟، من أنت؟، عرفني عن نفسك! \n\n\n'))

                elif ("صباح ال" in first_chat_text) and len(first_chat_text) < 20:
                    My_bot.send_message(first_chat_id, 'صباح النور والسرور ياهلا !')
                    print("the message text = ", first_chat_text)

                elif ("مساء ال" in first_chat_text) and len(first_chat_text) < 20:
                    My_bot.send_message(first_chat_id, 'مساء النور أهلاً وسهلاً !')
                    print("the message text = ", first_chat_text)

                elif ("كيف حالك" in first_chat_text or "كيف الحال" in first_chat_text) and (len(first_chat_text) < 20):
                    My_bot.send_message(first_chat_id, 'عال العال')
                    print("the message text = ", first_chat_text)

                elif ("اخبارك" in first_chat_text or "أخبارك" in first_chat_text) and (len(first_chat_text) < 20):
                    My_bot.send_message(first_chat_id, 'فرحان فيك 🤍')
                    print("the message text = ", first_chat_text)

                elif ("حياك" in first_chat_text) and (len(first_chat_text) < 20):
                    My_bot.send_message(first_chat_id, 'الله يحييك')
                    print("the message text = ", first_chat_text)

                elif 'إنهاء' in first_chat_text or 'انهاء' in first_chat_text and (len(first_chat_text) < 13):
                    My_bot.send_message(first_chat_id, 'شكراً لاستخدامك  تبيّن، نأمل أن يكون حاز على رضاك واستحسانك.')

                    My_bot.send_multipleChoiceMessage(first_chat_id, 'قيمني:'
                                                                     '\n'
                                                                     'نسعى دائماً لتقديم الأفضل لكم، لذا نرجو منك تقييم الخدمة المقدمة لك إذا تفضلت 😊',
                                                      Qayemnilist)
                    qayemni = True

                    print("the message text = ", first_chat_text)

                elif ("مشكور" in first_chat_text or "شكرا" in first_chat_text) and 'لا شكراً' != first_chat_text and len(first_chat_text) < 20:
                    My_bot.send_message(first_chat_id, 'اهلاً وسهلاً 😊🤍.'
                                                       '\n'
                                                       'شكراً لاستخدامك  تبيّن، نأمل أن يكون حاز على رضاك واستحسانك.')

                    My_bot.send_multipleChoiceMessage(first_chat_id, 'قيمني:'
                                                                     '\n'
                                                                     'نسعى دائماً لتقديم الأفضل لكم، لذا نرجو منك تقييم الخدمة المقدمة لك إذا تفضلت 😊',
                                                      Qayemnilist)
                    qayemni = True
                    print("the message text = ", first_chat_text)

                else:
                    My_bot.send_message(first_chat_id, "الرجاء إرسال كلمة 'تحقق' لتفعيل خدمة التحقق من الأخبار، 'إنهاء' لإنهاء المحادثة أو 'مساعدة' إن أردت إعادة تعريف النظام. "
                                                       '\n')
                    print("Unexpected message:", first_chat_text)
                    if (len(first_chat_text) > 5 and first_chat_text != '/start' and first_chat_text not in Qayemnilist and first_chat_text not in suggestionlist and first_chat_text not in newsdatelist):
                        with open('UnexpectedMessages.txt', 'a') as file:
                            file.write(first_chat_text + ",\r\n")
                        print("Unexpected message has been added to UnexpectedMessages.txt")


                new_offset = first_update_id + 1




if __name__ == '__main__':
    try:
        main()
        print('Done !')
    except KeyboardInterrupt:
        exit()

# This code has been written by Rawan Mohammed Alowaymir and Abdulmalik Sulaiman Alaqel
# Developers Information:
# Rawan Mohammed Alowaymir, Email:rawan864md@gmail.com
# Abdulmalik Sulaiman Alaqel, Email: Mloooki.3@gmail.com