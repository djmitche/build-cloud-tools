# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from cfn_pyplates.core import CloudFormationTemplate, Resource
from cfn_pyplates.core import Properties, options
from cfn_pyplates.functions import ref

# VPC

cft = CloudFormationTemplate(description="Release Engineering Web Cluster")

cft.resources.add(Resource(
    'MyStack', 'AWS::OpsWorks::Stack',
    Properties({
        'Name': 'MyStack',
        'VpcId': options['vpcid'],
        'DefaultSubnetId': options['private_subnet'],
        # TODO: replace this with an CF-created role
        'ServiceRoleArn':
            'arn:aws:iam::314336048151:role/aws-opsworks-service-role',
        'DefaultInstanceProfileArn':
            'arn:aws:iam::314336048151:instance-profile/aws-opsworks-ec2-role',
    })
))

cft.resources.add(Resource(
    'MyLayer', 'AWS::OpsWorks::Layer',
    Properties({
        'Name': 'MyLayer',
        'Shortname': 'mylayer',
        'StackId': ref('MyStack'),
        'AutoAssignElasticIps': 'false',
        'AutoAssignPublicIps': 'true',
        'EnableAutoHealing': 'true',
        'Type': 'php-app',
    })
))

cft.resources.add(Resource(
    'MyInstance', 'AWS::OpsWorks::Instance',
    Properties({
        'LayerIds': [ref('MyLayer')],
        'StackId': ref('MyStack'),
        'InstanceType': 'c3.large',
    })
))

cft.resources.add(Resource(
    'MyApp', 'AWS::OpsWorks::App',
    Properties({
        'Name': 'MyApp',
        'AppSource': {
            'Type': 'git',
            'Url': 'git://github.com/amazonwebservices/opsworks-demo-php-simple-app.git',
            'Revision': 'version1',
        },
        'Description': 'Demo App',
        'StackId': ref('MyStack'),
        'Type': 'php',
    })
))
