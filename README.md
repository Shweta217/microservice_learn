# microservice_learn
ecr authentication reference: https://blog.dbi-services.com/how-to-push-an-image-into-amazon-ecr-with-docker/#:~:text=8%20Steps%20To%20Push%20An%20Image%20Into%20Amazon,the%20image%20and%20the%20repository%20from%20Amazon%20

ecr authentication in k8s:
ACCOUNT=aws-account-id-digits
REGION=your-region
NAMESPACE=your-namespace 
SECRET_NAME=${REGION}-ecr-registry
EMAIL=dummy.email@email.com
TOKEN=`aws ecr get-login --region ${REGION} --registry-ids ${ACCOUNT} | cut -d' ' -f6`
echo "ENV variables setup done."
kubectl delete secret --ignore-not-found $SECRET_NAME -n $NAMESPACE
kubectl create secret docker-registry $SECRET_NAME -n $NAMESPACE \
--docker-server=https://${ACCOUNT}.dkr.ecr.${REGION}.amazonaws.com \
--docker-username=AWS \
--docker-password="${TOKEN}" \
--docker-email="${EMAIL}"
echo "Secret created by name. $SECRET_NAME"
kubectl patch serviceaccount default -p '{"imagePullSecrets":[{"name":"'$SECRET_NAME'"}]}' -n $NAMESPACE
echo "All done."

refernce: https://stackoverflow.com/questions/49654457/how-to-auto-deploy-docker-containers-from-amazon-ecr-to-kubernetes-using-jenkins
