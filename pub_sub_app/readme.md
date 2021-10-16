# simple application in flask to demostrate pubsub message processing (listenr/consumer)

Application DIR

    main.py := flask application file

    config.py := configuration infomation for GCP Project,Pubsub

    cloudbuild.yaml := cloud build triggers for application CI/CD

    requirements.txt := required packages 

    Dockerfile := for containerized application


Steps:

1) Create Pubsub topic in GCP project
2) Create subscription with push endpoint ( update it with cloud run url + "/msg_process")
3) Give Pubsub subscription service account cloud invoker role
4) Publish message at GCP topic (cloud console) and see cloud run log for result
5) Or use '/msg_send' route to publish the message
