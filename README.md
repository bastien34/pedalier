# RDT Pedalier

LibreOffice extension to provide VLC controls by foot pedals.

Works on Linux.

Dependencies
------------
    sudo apt install lib-gtk-3-0-dev
    pip install attrdict
    pip install wxPython (building wheel might take a while)
    pip install evdev
    pip install configobj

Udev rules & user group
-----------------------

Run the script `./install.sh` to create new rules for the foot device
switcher to be usable.

Be sure the user belongs to `plugdev` group.

     sudo adduser username plugdev


Extension development
---------------------

Extension development is done using the `lo-extension-dev` package 
which can be installed by pip.

    pip install lo-extension-dev

https://pypi.org/project/lo-extension-dev/
