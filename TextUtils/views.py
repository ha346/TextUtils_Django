from django.shortcuts import render 
from Text_Utils.models import Contact
from django.contrib import messages   


def index(request):
    return render(request, 'Index.html',{"strongtext":"Welcome to TextUtils!","text":"You can do anything with your text here!.","tag":"success"})


def analyzer(request):
    #Get the text
    djtext = request.POST.get('text', 'default')

    # Check checkbox values
    removepunc = request.POST.get('removepunc', 'off')
    fullcaps = request.POST.get('fullcaps', 'off')
    newlineremover = request.POST.get('newlineremover', 'off')
    extraspaceremover = request.POST.get('extraspaceremover', 'off')
    numberremover = request.POST.get('numberremover','off')

    #Check which checkbox is on
    if removepunc == "on":
        punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
        analyzed = ""
        for char in djtext:
            if char not in punctuations:
                analyzed = analyzed + char

        params = {'purpose':'Removed Punctuations', 'analyzed_text': analyzed}
        djtext = analyzed

    if(fullcaps=="on"):
        analyzed = ""
        for char in djtext:
            analyzed = analyzed + char.upper()

        params = {'purpose': 'Changed to Uppercase', 'analyzed_text': analyzed}
        djtext = analyzed

    if(extraspaceremover=="on"):
        analyzed = ""
        for index, char in enumerate(djtext):
            if not(djtext[index] == " " and djtext[index+1]==" "):                        
                analyzed = analyzed + char

        params = {'purpose': 'Removed NewLines', 'analyzed_text': analyzed}
        djtext = analyzed

    if (newlineremover == "on"):
        analyzed = ""
        for char in djtext: 
            if char != "\n" and char!="\r":
                analyzed = analyzed + char

        params = {'purpose': 'Removed NewLines', 'analyzed_text': analyzed}
        djtext = analyzed
    
    if (numberremover == "on"):
        analyzed = ""
        numbers = '0123456789'

        for char in djtext:
            if char not in numbers:
                analyzed = analyzed + char
        
        params = {'purpose': 'Removed NewLines', 'analyzed_text': analyzed}
        djtext = analyzed

    
    if(removepunc != "on" and newlineremover!="on" and extraspaceremover!="on" and fullcaps!="on" and numberremover != "on"):
        # return HttpResponse("please select any operation and try again")
        return render(request,"Index.html",{"strongtext":"","text":"Please select any operation and try again!","tag":"danger"})

    return render(request, 'Analyzer.html', params)

def about(request):
    return render(request, 'About.html')

def contact(request):
    return render(request, 'Contact.html')

def submitContact(request):
    if request.method=="POST": 
        name=request.POST['username']
        email=request.POST['email']
        phone=request.POST['phone']
        content =request.POST['content']
        if len(name)<2 or len(email)<3 or len(phone)<10: 
            return render(request, "Contact.html",{"strongtext":"","text":"Please fill your name must contain 2 characters or your email must consist 3 characters or your mobile no. must contain 10 digits","tag":"danger"})
        else:
            contact=Contact(name=name, email=email, phone=phone, content=content)
            contact.save() 
            message=True
            return render(request, "Contact.html",{"strongtext":"Success! ","text":"Your Contact has been saved","tag":"success"})
    return render(request, "Contact.html")