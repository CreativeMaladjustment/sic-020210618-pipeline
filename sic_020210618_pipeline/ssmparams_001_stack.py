from aws_cdk import core, aws_ssm as ssm

class Feature001Stack(core.Stack):
  def __init__(self, app: core.App, id: str, **kwargs):
    super().__init__(app, id, **kwargs)

    param001 = ssm.StringParameter(self, "sic_020210618_pipeline_feature001_ssm001",
        description="feature 001 requires this ssm param to be set",
        parameter_name="sic_020210618_pipeline/feature001_001",
        string_value="rabbit"
    )
    
    # param002 = ssm.StringParameter(stack, "sic_020210618_pipeline_feature001_ssm002",
    #     description="feature 002 requires this ssm param to be set",
    #     parameter_name="sic_020210618_pipeline/feature001_002",
    #     string_value="rabbits many many rabbits"
    # )