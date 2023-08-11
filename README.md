# databricks-model-serving-jaeger

## background

Logs can help diagnose specific issues, but they are sometimes unintuitive when operating multiple systems.

Metrics can be useful to identify trends, but aren't as useful when looking for specifics.

Traces are a newer, third option, which give us the ability to get request-specific information, even across systems. It is often difficult to find bottlenecks when operating latency-sensitive systems. It is extremely difficult for humans to find bottlenecks with multi-application systems. This is where tracing can be helpful.

## this repo

This repository contains an demo of Jaeger tracing, including:

- *jaeger.sh* - a shell script that installs a local Jaeger server
- *inference.py* - a barebones implementation of a PyFunc model, including steps for preprocessing and inference. this script sends 100 requests to an endpoint defined in `main.py`. 
- *main.py* - a simple webserver that hosts an endpoint /endpoint. just used as an example of cross-system/cross-application tracing

## runbook
(*nix commands given)
1) create a virtual environment and install the requirements - `virtualenv venv && source venv/bin/activate && pip install -r requirements.txt`
2) run jaeger.sh - `./jaeger.sh` - you may need to adjust the URL given according to your system architecture/operating system, see https://www.jaegertracing.io/download/
3) run main.sh - `python main.sh`
4) finally, run inference.py - `python main.sh`
5) open the jaeger UI and see your traces at `https://localhost:16686/`