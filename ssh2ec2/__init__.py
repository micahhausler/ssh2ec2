import argparse
import boto3
from botocore.exceptions import ProfileNotFound
import sys
import random
import os


def get_filters(args):
    """ Return a dict of filters based on the given arguments """
    filters = [
        {
            'Name': 'instance-state-name',
            'Values': ['running']
        }
    ]

    if args.tag:
        for t in args.tag:
            k, v = t.split('=')  # TODO error checking
            filters.append({
                'Name': 'tag:{}'.format(k),
                'Values': [v]
            })

    if args.has_tag_key:
        for k in args.has_tag_key:
            filters.append({
                'Name': 'tag-key',
                'Values': [k]
            })

    if args.has_tag_value:
        for v in args.has_tag_value:
            filters.append({
                'Name': 'tag-value',
                'Values': [v]
            })

    if args.availability_zone:
        filters.append({
            'Name': 'availability-zone',
            'Values': [args.availability_zone]
        })

    if args.image_id:
        filters.append({
            'Name': 'image-id',
            'Values': [args.image_id]
        })

    if args.instance_id:
        filters.append({
            'Name': 'instance-id',
            'Values': [args.instance_id]
        })

    if args.instance_type:
        filters.append({
            'Name': 'instance-type',
            'Values': [args.instance_type]
        })

    if args.security_group:
        filters.append({
            'Name': 'instance.group-name',
            'Values': [args.security_group]
        })

    if args.key_name:
        filters.append({
            'Name': 'key-name',
            'Values': [args.key_name]
        })

    if args.subnet_id:
        filters.append({
            'Name': 'subnet-id',
            'Values': [args.subnet_id]
        })

    if args.vpc_id:
        filters.append({
            'Name': 'vpc-id',
            'Values': [args.vpc_id]
        })

    return filters


def parse_args():

    parser = argparse.ArgumentParser()
    # EC2 filters
    parser.add_argument('--tag', action='append',
                        help='key=value')
    parser.add_argument('--has-tag-key', action='append',
                        help='Instance must have this tag key (value is not checked)')
    parser.add_argument('--has-tag-value', action='append',
                        help='Instance must have this tag value (key is not checked)')
    parser.add_argument('-a', '--availability-zone', dest='availability_zone')
    parser.add_argument('--image-id')
    parser.add_argument('--instance-id')
    parser.add_argument('--instance-type')
    parser.add_argument('--security-group', help='The name of the security group for the instance')
    parser.add_argument('--key-name')
    parser.add_argument('--subnet-id')
    parser.add_argument('--vpc-id')
    # AWS connection args
    parser.add_argument('--profile',
                        help='The name of a profile configured in the AWS credentials file')
    parser.add_argument('--region',
                        help='The name of the AWS region')
    # SSH args
    parser.add_argument('--ssh-user', help='Username to use for SSH connection')
    parser.add_argument('--ssh-args', default='', help='Additional arguments for SSH')
    parser.add_argument('--all-matching-instances', action='store_const', const=True,
                        help='Connect to or run command on all instances, instead of single random instance')
    # Any additional args are passed directly to SSH
    parser.add_argument('command', nargs=argparse.REMAINDER, help='Optional command to execute via SSH')

    return parser.parse_args()


def main():

    args = parse_args()

    try:
        boto3.setup_default_session(profile_name=args.profile, region_name=args.region)
        conn = boto3.client('ec2')
    except ProfileNotFound as e:
        print(e)
        sys.exit(1)

    # Retrieve a list of instances that match the filters
    reservations = conn.describe_instances(Filters=get_filters(args))
    if len(reservations['Reservations']) == 0:
        print('No instances matching criteria')
        sys.exit(1)

    instance_dns_names = [[
        instance['PublicDnsName'] for instance in reservation['Instances']][0]
        for reservation
        in reservations['Reservations']]
    if args.all_matching_instances:
        pass
    else:
        # Pick a random instance from the results
        instance_dns_names = [instance_dns_names[random.randrange(0, len(instance_dns_names))]]

    if args.command:
        remote_command = ' '.join(args.command)
    else:
        remote_command = ''

    for dns_name in instance_dns_names:
        if args.ssh_user:
            dns_name = '%s@%s' % (args.ssh_user, dns_name)

        ssh_cmd = 'ssh %s %s %s' % (args.ssh_args, dns_name, remote_command)
        os.system(ssh_cmd)


if __name__ == '__main__':
    main()
