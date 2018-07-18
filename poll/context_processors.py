from poll.models import Question

def polls_count(request):
    c = Question.objects.count()
    return {"count": c}