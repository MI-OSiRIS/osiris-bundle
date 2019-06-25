# osiris-bundle
OSiRIS client bundle for s3fs mounting

## Description

This bundle is designed to simplify configuration and usage of s3fuse to mount OSiRIS S3 buckets.  It is targeted both at interactive and non-interactive use in batch jobs.  

It includes an endpoint auto-detection component to determine which OSiRIS S3 endpoint is reachable by your host.  For example, from campus computing clusters at our member institutions you will generally only be able to reach the endpoint local to your campus.  From more general purpose machines you may be able to reach all of the OSiRIS S3 endpoints.  

A setup tool is also included to configure your S3 credentials.  

The default behaviour is to list all of your S3 buckets and mount each one under /tmp/${USER}-fuse/bucketname.  You can also specify buckets to mount and create them if necessary.  

## Usage

Usage of the client bundle for batch compute jobs assumes you have a consistent $HOME directory and can run the configure script first on a login interactive node.  Once the configuration script is run the osiris-mount utility does not require interaction to mount your buckets.  You can run the configuration script multiple times to change or add new credentials.  The credentials used are determined by the AWSPROFILE setting in osiris-bundle/osiris-config.  This setting can also be specified with the -p option to osiris-mount.  

    Usage: osiris-mount [ -u ] [ -n ] [ -R region ] [ -P <COU> ] [ -O '<options>' ] [ bucket1 ] [ bucket2 ] [ ... ]

        <bucket> is an S3 bucket to mount, if not specified mount all S3 buckets owned by user
        
        -n will create the bucket(s) specified on command line before mounting
        
        -P <COU> will place new buckets into COU.  Case sensitive, must match a COU you belong to.  
            * Only relevant if you belong to multiple OSiRIS COU / Virtual Org
            * You can also set default placement for all new buckets in OSiRIS COmanage
            * Not possible to modify placement of existing buckets

        -u will umount and remove tmp directories (calls fusermount -u on each mountpoint)
        
        -O to specify quoted list of additional options to s3fs mount. 
            * Example (enable debugging output): '-o curldbg -d -d -f' 
        
        -R <region> [,region ] [ ... ] will limit connection to regions in order specified.  
            * Comma separate multiple values (no spaces).  Options:  all,um,msu,wsu,vai
            * Tool will auto-detect reachable OSiRIS regions only from the list specified 
            * Default is equivalent to 'all'

    All flags and positional arguments are optional.

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




