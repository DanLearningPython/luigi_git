import luigi
import os
import git
import time


class PrintDateTask(luigi.Task):
    path = luigi.Parameter()
    current_date = time.strftime("%A, %B %d %Y")

    def run(self):
        with open(self.path, 'w') as out_file:
            out_file.write(self.current_date)
            out_file.close()

    def output(self):
        return luigi.LocalTarget(self.path)

    def requires(self):

        return [
            MakeDirectory(path=os.path.dirname(self.path)),
        ]


class PrintTimeTask(luigi.Task):
    path = luigi.Parameter()
    current_time = time.strftime("%I:%M:%S%p %Z")

    def run(self):
        with open(self.path, 'w') as out_file:
            out_file.write(self.current_time)
            out_file.close()

    def output(self):
        return luigi.LocalTarget(self.path)

    def requires(self):

        return [
            MakeDirectory(path=os.path.dirname(self.path)),
        ]


class CreateDateTimeFilesTask(luigi.Task):
    id = luigi.Parameter(default=0)

    def run(self):
        with open(self.input()[0].path, 'r') as date_file:
            current_date = date_file.read()
        with open(self.input()[1].path, 'r') as time_file:
            current_time = time_file.read()
        with open(self.output().path, 'w') as output_file:
            content = 'It is now: {} {}'.format(current_date, current_time)
            output_file.write(content)
            output_file.close()

    def requires(self):
        return [
            PrintDateTask(
                path='results/{}/date.txt'.format(self.id)
            ),
            PrintTimeTask(
                path='results/{}/time.txt'.format(self.id)
            ),
        ]

    def output(self):
        path = 'results/{}/datetime.txt'.format(self.id)
        return luigi.LocalTarget(path)


class DateTimeTask(luigi.Task):
    id = luigi.Parameter(default=0)

    def run(self):

        # push new date file to git
        self.push_to_git()

        date_path = 'results/{}/date.txt'.format(self.id)
        time_path = 'results/{}/time.txt'.format(self.id)
        datetime_path = 'results/{}/datetime.txt'.format(self.id)

        # cleanup
        os.remove(date_path)
        os.remove(time_path)
        os.remove(datetime_path)

    def requires(self):
        return [
            CreateDateTimeFilesTask(
                id=self.id
            )
        ]

    def push_to_git(self):

        current_datetime = time.strftime("%c")

        repo = git.Repo('.')
        repo.git.add('.')
        repo.git.commit(m='Auto create and commit files {}'.format(current_datetime))
        repo.git.push()
        repo.git.status()


class MakeDirectory(luigi.Task):
    path = luigi.Parameter()

    def output(self):
        return luigi.LocalTarget(self.path)

    def run(self):
        os.makedirs(self.path)


if __name__ == '__main__':
    luigi.run()
