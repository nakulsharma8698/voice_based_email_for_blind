from json import decoder, encoder
from django.http.request import HttpHeaders, HttpRequest
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
# from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm, LoginForm
from .models import User
import speech_recognition as sr
import time
from gtts import gTTS
import os
from playsound import playsound
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .EmailFunction import *


def signup_view(request):

    if request.user.is_authenticated and request.user.is_active:
        return redirect("myapp:home")
    if request.user.is_authenticated and not request.user.is_active:
        return redirect("myapp:auth")

    if request.method == 'POST':
        print(request.POST)
        file = 'test'
        i = '1'

        texttospeech(
            "Welcome to our Voice Based Email Portal. Signup with your Email account to continue. ", file + i)
        i = i + str(1)

        email = introVoice('email', file, i)
        print(email)
        UserObj = User.objects.filter(email=email).first()
        print(UserObj)
        # UserObj = get_object_or_404(User, email=email)
        if(UserObj):
            texttospeech("Account Already Exists, Try Again", file + i)
            i = i + str(1)
            return JsonResponse({'result': 'failure'})

        name = introVoice('Name', file, i)
        passs = introVoice('password', file, i)
        gpass = introVoice('G-Mail Password', file, i)
        # confirmPass = introVoice('password again',file,i)
        try:
            obj = User.objects.create_user(
                email=email, password=passs, name=name, gpass=gpass)
            obj.is_active = False
            obj.save()
            print(obj)
        except:
            print("Some error")
            texttospeech("There was some error, Please try again", file+i)
            return JsonResponse({'result': 'failure'})

        user = authenticate(email=email, password=passs)

        if user:
            login(request, user)
            return JsonResponse({'result': 'success'})
        else:
            return JsonResponse({'result': 'failure'})
    else:
        form = SignUpForm()
        return render(request, 'myapp/signup.html', {'form': form})


def home_view(request):
    context = {}
    user = request.user
    print("Printing in views")
    if not user.is_authenticated:
        return redirect("myapp:first")

    if not user.is_active:
        return redirect("myapp:auth")

    print("--------------", user.email)
    print("=========", user.gpass)
    MailList = ReadMails(user.email, user.gpass)

    if request.method == 'POST':
        flag = True
        file = 'test'
        i = '0'

        texttospeech(
            "You are logged into your account. What would you like to do ?", file + i)
        i = i + str(1)
        while (flag):
            action = ''
            texttospeech(
                 "To compose an email say 1."
                 "To open Inbox folder say 2. "
                 "To open Sent folder say 3. "
                 "To Read mails say 4. "
                 "To Read Trash Mails say 5. "
                 "To search an email say 6. "
                 "To Logout say 9. "
                "Say 0 to hear again.",
                file + i)
            i = i + str(1)
            act = speechtotext(5)
            act = act.strip()
            act = act.replace(' ', '')
            act = act.lower()

            if act == 'yes':
                continue
            elif act == '1' or act == 'one':
                return JsonResponse({'result': 'compose'})
            elif act == '2' or act == 'two':
                return JsonResponse({'result': 'inbox'})
            elif act == '3' or act == 'three':
                return JsonResponse({'result': 'sent'})
            elif act == '4' or act == 'four' or act == 'fore' or act == 'for' or act == 'aur':
                ans, action = Read(MailList, file, i)
                print(ans, action)
                if action == 'read':
                    if ans >= 0:
                        print("reached on line 114")
                        return JsonResponse({'result': 'read', 'id': ans})
                elif action == 'delete':
                    if ans >= 0:
                        # print("reached on line 114")
                        # return JsonResponse({'result': 'delete', 'id': ans})

                        deletemails(ans, request.user.email, request.user.gpass)
                        texttospeech('Mail moved to trash!', file)
                        return JsonResponse({'result': 'home'})

            elif act == '5' or act == 'five':
                return JsonResponse({'result': 'trash'})

            elif act == '6' or act == 'six' or act == 'pix' or act=='sex':
                texttospeech("Please speak a keyword to search", file+i)
                i = i + str(1)
                say = speechtotext(10)
                return JsonResponse({'result': 'search', 'key':say})

            elif act == '9' or act == 'nine':
                texttospeech(
                    "You have been logged out of your account and now will be redirected back to the login page.",
                    file + i)
                i = i + str(1)
                return JsonResponse({'result': 'logout'})
            elif act == '0' or act == 'zero':
                texttospeech("Repeating again", file + i)
                i = i + str(1)
                continue
            else:
                texttospeech("Invalid action. Please try again.", file + i)
                i = i + str(1)
                continue

    return render(request, 'myapp/home.html', {'userobj': user, 'MailList': MailList,  'page_heading':'INBOX'})


def Read(MailList, file, i):
    for j in range(0, len(MailList)):
        k = MailList[j]
        texttospeech("Mail number"+str(j)+",is sent by "+k.senderName+" on "+k.date+" and Subject is " +
                     k.subject+". Do you want to read it? say yes to read, no to continue or delete to move mail to trash", file+i)
        i = i + str(1)
        say = speechtotext(10)
        print(say)
        action = ''
        if say == 'yes' or say == "Yes" or say == "Yes Yes":
            action = 'read'
            return j, action
        elif say == 'delete':
            action = 'delete'
            return j, action
        else:
            continue
    return -1


# def SearchList(MailList, file, i):
#     for j in range(0, len(MailList)):
#         k = MailList[j]
#         texttospeech("Mail number"+str(j)+",is sent by "+k.senderName+" on "+k.date+" and Subject is " +
#                      k.subject+". Do you want to read it? say yes to read, no to continue or delete to move mail to trash", file+i)
#         i = i + str(1)
#         say = speechtotext(10)
#         print(say)
#         action = ''
#         if say == 'yes' or say == "Yes" or say == "Yes Yes":
#             action = 'read'
#             return j, action
#         elif say == 'delete':
#             action = 'delete'
#             return j, action
#         else:
#             continue
#     return -1

def search_view(request, key):
    print("=============************", key)
    user = request.user
    file = 'test'
    i = '0'
    print("--------------", user.email)
    MailList = searchMails(user.email, user.gpass, key)
    print("**********************", MailList)
    if request.method == 'GET':
        if MailList:
            return render(request, 'myapp/search.html', {'userobj': user, 'MailList': MailList, 'page_heading': 'SEARCH', 'key': key})

        texttospeech("No mail with the keyword " + key + " found, Redirecting back to home", file + i)
        return redirect('myapp:home')

    elif request.method == 'POST':
        print('+++++++++++++++++++POST')
        flag = True
        file = 'test'
        i = '0'
        ans = ReadSearch(MailList, file, i)
        if ans >= 0:
            print("reached on line 563")
            return JsonResponse({'result': 'read', 'key':key, 'id': ans })
        elif ans == -2:
            return JsonResponse({'result': 'home'})
        texttospeech("No more mails in Search Box, Redirecting back to Home", file + i)
        i = i + str(1)
        return JsonResponse({'result': 'home'})


def ActionVoice():
    flag = True
    addr = ''
    passs = ''
    file = 'test'
    while (flag):
        texttospeech("Enter your"+email, file + i)
        i = i + str(1)
        addr = speechtotext(10)
        if addr != 'N':
            texttospeech("You meant " + addr +
                         " say yes to confirm or no to enter again", file + i)

            i = i + str(1)
            say = speechtotext(10)
            print(say)
            if say == 'yes' or say == 'Yes' or say == 'yes yes':
                flag = False
                addr = addr.strip()
                addr = addr.replace(' ', '')
                addr = addr.lower()
                addr = convert_special_char(addr)
                return addr
        else:
            texttospeech("could not understand what you meant:", file + i)
            i = i + str(1)


def first(request):
    context = {}

    user = request.user
    if user.is_authenticated and user.is_active:
        return redirect("myapp:home")

    if user.is_authenticated and not user.is_active:
        return redirect("myapp:auth")

    return render(request, 'myapp/first.html', context)


def texttospeech(text, filename):
    filename = filename + '.mp3'
    flag = True
    while flag:
        try:
            tts = gTTS(text=text, lang='en', slow=False)
            tts.save(filename)
            flag = False
        except:
            print('Trying again')
    playsound(filename)
    os.remove(filename)
    return


def speechtotext(duration):
    global i, addr, passwrd
    file = 'test'
    i = '1'
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=1)
        texttospeech('Speak', file + i)
        audio = r.listen(source, phrase_time_limit=duration)
    try:
        response = r.recognize_google(audio)
        print(response)
    except:
        response = 'N'
    return response


def convert_special_char(text):
    temp = text
    special_chars = ['dot', 'underscore', 'dollar', 'hash', 'star',
                     'plus', 'minus', 'space', 'dash', 'at the rate', 'attherate', 'zero']
    for character in special_chars:
        while(True):
            pos = temp.find(character)
            if pos == -1:
                break
            else:
                if character == 'dot':
                    temp = temp.replace('dot', '.')
                elif character == 'underscore':
                    temp = temp.replace('underscore', '_')
                elif character == 'zero':
                    temp = temp.replace('zero', '0')
                elif character == 'dollar':
                    temp = temp.replace('dollar', '$')
                elif character == 'hash':
                    temp = temp.replace('hash', '#')
                elif character == 'star':
                    temp = temp.replace('star', '*')
                elif character == 'plus':
                    temp = temp.replace('plus', '+')
                elif character == 'minus':
                    temp = temp.replace('minus', '-')
                elif character == 'space':
                    temp = temp.replace('space', '')
                elif character == 'dash':
                    temp = temp.replace('dash', '-')
                elif character == 'at the rate':
                    temp = temp.replace('at the rate', '@')
                elif character == 'attherate':
                    temp = temp.replace('attherate', '@')
    return temp.strip()


def logout_view(request):
    logout(request)
    return redirect("myapp:first")


def introVoice(email, file, i):
    flag = True
    addr = ''
    passs = ''
    while (flag):
        texttospeech("Enter your"+email, file + i)
        i = i + str(1)
        addr = speechtotext(10)
        if addr != 'N':
            texttospeech("You meant " + addr +
                         " say yes to confirm or  no to enter again or exit to terminate the program", file + i)

            i = i + str(1)
            say = speechtotext(10)
            print(say)
            if say == 'yes' or say == 'Yes' or say == 'yes yes':
                flag = False
                addr = addr.strip()
                addr = addr.replace(' ', '')
                addr = addr.lower()
                addr = convert_special_char(addr)
                return addr
            elif say == 'exit':
                flag = False
                time.sleep(60)
                texttospeech(
                    "The application will restart in a minute", file+i)
                i = i + str(1)
                return JsonResponse({'result': 'failure', 'message': 'message'})

        else:
            texttospeech("could not understand what you meant:", file + i)
            i = i + str(1)


def login_view(request):
    context = {}
    if request.user.is_authenticated and request.user.is_active:
        return redirect("myapp:home")

    if request.user.is_authenticated and not request.user.is_active:
        return redirect("myapp:auth")

    if request.method == 'POST':
        file = 'test'
        i = '1'
        text1 = "Welcome to our Voice Based Email Portal. Login with your email account to continue. "
        texttospeech(text1, file + i)
        i = i + str(1)

        emailId = introVoice('email', file, i)

        account = User.objects.filter(email=emailId).first()
        print("---------------->", account)

        if account:
            print("User Exists")
            passs = introVoice("Password", file, i)
            # form = LoginForm(email=addr,password=passs,auth_code='1010101010')
            # if account:
            # auth_code = '1010101010'
            user = authenticate(email=emailId, password=passs)
            print("USER--------->>>", user)

            if user is not None:
                if not account.is_active:
                    print(
                        "Your account is not active, create authentication code to continue")
                    message = 'Account not active'
                    texttospeech(
                        "Your account is not active, create authentication code to continue", file + i)
                    i = i + str(1)
                    login(request, user)
                    return JsonResponse({'result': 'failure-active', 'message': message})

                login(request, user)
                return JsonResponse({'result': 'success'})
            else:
                message = 'Incorrect Password!'
                texttospeech("Please enter correct password !", file + i)
                i = i + str(1)
                return JsonResponse({'result': 'failure', 'message': message})
        else:
            print(emailId, "does not exist!")
            texttospeech("Please enter correct email address!", file+i)
            i = i + str(1)
            message = 'Please enter correct email address!'
            return JsonResponse({'result': 'failure', 'message': message})
    else:
        context['form'] = LoginForm()

    return render(request, 'myapp/login.html', context)


def auth_view(request):
    file = 'test'
    i = '1'
    user = request.user
    if request.method == 'GET':
        context = {}
        print('testng')
        if not user.is_authenticated:
            return redirect("myapp:first")

        if user.is_active:
            # verify Auth Code
            texttospeech(
                "Account already active, enter 10 digit authentication code using mouse clicks", file + i)
            i = i + str(1)
            print("Account already active, enter authentication code using mouse clicks")

        if not user.is_active:
            # create Auth Code
            texttospeech(
                "Enter 10 digit authentication code using mouse clicks to continue", file + i)
            i = i + str(1)
            print("Account not active, create auth code")

        print("Email address----------->", user.email)

        return render(request, 'myapp/login2.html', context)
    else:
        print("We have reached here")
        code = request.POST['authcode']
        print(code)
        print(user.auth_code)
        if user.auth_code:
            if user.auth_code == code:
                texttospeech("User authentication completed", file+i)
                i = i + str(1)
                return redirect('myapp:home')
            else:
                texttospeech(
                    "Authentication failed , please try again!", file+i)
                i = i + str(1)
        else:
            u = User.objects.filter(email=user.email).first()
            u.auth_code = code
            u.is_active = True
            u.save()
            texttospeech("Account successfully created", file+i)
            i = i + str(1)
            return redirect('myapp:home')
        return render(request, 'myapp/login2.html')


def compose_view(request):
    file = 'test'
    i = '1'
    user = request.user
    if request.method == 'POST':
        print("hit post request in compose view")
        # entering sender's email address
        recievers_addr = introVoice('Senders Address', file, i)
        print("recievers_addr-->")
        print(recievers_addr)
        subject = introVoice('Subject', file, i)
        print("subject-->")
        print(subject)
        # entering content
        msg = composeMessage(file, i)
        print("msg---->")
        print(msg)
        read = composeVoice(
            "Do you want to read it. Say yes to read or no to proceed further", file, i)
        print(read)
        if read == "yes":
            texttospeech(msg, file+i)
            i = i+str(1)
        composeAction = composeVoice(
            "Say delete to discard the draft or rewrite to compose again or send to send the draft", file, i)
        print(composeAction)
        if composeAction == 'delete':
            print("deleting")
            msg = ""
            texttospeech(
                "Draft has been deleted and you have been redirected to home page", file+i)
            i = i+str(1)
            return JsonResponse({'result': 'success'})
        elif composeAction == 'rewrite':
            print("rewriting")
            return JsonResponse({'result': 'rewrite'})
        elif composeAction == 'send':
            u = User.objects.filter(email=user.email).first()
            sendMail(u.email, u.gpass, recievers_addr, subject, msg)
            print("mail sent")
            texttospeech(
                "Mail sent successfully. You are now redirected to sent folder", file+i)
            i = i+str(1)
            return JsonResponse({'result': 'success'})
    print("hit get request in compose view")
    return render(request, 'myapp/compose.html')


def composeMessage(file, i):
    flag = True
    msg = ''
    while (flag):

        sentence = composeVoice("Enter the sentence", file, i)
        say = composeVoice(
            "Say continue to keep writing further or finish if you are done ", file, i)
        print(say)
        if say == 'continue' or say == 'Continue':
            msg = msg+sentence
            sentence = ""
        elif say == 'finish':
            flag = False
            msg = msg+sentence
            return msg


def composeVoice(msg, file, i):
    flag = True
    addr = ''
    passs = ''
    while (flag):
        texttospeech(msg, file + i)
        i = i + str(1)
        addr = speechtotext(10)
        if addr != 'N':
            texttospeech("You meant " + addr +
                         " say yes to confirm or no to enter again", file + i)
            i = i + str(1)
            say = speechtotext(10)
            print(say)
            if say == 'yes' or say == 'Yes' or say == 'yes yes':
                flag = False
                addr = addr.strip()
                #addr=addr.replace(' ','')
                addr = addr.lower()
                addr = convert_special_char(addr)
                return addr

        else:
            texttospeech("could not understand what you meant:", file + i)
            i = i + str(1)


def inbox_view(request):
    print("Reached Inbox View")
    return render(request, 'myapp/compose.html')


def sent_view(request):
    user = request.user
    print("--------------", user.email)
    MailList = read_sentmail(user.email, user.gpass)
    if request.method == 'GET':
        return render(request, 'myapp/sent.html',{'userobj': user, 'MailList': MailList,'page_heading':'SENT'})

    if request.method == 'POST':
        flag = True
        file = 'test'
        i = '0'
        ans = ReadSent(MailList,file,i)
        if ans >= 0:
            print("reached on line 522")
            return JsonResponse({'result': 'read', 'id': ans})

        texttospeech("No more mails in Sent Box, Redirecting back to Home", file + i)
        i = i + str(1)
        return JsonResponse({'result': 'home'})


def ReadSent(MailList, file, i):
    for j in range(0, len(MailList)):
        k = MailList[j]
        texttospeech("Mail number"+str(j)+", was sent by "+k.senderName+" on "+k.date+" and Subject is " +
                     k.subject+". Do you want to read it? say yes to read or delete to delete or continue to proceed further.", file+i)
        i = i + str(1)
        say = speechtotext(10)
        print(say)
        if say == 'yes' or say == "Yes" or say == "Yes Yes":
            return j
        if say == 'delete':
            pass
        else:
            continue
    return -1


def trash_view(request):
    user = request.user
    print("--------------", user.email)
    MailList = read_trashmail(user.email, user.gpass)
    print("**********************", MailList)
    if request.method == 'GET':
        return render(request, 'myapp/trash.html',{'userobj': user, 'MailList': MailList,'page_heading':'TRASH'})

    if request.method == 'POST':
        flag = True
        file = 'test'
        i = '0'
        ans = ReadTrash(MailList,file,i)
        if ans >= 0:
            print("reached on line 563")
            return JsonResponse({'result': 'read', 'id': ans})
        elif ans == -2:
            return JsonResponse({'result': 'home'})
        texttospeech("No more mails in Trash Box, Redirecting back to Home", file + i)
        i = i + str(1)
        return JsonResponse({'result': 'home'})


def ReadTrash(MailList, file, i):
    for j in range(0, len(MailList)):
        k = MailList[j]
        texttospeech("Mail number"+str(j)+", was sent by "+k.senderName+" on "+k.date+" and Subject is " + k.subject +
                     ". Do you want to read it? say yes to read or say continue to proceed further, or say back to go back to the main menu", file+i)
        i = i + str(1)
        say = speechtotext(5)
        print(say)
        if say == 'yes' or say == "Yes" or say == "Yes Yes":
            return j
        elif say == 'back':
            return -2
        else:
            continue
    return -1


def ReadSearch(MailList, file, i):
    for j in range(0, len(MailList)):
        k = MailList[j]
        texttospeech("Mail number"+str(j)+", was sent by "+k.senderName+" on "+k.date+" and Subject is " + k.subject +
                     ". Do you want to read it? say yes to read or say continue to proceed further, or say back to go back to the main menu", file+i)
        i = i + str(1)
        say = speechtotext(5)
        print(say)
        if say == 'yes' or say == "Yes" or say == "Yes Yes":
            return j
        elif say == 'back':
            return -2
        else:
            continue
    return -1

def read_trash_view(request, id):
    id = int(id)
    user = request.user
    MailList = read_trashmail(user.email, user.gpass)
    mail = MailList[id]
    print("Reached read Trash View")
    i = '1'
    file = "test"
    if request.method == 'GET':
        return render(request, 'myapp/readTrash.html', {'mail': mail, 'mail_id': id})

    if request.method == 'POST':
        k = mail
        flag = True
        while flag:
            texttospeech(k.body, file + i)
            i = i + str(1)
            texttospeech("Say yes to listen again or no to continue", file + i)
            say = speechtotext(10)
            i = i + str(1)
            if say == 'yes' or say == 'yes yes':
                print("Reading Trash Mail", id, "again")
                texttospeech("Reading Mail Again", file + i)
                i = i + str(1)
            else:
                flag = False
        return JsonResponse({'result': 'readtrashsuccess'})



def read_sent_view(request,id):
    id = int(id)
    user = request.user
    MailList = read_sentmail(user.email, user.gpass)
    mail = MailList[id]
    print("Reached read sent View")
    i = '1'
    file = "test"
    if request.method == 'GET':
        return render(request,'myapp/readSent.html',{'mail':mail,'mail_id':id})

    if request.method == 'POST':
        k = mail
        texttospeech(k.body, file+i)
        i = i + str(1)
        say = composeVoice("Do you want to reply to this mail, say reply to reply or continue to proceed",file,i)
        i = i + str(1)
        if say == "reply" or say == 'replay':
            
            # entering content
            msg = composeMessage(file, i)
            print("msg---->")
            print(msg)
            read = composeVoice(
                "Do you want to read it. Say yes to read or no to proceed further", file, i)
            print(read)
            if read == "yes":
                texttospeech(msg, file+i)
                i = i+str(1)
            composeAction = composeVoice(
                "Say delete to discard the draft or rewrite to compose again or send to send the draft", file, i)
            print(composeAction)
            if composeAction == 'delete':
                print("deleting")
                msg = ""
                texttospeech(
                    "Draft has been deleted and you have been redirected to home page", file+i)
                i = i+str(1)
                return JsonResponse({'result': 'readsentsuccess'})
            elif composeAction == 'rewrite':
                print("rewriting")
                return JsonResponse({'result': 'rewrite'})
            elif composeAction == 'send':
                u = User.objects.filter(email=user.email).first()
                replyMail(u.email, u.gpass, k.email, k.subject, msg)
                print("mail sent")
                # texttospeech(
                #     "Mail sent successfully. You are now redirected to home page", file+i)
                # i = i+str(1)
        say = composeVoice("Do you want to forward this mail, say yes to forward or no to proceed",file,i)
        i = i + str(1)
        if say == 'yes':
            emailId = introVoice('email', file, i)
            sendMail(user.email, user.gpass, emailId, k.subject, k.body)
            print("mail sent")
            texttospeech(
                "Mail sent successfully. You are now redirected to home page", file+i)
            i = i+str(1)
            return JsonResponse({'result': 'readsentsuccess'})
        texttospeech(
                "You are now redirected to home page", file+i)
        i = i+str(1)
        return JsonResponse({'result': 'readsentsuccess'})


def read_view(request, id):
    id = int(id)
    user = request.user
    MailList = ReadMails(user.email, user.gpass)
    mail = MailList[id]
    print("Reached read View")
    i = '1'
    file = "test"
    if request.method == 'GET':
        return render(request,'myapp/read.html',{'mail':mail,'mail_id':id})
        

    if request.method == 'POST':
        k = mail
        texttospeech(k.body, file+i)
        i = i + str(1)
        say = composeVoice("Do you want to reply to this mail, say reply to reply or continue to proceed",file,i)
        i = i + str(1)
        if say == "reply" or say == 'replay':
            
            # entering content
            msg = composeMessage(file, i)
            print("msg---->")
            print(msg)
            read = composeVoice(
                "Do you want to read it. Say yes to read or no to proceed further", file, i)
            print(read)
            if read == "yes":
                texttospeech(msg, file+i)
                i = i+str(1)
            composeAction = composeVoice(
                "Say delete to discard the draft or rewrite to compose again or send to send the draft", file, i)
            print(composeAction)
            if composeAction == 'delete':
                print("deleting")
                msg = ""
                texttospeech(
                    "Draft has been deleted and you have been redirected to home page", file+i)
                i = i+str(1)
                return JsonResponse({'result': 'success'})
            elif composeAction == 'rewrite':
                print("rewriting")
                return JsonResponse({'result': 'rewrite'})
            elif composeAction == 'send':
                u = User.objects.filter(email=user.email).first()
                replyMail(u.email, u.gpass, k.email, k.subject, msg)
                print("mail sent")
                # texttospeech(
                #     "Mail sent successfully. You are now redirected to home page", file+i)
                # i = i+str(1)
        say = composeVoice("Do you want to forward this mail, say yes to forward or no to proceed",file,i)
        i = i + str(1)
        if say == 'forward':
            emailId = introVoice('email', file, i)
            sendMail(user.email, user.gpass, emailId, k.subject, k.body)
            print("mail sent")
            texttospeech(
                "Mail sent successfully. You are now redirected to home page", file+i)
            i = i+str(1)
            return JsonResponse({'result': 'success'})
        texttospeech(
                "You are now redirected to home page", file+i)
        i = i+str(1)
        return JsonResponse({'result': 'success'})


# def read_view(request, id):
#     id = int(id)
#     user = request.user
#     MailList = ReadMails(user.email, user.gpass)
#     mail = MailList[id]
#     print("Reached read View")
#     i = '1'
#     file = "test"
#     if request.method == 'GET':
#         return render(request, 'myapp/read.html', {'mail': mail, 'mail_id': id})
#
#     if request.method == 'POST':
#         k = mail
#         texttospeech(k.body, file + i)
#         i = i + str(1)
#         say = composeVoice("Do you want to reply to this mail, say reply to reply or continue to proceed", file, i)
#         i = i + str(1)
#         if say == "reply" or say == 'replay':
#
#             # entering content
#             msg = composeMessage(file, i)
#             print("msg---->")
#             print(msg)
#             read = composeVoice(
#                 "Do you want to read it. Say yes to read or no to proceed further", file, i)
#             print(read)
#             if read == "yes":
#                 texttospeech(msg, file + i)
#                 i = i + str(1)
#             composeAction = composeVoice(
#                 "Say delete to discard the draft or rewrite to compose again or send to send the draft", file, i)
#             print(composeAction)
#             if composeAction == 'delete':
#                 print("deleting")
#                 msg = ""
#                 texttospeech(
#                     "Draft has been deleted and you have been redirected to home page", file + i)
#                 i = i + str(1)
#                 return JsonResponse({'result': 'success'})
#             elif composeAction == 'rewrite':
#                 print("rewriting")
#                 return JsonResponse({'result': 'rewrite'})
#             elif composeAction == 'send':
#                 u = User.objects.filter(email=user.email).first()
#                 replyMail(u.email, u.gpass, k.email, k.subject, msg)
#                 print("mail sent")
#                 # texttospeech(
#                 #     "Mail sent successfully. You are now redirected to home page", file+i)
#                 # i = i+str(1)
#         say = composeVoice("Do you want to forward this mail, say yes to forward or no to proceed", file, i)
#         i = i + str(1)
#         if say == 'forward':
#             emailId = introVoice('email', file, i)
#             sendMail(user.email, user.gpass, emailId, k.subject, k.body)
#             print("mail sent")
#             texttospeech(
#                 "Mail sent successfully. You are now redirected to home page", file + i)
#             i = i + str(1)
#             return JsonResponse({'result': 'success'})
#         texttospeech(
#             "You are now redirected to home page", file + i)
#         i = i + str(1)
#         return JsonResponse({'result': 'success'})


def read_search_view(request, key, id):
    id = int(id)
    user = request.user
    MailList = searchMails(user.email, user.gpass, key)
    mail = MailList[id]
    print("Reached read Search View")
    i = '1'
    file = "test"
    if request.method == 'GET':
        return render(request, 'myapp/readSearch.html', {'mail': mail, 'id': id, 'key':key})

    if request.method == 'POST':
        k = mail
        flag = True
        while flag:
            texttospeech(k.body, file + i)
            i = i + str(1)
            texttospeech("Say yes to listen again or no to continue", file + i)
            say = speechtotext(10)
            i = i + str(1)
            if say == 'yes' or say == 'yes yes':
                print("Reading Trash Mail", id, "again")
                texttospeech("Reading Mail Again", file + i)
                i = i + str(1)
            else:
                flag = False
        return JsonResponse({'result': 'readsearchsuccess', 'key': key})
