import argparse
import boto
import sys
import random
import os


def get_filters(args):
    """ Return a dict of filters based on the given arguments """
    filters = {}

    if args.tag:
        for t in args.tag:
            k, v = t.split('=') # TODO error checking
            filters['tag:%s' % k] = v

    if args.has_tag_key:
        for k in args.has_tag_key:
            filters['tag-key'] = k

    if args.has_tag_value:
        for v in args.has_tag_value:
            filters['tag-value'] = v

    if args.availability_zone:
        filters['availability_zone'] = args.availability_zone

    if args.image_id:
        filters['image-id'] = args.image_id

    if args.instance_id:
        filters['instance-id'] = args.instance_id

    if args.instance_type:
        filters['instance-type'] = args.instance_type

    if args.security_group:
        filters['instance.group-name'] = args.security_group

    if args.key_name:
        filters['key-name'] = args.key_name

    if args.subnet_id:
        filters['subnet-id'] = args.subnet_id

    if args.vpc_id:
        filters['vpc-id'] = args.vpc_id

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
    # Retrieve a list of instances that match the filters
    conn = boto.connect_ec2()
    instances = conn.get_only_instances(filters=get_filters(args))
    if len(instances) == 0:
        print 'No instances matching criteria'
        sys.exit(1)

    instance_dns_names = []
    if args.all_matching_instances:
        for instance in instances:
            instance_dns_names.append(instance.public_dns_name)
    else:
        # Pick a random instance from the results
        instance = instances[random.randrange(0, len(instances))]
        instance_dns_names.append(instance.public_dns_name)

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
