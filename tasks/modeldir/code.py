from shutil import copyfile
import tempfile
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from common import models
from common.functions import makepath
from tasks.modeldir.programming import Environment
from tasks.models import Task, Submission
import os

class CodeTask(Task):
    class Meta:
        app_label = 'tasks'

    @classmethod
    def create(cls, *args, **kwargs):
        val = super().create(*args, **kwargs)
        os.mkdir(val.get_path())
        return val

    def get_path(self, name=''):
        return makepath('codeio/{}/{}'.format(self.id, name))

    def get_io_files(self):
        files = os.listdir(self.get_path())
        return sorted(set(['.'.join(f.split('.')[:-1]) for f in files]))

    def has_io_files(self, name):
        return os.path.isfile(self.get_path(name + '.in'))

    def add_io_files(self, name, infile, outfile):
        path = self.get_path(name)
        default_storage.save(path + '.in', ContentFile(infile.read()))
        default_storage.save(path + '.out', ContentFile(outfile.read()))

    def delete_io_files(self, name):
        path = self.get_path(name)
        default_storage.delete(path + '.in')
        default_storage.delete(path + '.out')

SCORES = enumerate([
    'Doesn\'t look right to me...',
    'Your answer looks right, but some letters aren\'t capitalised correctly.',
    'Getting there, but check that the punctuation is correct.',
    'Almost there, but check the whitespace (newlines, spaces, tabs)',
    'That looks good to me!'
])

class CodeSubmission(Submission):
    class Meta:
        app_label = 'tasks'

    comment = models.IntegerField(choices=SCORES)
    error = models.CharField(blank=True, null=True, max_length=50)  # error type
    order = models.IntegerField()  # for code tasks, we can have multiple submissions

    def on_submit(self, bonus):
        # here we execute their code
        self.comment = 0
        self.order = 0
        self.error = None
        # env = Environment()
        # print(env.add_file('main.py', bonus['data'].read()))
        # print(env.run_simple([], ))
        directory = tempfile.mkdtemp()
        os.chmod(directory, 0o755)
        code = os.path.join(directory, 'main.py')
        f = open(code, 'wb')
        f.write(self.data.read())
        f.close()
        for io in self.task.codetask.get_io_files():
            fin = open(os.path.join(directory, 'infile'), 'w')
            infile = open(makepath('codeio/{}/{}.in'.format(self.task.id, io))).read()
            fin.write(infile)
            fin.close()
            outfile = open(makepath('codeio/{}/{}.out'.format(self.task.id, io))).read()
            print(os.popen('python3 {0}/main.py < {0}/infile'.format(directory)))


        return 'submitted a code task'