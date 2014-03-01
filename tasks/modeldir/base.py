from auth.models import User
from common import models
from courses.models import Course


# https://docs.djangoproject.com/en/1.6/topics/db/models/#multi-table-inheritance
# Task.objects.* can access subclasses of task as well as task
class Task(models.Model):
    class Meta:
        app_label = 'tasks'

    name = models.CharField(max_length=100)
    desc = models.CharField(max_length=10000)
    course = models.ForeignKey(Course)

    @classmethod
    def create(cls, *args, **kwargs):
        task = Task(*args, **kwargs)
        task.save()

        from misc.models import Search  # bidirectional import
        Search.add_words(kwargs['name'], task.id, Task)
        return task

    def __repr__(self):
        return self.name


class Submission(models.Model):
    class Meta:
        app_label = 'tasks'

    user = models.ForeignKey(User)
    marks = models.IntegerField()  # TODO: make this a seperate table for certain task types
    task = models.ForeignKey(Task)
