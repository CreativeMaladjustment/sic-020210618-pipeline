#!/usr/bin/env python3

CODECOMMIT_REPO_NAME = "sic-020210618-pipeline"

from aws_cdk import core

from sic_020210618_pipeline.pipeline_stack import PipelineStack
from sic_020210618_pipeline.lambda_stack import LambdaStack

app = core.App()

lambda_stack = LambdaStack(app, "LambdaStack")

PipelineStack(app, "PipelineDeployingLambdaStack",
    lambda_code=lambda_stack.lambda_code,
    repo_name=CODECOMMIT_REPO_NAME)

app.synth()
