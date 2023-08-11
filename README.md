# jaeger-databricks-inference

## background

Logs can help diagnose specific issues, but they are sometimes unintuitive when operating multiple systems.

Metrics can be useful to identify trends, but aren't as useful when looking for specifics.

Traces are a newer, third option, which give us the ability to get request-specific information, even across systems. It is often difficult to find bottlenecks when operating latency-sensitive systems. It is extremely difficult for humans to find bottlenecks with multi-application systems. This is where tracing can be helpful.

## this repo

This repository contains an demo of Jaeger tracing, including:

- *jaeger.sh* - a shell script that installs a local Jaeger server
- *inference.py* - a barebones implementation of a PyFunc model, including steps for preprocessing and inference. this script sends 100 requests to an endpoint defined in `main.py`. 
- *main.py* - a simple webserver that hosts an endpoint /endpoint. just used as an example of cross-system/cross-application tracing
