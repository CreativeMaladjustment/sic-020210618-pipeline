#https://docs.aws.amazon.com/cdk/latest/guide/codepipeline_example.html
from aws_cdk import (core, aws_codebuild as codebuild,
                     aws_codecommit as codecommit,
                     aws_codepipeline as codepipeline,
                     aws_codepipeline_actions as codepipeline_actions,
                     aws_lambda as lambda_)

class PipelineStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, *, repo_name: str=None,
                 lambda_code: lambda_.CfnParametersCode=None, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        code = codecommit.Repository.from_repository_name(self, "ImportedRepo",
                  repo_name)

        cdk_build = codebuild.PipelineProject(self, "CdkBuild",
                        build_spec=codebuild.BuildSpec.from_object(dict(
                            version="0.2",
                            phases=dict(
                                install=dict(
                                    commands=[
                                        "npm install aws-cdk",
                                        "npm update",
                                        "python -m pip install -r requirements.txt"
                                    ]),
                                build=dict(commands=[
                                    "npx cdk synth -o dist"])),
                            artifacts={
                                "base-directory": "dist",
                                "files": [
                                    "sic020210618-Lambda-pipeline.template.json","sic020210618-cloud9-pipeline.template.json","sic020210618-feature001-pipeline.template.json"]},
                            environment=dict(buildImage=
                                codebuild.LinuxBuildImage.STANDARD_2_0))))

        lambda_build = codebuild.PipelineProject(self, 'LambdaBuild',
                        build_spec=codebuild.BuildSpec.from_object(dict(
                            version="0.2",
                            phases=dict(
                                install=dict(
                                    commands=[
                                        "cd lambda",
                                        "npm install",
                                        "npm install typescript"]),
                                build=dict(
                                    commands=[
                                        "npx tsc index.ts"])),
                            artifacts={
                                "base-directory": "lambda",
                                "files": [
                                    "index.js",
                                    "node_modules/**/*"]},
                            environment=dict(buildImage=
                                codebuild.LinuxBuildImage.STANDARD_5_0))))

        source_output = codepipeline.Artifact()
        cdk_build_output = codepipeline.Artifact("CdkBuildOutput")
        lambda_build_output = codepipeline.Artifact("LambdaBuildOutput")

        lambda_location = lambda_build_output.s3_location

        codepipeline.Pipeline(self, "Pipeline",
            stages=[
                codepipeline.StageProps(stage_name="Source",
                    actions=[
                        codepipeline_actions.CodeCommitSourceAction(
                            action_name="CodeCommit_Source",
                            branch="main",
                            repository=code,
                            output=source_output)]),
                codepipeline.StageProps(stage_name="Build",
                    actions=[
                        codepipeline_actions.CodeBuildAction(
                            action_name="Lambda_Build",
                            project=lambda_build,
                            input=source_output,
                            outputs=[lambda_build_output]),
                        codepipeline_actions.CodeBuildAction(
                            action_name="CDK_Build",
                            project=cdk_build,
                            input=source_output,
                            outputs=[cdk_build_output])]),
                codepipeline.StageProps(stage_name="Deploy",
                    actions=[
                        codepipeline_actions.CloudFormationCreateUpdateStackAction(
                            action_name="Lambda_CFN_Deploy",
                            template_path=cdk_build_output.at_path(
                                "sic020210618-Lambda-pipeline.template.json"),
                            stack_name="sic020210618-Lambda-pipeline",
                            admin_permissions=True,
                            parameter_overrides=dict(
                                lambda_code.assign(
                                    bucket_name=lambda_location.bucket_name,
                                    object_key=lambda_location.object_key,
                                    object_version=lambda_location.object_version)),
                            extra_inputs=[lambda_build_output])
                            ,
                        codepipeline_actions.CloudFormationCreateUpdateStackAction(
                            action_name="Cloud9_CFN_Deploy",
                            template_path=cdk_build_output.at_path(
                                "sic020210618-cloud9-pipeline.template.json"),
                            stack_name="sic020210618-cloud9-pipeline",
                            admin_permissions=True)
                            ,
                        codepipeline_actions.CloudFormationCreateUpdateStackAction(
                            action_name="Feature001_CFN_Deploy",
                            template_path=cdk_build_output.at_path(
                                "sic020210618-feature001-pipeline.template.json"),
                            stack_name="sic020210618-feature001-pipeline",
                            admin_permissions=True)
                        #     ,
                        # codepipeline_actions.CloudFormationCreateUpdateStackAction(
                        #     action_name="vpcforcloud9_CFN_Deploy",
                        #     template_path="/cloudformationtemplates/vpc-for-cloud9-privatesubnetpoc.yml",
                        #     stack_name="sic020210618-vpcforcloud9-pipeline",
                        #     admin_permissions=True)
                    ])
                ]
            )
