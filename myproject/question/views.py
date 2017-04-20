from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

from django.http import HttpResponse,HttpResponseForbidden
from .decorators import ajax_required
from activities.models import Activity
from .models import Question, Answer, Tag
from .forms import QuestionForm, AnswerForm


def _question(request, question, active):
	paginator = Paginator(question, 10)
	page = request.GET.get('page')
	try:
		question = paginator.page(page)
	except PageNotAnInteger:
		question = paginator.page(1)
	except EmptyPage:
		question = paginator.page(paginator.num_pages)
		return render(request, 'questions/question.html', {'question': question,'active': active})


def askQuestion(request):
	if request.method=="POST":
		form = QuestionForm(request.POST)
		if form.is_valid():
			question= Question()
			question.user =  request.user
			question.title = form.cleaned_data.get('title')
			question.description = form.cleaned_data.get('description')
			question.save()
			tags = form.cleaned_data.get('tag')
			question.create_tags(tags)
			return redirect('/questions/ask.html')

	else:
		form = QuestionForm()
	return render(request, 'questions/ask.html', {'form': form})

def question(request,pk):
	question = get_object_or_404(Question, pk=pk)

	form = AnswerForm(initial={'question': question})
	return render(request, 'questions/question.html', {'question': question,'form': form})



def writeAnswer(request):
	if request.method=="POST":
		form=AnswerForm(request.POST)
		if form.is_valid():
			answer=Answer()
			answer.user=request.user
			answer.question=form.cleaned_data.get('question')
			answer.description=form.cleaned_data.get('description')
			answer.save()
			return redirect('/question/{0}/'.format(answer.question.pk))
		else:
			question = form.cleaned_data.get('question')
		return render(request, 'questions/question.html', {
			'question': question,
			'form': form
			})
	else:
		return redirect('/question/')

@ajax_required
def answerAccept(request):
	answer_id = request.POST['answer']
	answer = Answer.objects.get(pk=answer_id)
	user=request.user

	if answer.question==user:
		answer.accept()
		return HttpResponse()
	else:
		return HttpResponseForbidden()


@ajax_required
def favorite(request):
	question_id = request.POST['question']
	question = Question.objects.get(pk=question_id)
	user = request.user
	activity = Activity.objects.filter(activity_type=Activity.FAVORITE,user=user, question=question_id)
	if activity:
		activity.delete()
	else:
		activity = Activity(activity_type=Activity.FAVORITE, user=user,question=question_id)
		activity.save()
	return HttpResponse(question.calculate_favorites())


@ajax_required
def vote(request):
	answer_id = request.POST['answer']
	answer = Answer.objects.get(pk=answer_id)
	vote = request.POST['vote']
	user = request.user
	activity = Activity.objects.filter(Q(activity_type=Activity.UP_VOTE) | Q(activity_type=Activity.DOWN_VOTE),   # noqa: E501
		user=user, answer=answer_id)
	if activity:
		activity.delete()
	if vote in [Activity.UP_VOTE, Activity.DOWN_VOTE]:
		activity = Activity(activity_type=vote, user=user, answer=answer_id)
		activity.save()
	return HttpResponse(answer.calculate_votes())