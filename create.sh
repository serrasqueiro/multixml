#!/bin/sh


usage ()
{
 echo "Usage:

	$0
"
 if [ "$*" ]; then
	echo
	echo "$*"
 fi
 exit 0
}


#
# Main script
#

[ "$MULTI_BASE" = "" ] && usage "Please define variable MULTI_BASE, example:

	export MULTI_BASE=$HOME/git_repos

...and run
	$0
"

THERE=results/country_calling_codes.json
[ -f $THERE ] && PRE="Re-"

python src/packages/multix/callingcodes.test.py $MULTI_BASE/aggregates/ggle/libphonenumber/resources/PhoneNumberMetadata.xml | grep -v ^"#" > $THERE
RES=$?

# Exit status
[ $RES = 0 ] && echo "${PRE}Generated results/country_calling_codes.json"
exit $RES
