#!/bin/bash

# \ ]* # use this RegEx to remove the query tags
# ./start.sh SPOTIFY LINKS HERE
 export SONGS=$(./stripParams $@)
 echo $SONGS
 echo $SONGS >> $(pwd)/downloaded.txt
 ./start.sh $SONGS