set -o allexport
source .env.prod set #change
+o allexport

AWS_PROFILE=default terraform apply

#echo "Do you wish to install this program?"
#select yn in "Yes" "No"; do
#    case $yn in
#        Yes ) AWS_PROFILE=default terraform apply; break;;
#        No ) exit;;
#    esac
#done
