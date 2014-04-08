"""
A file to store jenks command classes
"""
from jenkinsapi.custom_exceptions import NoBuildData
import webbrowser


class Status(object):
    """ Return the status of jobs """

    argument = None
    TEMPLATE = "{key}: {host}, {name} (last build #{number}) {status}"

    @staticmethod
    def act(job):
        try:
            last_build = job.api_instance().get_last_build()

            if job.api_instance().is_queued():
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
        except NoBuildData:
            return Status.TEMPLATE.format(
                key=job.key,
                host=job.host,
                name=job.name,
                number=0,
                status="Hasn't run yet"
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


class Browser(object):
    """ open the job's page in a browser """
    argument = "--browser"

    @staticmethod
    def act(job):
        webbrowser.open(job.api_instance().baseurl)
        return ""
