#!/usr/bin/env python3

CODECOMMIT_REPO_NAME = "sic-020210618-pipeline"

from aws_cdk import core
from aws_cdk.core import Stack, Tags

from sic_020210618_pipeline.pipeline_stack import PipelineStack
from sic_020210618_pipeline.lambda_stack import LambdaStack
from sic_020210618_pipeline.cloud9_stack import Cloud9Stack

def tag_stack(stack: Stack, tags: dict):
    for key, value in tags.items():
        Tags.of(stack).add(key, value)

standard_tags={}        
standard_tags["owneremail"]="jason.davis@stelligent.com"
standard_tags["project"]="sic020210618"
        
app = core.App()

lambda_stack = LambdaStack(app, "sic020210618-Lambda-pipeline")
tag_stack(lambda_stack, standard_tags)

cloud9_stack = LambdaStack(app, "sic020210618-cloud9-pipeline")
tag_stack(cloud9_stack, standard_tags)

pipeline_stack = PipelineStack(app, "sic020210618-pipeline", lambda_code=lambda_stack.lambda_code, repo_name=CODECOMMIT_REPO_NAME)
tag_stack(pipeline_stack, standard_tags)

app.synth()
