#!/bin/sh

DEVICE="/media/elmarw/CIRCUITPY/"

# echo "cleaning"
# remotefiles=$(ls $DEVICE)
# for file in $remotefiles; do
#     if [ "$file" = "keyz" ]; then
#         echo "found keyz install, removing"
#         $(rm -rf $DEVICE/keyz)
#     fi
# done

# echo "installing"
cd source
echo "transfering boot.py"
$(cp boot.py $DEVICE)
echo "transfering code.py"
$(cp code.py $DEVICE)
# echo "transfering config"
# $(cp config $DEVICE)
echo "creating folders"
$(mkdir -p $DEVICE/lib)
cd lib
localfiles=$(ls)
for file in $localfiles; do
    echo "transfering lib/$file"
    $(cp $file $DEVICE/lib)
done