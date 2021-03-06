from django_jinja import library
import importlib

lib = library.Library()

form_names = {
    'auth': {
        'Register',
        'Login',
        'ResetPwd',
        'ForgotPwd',
        'DoResetPwd',
    },
    'courses': {
        'CreateCourse',
        'JoinCourse',
    },
    'tasks': {
        'CreateTask',
        'EditTaskDesc',
        'AddIOFile',
        'DeleteIOFile',
        'Submit'
    }
}

forms = {}

for modulename in form_names:
    module = importlib.import_module(modulename + '.forms')
    for cls in form_names[modulename]:
        cls = getattr(module, cls + 'Form')
        forms[cls.cls_name()] = cls

@lib.global_function
def as_form(name, info, *args, **kwargs):
    return forms[name](view=info[0], user=info[1]).as_form(*args, **kwargs)

@lib.global_function
def as_modal(name, info, *args, **kwargs):
        return forms[name](view=info[0], user=info[1]).as_modal(*args, **kwargs)

@lib.global_function
def string(s):
    return str(s)

@lib.global_function
def percent(n):
    return str(int(n * 100)) + '%'

@lib.global_function
def integer(n):
    return int(n)

@lib.global_function
def table_width(i):
    return (3, 4, 3)[i]

@lib.global_function
def func(fn, *args, **kwargs):
    return eval(fn)(*args, **kwargs)
