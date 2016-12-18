import logging
import re
import subprocess

logger = logging.getLogger(__name__)


class SemanticVersioning(object):
    """handles semantic versioning

    version = SemanticVersioning()
    version.current()  -> v1.0.1  # fetches tags and shows most recent
    v = version.next_version()  -> v1.1.0  # increments minor version by default
    version.tag(v)  # creates an annotated tag and pushes it to the remote
    """
    prefix = 'v'

    def __init__(self, prefix=None):
        if prefix:
            self.prefix = prefix

    def is_match(self, tag):
        pattern = r'^{}(\d+\.)?(\d+\.)?(\*|\d+)$'.format(self.prefix)
        return re.match(pattern, tag)

    def fetch_tags(self):
        self._check_output("git fetch --tags")

    def get_tags(self):
        """return tags with most recent first"""
        output = self._check_output("git for-each-ref --sort=-taggerdate --format %(tag) refs/tags")
        return output.split('\n')

    def current(self):
        self.fetch_tags()
        for tag in self.get_tags():
            if self.is_match(tag):
                return tag

        # valid tagged version not found so create one
        version = None
        while not version:
            version = raw_input('Please enter a starting version.  Should be of format {}1.0.0: '.format(self.prefix))
            if not self.is_match(version):
                version = None

        self.tag(version)
        return version

    def rollback(self):
        latest_tag = self.current()
        self._check_output('git tag --delete {}'.format(latest_tag))
        self._check_output('git push origin :{}'.format(latest_tag))

    def next_version(self, release_type='minor'):
        major, minor, patch = self.current().replace(self.prefix, '').split('.')
        if release_type == 'major':
            major = int(major) + 1
            minor, patch = 0, 0
        elif release_type == 'minor':
            minor = int(minor) + 1
            patch = 0
        elif release_type == 'patch':
            patch = int(patch) + 1
        else:
            raise AttributeError('release {} arg not recognised'.format(release_type))

        return '{}{}.{}.{}'.format(self.prefix, major, minor, patch)

    def tag(self, version, push=False):
        self._check_output('git tag -a {0} -m "{0}"'.format(version))
        if push:
            self._check_output('git push --tags')

    def _check_output(self, command):
        """utility function to execute and log shell commands"""
        try:
            logger.info(command)
            output = subprocess.check_output(command.split(' '))
            logger.info(output)
            return output
        except subprocess.CalledProcessError as e:
            logger.error(e)
