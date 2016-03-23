# Copyright 2015 Jared Rodriguez (jared at blacknode dot net)
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

from setuptools import setup

setup(
    name='mercury-agent',
    version='0.0.1',
    packages=['mercury'],
    url='https://www.rackspace.com',
    license='',
    author='Jared Rodriguez',
    author_email='jared.rodriguez@rackspace.com',
    description='',
    install_requires=[
        'pyzmq',
        'msgpack-python',
        'netifaces',
        'pexpect',
        'pyudev'
    ],
    entry_points="""
    [console_scripts]
    mercury_agent = mercury.agent.agent:main
    """,
)