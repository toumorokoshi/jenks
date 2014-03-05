"""
A file to store jenks command classes
"""
import requests


class Status(object):
    """ Return the status of jobs """

    argument = None
    TEMPLATE = "{key}: {host}, {name} (last build #{number}) {status}"

    @staticmethod
    def act(job):
        last_build = job.api_instance.get_last_build()

        if job.api_instance.is_queued():
            status = "queued"
        else:
            status = last_build.get_status() or "running..."

        return Status.TEMPLATE.format(
            key=job.key,
            host=job.host,
            name=job.name,
            number=last_build.get_number(),
            status=status
        )


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


class Trigger(object):
    """" trigger jobs """

    argument = "--trigger"

    @staticmethod
    def act(job):
        if job.api_instance.is_running():
            return "{0}, {1} is already running".format(job.host, job.name)
        else:
            requests.get(job.api_instance.get_build_triggerurl())
            return "triggering {0}, {1}...".format(job.host, job.name)
