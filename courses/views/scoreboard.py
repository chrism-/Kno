from django.shortcuts import redirect
from courses.views import ViewCourseView
from tasks.modeldir.base import Submission


class ScoreboardView(ViewCourseView):
    template_name = 'courses/scoreboard.html'
    valid_users = (1,)

    def get(self, request, *args, **kwargs):
        result = super().get(request, *args, **kwargs)
        if not self.permission:
            return redirect('index')
        return result

    def custom_context_data(self):
        mode = self.request.GET.get('mode', 'weighted')
        students = self.course.students.all()
        tasks = self.course.task_set.all().exclude(kind='read').order_by('id')
        totalweight = sum(x.weight for x in tasks)
        marks = {}
        for student in students:
            marks[student] = []
            total = 0
            for task in tasks:
                total += task.marks if mode == 'raw' else task.weight
                submission = task.get_submissions(student).first()
                if task.kind == 'assign':
                    mark = 0 if submission is None else submission.mark
                marks[student].append(mark if mode == 'raw' else (mark / task.marks * task.weight
                / totalweight))
            if total == 0: total -= 1
            marks[student].append(sum(marks[student]) if mode == 'raw' else sum(marks[student]) / total)
        return {
            'course': self.course,
            'tasks': tasks,
            'students': students,
            'marks': marks,
            'mode': mode,
            'totalweight': totalweight,
            'totalmarks': max(total, 0),
        }
