"""
A file to store jenks command classes
"""


class Status(object):
    """ Return the status of jobs """

    argument = None
    TEMPLATE = "{key}: {host}, {name} (build #{number}) {status}"

    @staticmethod
    def act(job):
        last_build = job.api_instance.get_last_build()
        return Status.TEMPLATE.format(
            key=job.key,
            host=job.host,
            name=job.name,
            number=last_build.get_number(),
            status=last_build.get_status() or "running..."
        )


class Console(object):
    """ return the console output of jobs """

    argument = "--console"

    @staticmethod
    def act(job):
        return job.api_instance.get_last_build().get_console()


class List(object):
    """ list the information about the job without retrieving information online """

    argument = "--list"
    TEMPLATE = "{key} {host} {name}"

    @staticmethod
    def act(job):
        return List.TEMPLATE.format(
            key=job.key,
            host=job.host,
            name=job.name
        )
