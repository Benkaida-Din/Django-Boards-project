from django.shortcuts import render , redirect
from django.contrib.auth.models import User
from .models import Board , Topic , Post
from .forms import NewTopicForm
from django.contrib.auth.decorators import login_required as login_req

def home(request):
    boards = Board.objects.all()
    return render(request,'home.html',{'boards':boards})

def board_topics(request,board_id):
    board = Board.objects.get(id=board_id)
    return render(request,'topics.html',{'board':board})

@login_req
def new_topic(request,board_id):
    board = Board.objects.get(id=board_id)
    form = NewTopicForm()
    user = User.objects.first()
    if request.method == 'POST':
        form = NewTopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.board = board
            topic.created_by = user
            topic.save()
            post = Post.objects.create(message=form.cleaned_data.get('message'), created_by=user, topic=topic)
            return redirect('board_topics', board_id=board.id)
    else:
        form = NewTopicForm()
    return render(request,'new_topic.html',{'board':board,'form':form})

