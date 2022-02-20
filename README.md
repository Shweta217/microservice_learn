# microservice_learn

1) download aws cli and helm and configure aws cli on putty

2) take ecr login: refer https://blog.dbi-services.com/how-to-push-an-image-into-amazon-ecr-with-docker/#:~:text=8%20Steps%20To%20Push%20An%20Image%20Into%20Amazon,the%20image%20and%20the%20repository%20from%20Amazon%20

3) create secret vault for ecr:
   ACCOUNT=aws-account-id
   REGION=ap-south-1
   SECRET_NAME=${REGION}-ecr-registry
   EMAIL=shweta.alter1@gmail.com
   TOKEN=`aws ecr get-login --region ${REGION} --registry-ids ${ACCOUNT} | cut -d' ' -f6`
   echo "ENV variables setup done."
   kubectl delete secret --ignore-not-found $SECRET_NAME 
   kubectl create secret docker-registry $SECRET_NAME \
   --docker-server=https://${ACCOUNT}.dkr.ecr.${REGION}.amazonaws.com \
   --docker-username=AWS \
   --docker-password="${TOKEN}" \
   --docker-email="${EMAIL}"
   echo "Secret created by name. $SECRET_NAME"
   kubectl patch serviceaccount default -p '{"imagePullSecrets":[{"name":"'$SECRET_NAME'"}]}' -n $NAMESPACE
   echo "All done."

4) create eks cluster: 
  eksctl create iamserviceaccount \
--cluster=test-cluster \
--region=ap-south-1 \
--namespace=kube-system \
--name=aws-load-balancer-controller \
--attach-policy-arn=arn:aws:iam::<aws-account-id>:policy/AWSLoadBalancerControllerIAMPolicy \
--override-existing-serviceaccounts \
--approve	
  
5) create IAM policies and attach to ALB: follow https://nubisoft.io/blog/how-to-set-up-kubernetes-ingress-with-aws-alb-ingress-controller/
   attach https://raw.githubusercontent.com/kubernetes-sigs/aws-load-balancer-controller/v2.2.0/docs/install/iam_policy.json policy instead of mentioned in blog

6) create certificate and attach to aws account: follow
   https://medium.com/@francisyzy/create-aws-elb-with-self-signed-ssl-cert-cd1c352331f
  
7) use code of alb.yml and react.yml to test the app on https.  
