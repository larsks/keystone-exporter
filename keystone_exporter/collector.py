import logging
import re

from prometheus_client.core import GaugeMetricFamily

LOG = logging.getLogger(__name__)
re_invalid_chars = re.compile(r'[^\w]+')


class KeystoneCollector(object):
    def __init__(self, cloud):
        self.cloud = cloud

    def get_domains(self):
        LOG.info('start collecting keystone domains')
        m = GaugeMetricFamily('keystone_domain',
                              'Information about a keystone domain',
                              labels=['os_domain_uuid', 'os_domain_name'])

        for dom in self.cloud.list_domains():
            m.add_metric([dom.id, dom.name], 1.0)

        LOG.info('done collecting keystone domains')
        yield m

    def get_projects(self):
        LOG.info('start collecting keystone projects')
        m = GaugeMetricFamily('keystone_project',
                              'Information about a keystone project',
                              labels=['os_project_uuid', 'os_project_name'])

        for proj in self.cloud.list_projects():
            m.add_metric([proj.id, proj.name], 1.0)

        LOG.info('done collecting keystone projects')
        yield m

    def get_users(self):
        LOG.info('start collecting keystone users')
        m = GaugeMetricFamily('keystone_user',
                              'Information about a keystone user',
                              labels=['os_user_uuid', 'os_user_name',
                                      'os_user_email'])

        for user in self.cloud.list_users():
            m.add_metric([user.id, user.name,
                          user.email if user.email else ''], 1.0)

        LOG.info('done collecting keystone users')
        yield m

    def describe(self):
        return []

    def collect(self):
        LOG.info('start collecting keystone information')
        yield from self.get_domains()
        yield from self.get_projects()
        yield from self.get_users()
        LOG.info('done collecting keystone information')
