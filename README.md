# Deploying a Websocket Server to AWS with Pulumi

`server` contains a Python websocket server that consumes from a Kafka Topic on Confluent Cloud. It also contains login/connection details, and a sample dockerfile.

`deploy` contains Pulumi settings for deploying the server to AWS.

## Running

```sh
cd deploy
pulumi stack init dev
pulumi stack select dev
pulumi config set cloud:provider aws
pulumi config set cloud-aws:useFargate true
pulumi config set aws:region eu-west-2
pulumi up
```

The `pulumi up` command will prompt for confirmation before creating resources on AWS.  When deployment is complete it will display the Websocket endpoint similar to:

```txt
Outputs:
   websocketServerUrl: "ws://545ccd01-40f9196-6433d7830c432240.elb.eu-west-2.amazonaws.com:8080"
```

Connecting to that address with a tool like `ws` will test it:

```sh
ws ws://545ccd01-40f9196-6433d7830c432240.elb.eu-west-2.amazonaws.com:8080
< {"TOTAL": 93144.08129702274}
< {"TOTAL": 93171.30908460579}
< {"TOTAL": 93204.98305774863}
< ...
```

