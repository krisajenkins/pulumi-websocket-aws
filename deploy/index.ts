import * as cloud from "@pulumi/cloud";
import { interpolate } from "@pulumi/pulumi";

let service = new cloud.Service("pulumi-service", {
    containers: {
        websocketConsumer: {
            build: "../server",
            memory: 128,
            ports: [{ port: 8080 }],
        },
    }
});

exports.websocketServerUrl = interpolate`ws://${service.defaultEndpoint.hostname}:8080`
