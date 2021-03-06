from django.shortcuts import get_object_or_404, redirect
from common.views import TemplateView, get_user
from courses.models import Course


class ViewCourseView(TemplateView):
    template_name = 'courses/view.html'
    valid_users = (1,)

    def get(self, request, *args, **kwargs):
        user = get_user(self)
        id = int(args[0])
        self.course = get_object_or_404(Course, id=id)
        self.permission = self.course.students.filter(id=user.id).first() or self.course.teacher == user
        if user is None:
            return redirect('index')
        return super().get(request, *args, **kwargs)

    def custom_context_data(self):
        return {'course': self.course, 'scoreboard': self.permission}
