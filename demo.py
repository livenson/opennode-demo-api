#!/usr/bin/env python

import web
import json
import string
import random

urls = (
    '/computes', 'ComputeList',
    '/computes/(\d+)', 'Compute',
    '/networks', 'NetworkList',
    '/networks/(\d+)', 'Network',
    '/storages', 'StorageList',
    '/storages/(\d+)', 'Storage',
    '/templates', 'TemplateList',
    '/templates/(\d+)', 'Template',
    '/news', 'NewsList',
    '/news/(\d+)', 'News'
)
app = web.application(urls, globals())

def gen_compute_data(id):
    return {'id': id,
            'hostname': 'hostname %s' %id, 
            'arch': ['x86', 'x64', 'win32', 'win64', 'macosx'][id % 5], 
            'memory': 2*id,
            'cpu': 0.2 * id,
            'cores': range(1,16)[id % 15],
            'template': ['centos5', 'centos6', 'rhel6-jbos', 'winserver2008', 'jetty-cluster'][id % 5],
            'state': ['running', 'stopped', 'suspended'][id % 3]}

def gen_network_data(id):
    return {'id': id,
            'name': 'network %s' %id, 
            'ip': '%s.%s.%s.%s' %(id, id, id, id),
            'mask': '%s.%s.%s.0' %(id * 2, id * 2, id * 2),
            'address_allocation': ['dhcp', 'static'][id % 2], 
            'gateway': '%s.%s.%s.1' %(id * 2, id * 2, id * 2)
           }

def gen_storage_data(id):
    return {'id': id,
            'name': 'network %s' %id, 
            'size': id * 3000,
            'type': ['local', 'iscsi', 'lvm', 'nfs'][id % 4]
            }

def gen_template_data(id):
    return {'id': id,
            'name': 'network %s' %id, 
            'min_disk_size': id * 3000,
            'min_memory_size': id * 300
            }

def gen_news_data(id):
    def get_string(length):
        return ''.join(random.choice(string.letters) for i in xrange(length))
    return {'id': id,
            'type': ['info', 'warning', 'error', 'system_message'][id % 4],
            'title': get_string(20),
            'content': get_string(400)
            }

limit = 20

computes = [gen_compute_data(i) for i in range(limit)]
storages = [gen_storage_data(i) for i in range(limit)]
networks = [gen_network_data(i) for i in range(limit)]
templates = [gen_network_data(i) for i in range(limit)]
news = [gen_network_data(i) for i in range(limit)]

class ComputeList(object):
    def GET(self):
        return json.dumps([c['hostname'] for c in computes])

class Compute(object):
    def GET(self, id):
        id = int(id)
        return json.dumps(computes[id], sort_keys = 4, indent = 4)

class NetworkList(object):
    def GET(self):
        return json.dumps([n['name'] for n in networks])

class Network(object):
    def GET(self, id):
        id = int(id)
        return json.dumps(networks(id), sort_keys = 4, indent = 4)

class StorageList(object):
    def GET(self):
        return json.dumps([s['name'] for s in storages])

class Storage(object):
    def GET(self, id):
        id = int(id)
        return json.dumps(storages(id), sort_keys = 4, indent = 4)

class TemplateList(object):
    def GET(self):
        return json.dumps([t['name'] for t in templates])

class Template(object):
    def GET(self, id):
        id = int(id)
        return json.dumps(templates(id), sort_keys = 4, indent = 4)

class NewsList(object):
    def GET(self):
        return json.dumps([n['title'] for n in news])

class News(object):
    def GET(self, id):
        id = int(id)
        return json.dumps(news(id), sort_keys = 4, indent = 4)


if __name__ == "__main__":
    app.run()
