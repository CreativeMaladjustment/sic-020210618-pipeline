#!/usr/bin/env python3

CODECOMMIT_REPO_NAME = "sic-020210618-pipeline"

from aws_cdk import core

from sic_020210618_pipeline.pipeline_stack import PipelineStack
from sic_020210618_pipeline.lambda_stack import LambdaStack
from sic_020210618_pipeline.cloud9_stack import Cloud9Stack

app = core.App()

lambda_stack = LambdaStack(app, "LambdaStack")

PipelineStack(app, "PipelineDeployingLambdaStack",
    lambda_code=lambda_stack.lambda_code,
    repo_name=CODECOMMIT_REPO_NAME)

cloud9_stack = Cloud9Stack(app, "sic020210618Cloud9")
app.synth()
