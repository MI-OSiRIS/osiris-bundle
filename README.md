# osiris-bundle
OSiRIS client bundle for s3fs mounting

## Description

This bundle is designed to simplify configuration and usage of s3fuse to mount OSiRIS S3 buckets.  It is targeted both at interactive and non-interactive use in batch jobs.  

It includes an endpoint auto-detection component to determine which OSiRIS S3 endpoint is reachable by your host.  For example, from campus computing clusters at our member institutions you will generally only be able to reach the endpoint local to your campus.  From more general purpose machines you may be able to reach all of the OSiRIS S3 endpoints.  

A setup tool is also included to configure your S3 credentials.  

The default behaviour is to list all of your S3 buckets and mount each one under /tmp/${USER}-fuse/bucketname.  You can also specify buckets to mount and create them if necessary.  

## Usage

Usage of the client bundle for batch compute jobs assumes you have a consistent $HOME directory and can run the configure script first on a login interactive node.  Once the configuration script is run the osiris-mount utility does not require interaction to mount your buckets.  You can run the configuration script multiple times to change or add new credentials.  The credentials used are determined by the AWSPROFILE setting in osiris-bundle/osiris-config.  This setting can also be specified with the -p option to osiris-mount.  

### Example:

Download the bundle:

    curl -L --output osiris-bundle.tgz \
    https://github.com/MI-OSiRIS/osiris-bundle/releases/latest/download/osiris-bundle.tgz

Untar into your home directory:

    cd ~ && tar -xvzf osiris-bundle.tgz

Run the setup tool:

    ~/osiris-bundle/osiris-setup.dist

You will be prompted for your OSiRIS Virtual Organization (aka COU), an S3 userid, and S3 access key / secret.  This information is available from OSiRIS COManage at https://comanage.osris.org.  Look under your User Menu at the upper right for Ceph Credentials and My Profile to determine your credentials and COU.  

Mount your buckets.  If you have not created any the tool will create one for you:

    ~/osiris-bundle/osiris-mount

When you are finished unmount:

    ~/osiris-bundle/osiris-mount -u


Optionally you can specify a bucket and have it created:
    
    ~/osiris-bundle/osiris-mount -n mycou-anyname

Buckets should be all lowercase and must be prefixed with your COU (virtual organization) or the request will be denied.  


## More information

Basic usage help for this utility is available by running 'osiris-mount -h'

More OSiRIS documentation is available from our website: http://www.osris.org/documentation/




