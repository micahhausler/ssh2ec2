# ssh2ec2

A little helper script to simplify connecting to an EC2 instance via SSH.

Specify some tags and metadata to filter your instances, and you'll be connected to an instance in the matching set.

See the [blog post](http://awssystemadministration.com/ssh2ec2-connect-to-instances-using-tags-and-metadata-instead-of-hostnames/) for more details.

## Usage Examples

Open an SSH connection to a random instance that matches the given filters:

    ssh2ec2 --tag Name=nginx

    ssh2ec2 --tag role=web --tag environment=production

    ssh2ec2 --availability-zone us-east-1a --instance-type t2.micro

    ssh2ec2 --tag role=web --ssh-user ubuntu

Pass commands to SSH for execution on the remote host:

    ssh2ec2 --tag role=web uname -a

SSH arguments can be specified by including them in a quoted string at the end of the command,
or explicitly specified with --ssh-args. The following commands are functionally identical:

    ssh2ec2 --tag role=web "-i /path/to/key echo hello"
    ssh2ec2 --tag role=web --ssh-args "-i /path/to/key" echo hello

Execute the same command on all instances matching the filters:

    ssh2ec2 --all-matching-instances --tag role=web hostname

## Installation and Configuration

    pip install ssh2ec2

This script does not require any specific configuration. However, it does assume that your AWS
credentials and default region are available in a config file or environment variables. See the
[AWS documentation](http://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html#config-settings-and-precedence) for more details.

If you have multiple sets of credentials in your `~/.aws/credentials` file you can select which one will be
used with the --profile argument:

    ssh2ec2 --profile profile_name ...

Multi-Factor Authentication devices are supported, but you must use the `mfa_serial` directive in your `~/.aws/credentials`:

    $ ssh2ec2 --profile prod --tag role=web
    Enter MFA code:


## Supported Filters

|Name               | Description       |
|---                |---                |
|availability-zone  | The Availability Zone of the instance. |
|image-id|			The ID of the image used to launch the instance.|
|instance-id|			The ID of the instance.|
|instance-type|			The type of instance (for example, t2.micro).|
|instance.group-name|			The name of the security group for the instance.|
|key-name|			The name of the key pair used when the instance was launched.|
|subnet-id|			The ID of the subnet for the instance.|
|tag:key=value|			The key/value combination of a tag assigned to the resource, where tag:key is the tag's key.|
|tag-key|			The key of a tag assigned to the resource. This filter is independent of the tag-value filter. For example, if you use both the filter "tag-key=Purpose" and the filter "tag-value=X", you get any resources assigned both the tag key Purpose (regardless of what the tag's value is), and the tag value X (regardless of what the tag's key is). If you want to list only resources where Purpose is X, see the tag:key=value filter.|
|tag-value|			The value of a tag assigned to the resource. This filter is independent of the tag-key filter.|
|tenancy|			The tenancy of an instance (dedicated, default, host).|
|vpc-id|			The ID of the VPC that the instance is running in.|



