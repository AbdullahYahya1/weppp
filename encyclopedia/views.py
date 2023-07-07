from django.shortcuts import render , redirect
#import reverse
from django.urls import reverse

from . import util
from django import forms
def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
    })

def wiki(request , name):

    if request.method == "POST":
        html = util.get_html(name)
        return render(request, "encyclopedia/edit.html", {"html": util.get_orginal(html) , 'title':name  ,'edit':True })

    html = util.get_html(name)
    return render(request, "encyclopedia/wiki.html", {"html": html , 'title':name ,  })

def search(request):

    if request.method == "POST":
        post = request.POST
        # check if post is valid
        if not post.get("q") :
            return render(request, "encyclopedia/search.html", {
                "error": "Please enter a word to search",   
            })
        #get post
        post = request.POST
        word_to_search = (post.get("q"))
        html = util.get_html(word_to_search)
        if(html):
            return render(request ,'encyclopedia/search.html' ,{
                'html':html , 'title':word_to_search })
        list = util.get_list_Similler(word_to_search)
        if(list):
            return render(request,'encyclopedia/search.html',{
                'entries':list , })
            
        return render(request, "encyclopedia/search.html",{
            "error2": "No results found for " + word_to_search,
            })
    else:
        return redirect("index")
    


class new_pageForm(forms.Form):
    title = forms.CharField(max_length=100)
    content = forms.CharField(widget=forms.Textarea)

def new_page(request):
    if(request.method == "POST"):
        form = new_pageForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']
            if util.get_entry(title):
                return render(request , 'encyclopedia/new_page.html' , {'error':"page already exists", } ,)
            util.save_entry(title, content)
            return redirect(reverse('wiki', args=[title]))
        return render(request , 'encyclopedia/new_page.html' , {'form': new_pageForm, })

    return render(request , 'encyclopedia/new_page.html' , {'form': new_pageForm,})

def edit(request):
    if(request.method == "POST"):
        print('here')
        html = request.POST['html']
        name = request.POST['title']
        util.save_entry(name, html)
        return redirect("wiki", name)
def rand(request):
    random = util.random_entrie()
    print(random)
    return redirect("wiki", random)