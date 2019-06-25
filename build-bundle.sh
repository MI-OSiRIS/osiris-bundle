#!/bin/bash

# builds osiris client bundle
# builds an s3fs appimage from scratch, including download of app image tools
# downloads and installs awscli

WD=`pwd`

AI="linuxdeploy-x86_64.AppImage"
AIP="linuxdeploy-plugin-appimage-x86_64.AppImage"

GITREPO="https://github.com/linuxdeploy"

AIDL="$GITREPO/linuxdeploy/releases/download/continuous/$AI"
AIPDL="$GITREPO/linuxdeploy-plugin-appimage/releases/download/continuous/$AIP"

# check for and download appimage linuxdeploy tools
if [ ! -f $AI ]; then
	wget $AIDL && chmod +x $AI
fi

if [ ! -f $AIP ]; then
	wget $AIPDL && chmod +x $AIP
fi

# clone repo if not already
if [ ! -d s3fs-fuse ]; then
	# clone s3fs-fuse
	git clone https://github.com/s3fs-fuse/s3fs-fuse.git
fi

cd s3fs-fuse

# clean up if this isn't a fresh clone
rm -rf AppDir 2> /dev/null
mkdir AppDir

PRE=`pwd`

./autogen.sh

./configure --prefix=$PRE/AppDir
make
make install

if [ $? -ne 0 ]; then
	echo "Build failed, exiting"
	exit 1
fi

cd $WD

./linuxdeploy-x86_64.AppImage \
--create-desktop-file \
--icon-file=s3fs-fuse/doc/s3fs.png \
--executable=s3fs-fuse/AppDir/bin/s3fs \
--appdir s3fs-fuse/AppDir  \
--output=appimage

if [ $? -eq 0 ]; then
	mkdir osiris-bundle
	# image will be built with git commit hash in name if done inside git repo 
	mv s3fs-*.AppImage osiris-bundle/s3fs
fi

mv README.md osiris-bundle/README

# copy our other tools into bundle directory
/bin/cp -f \
detect-endpoint.py \
osiris-mount \
osiris-setup.dist \
osiris-bundle/

tar -czf osiris-bundle.tgz osiris-bundle/
