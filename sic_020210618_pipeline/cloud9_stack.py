from aws_cdk import core, aws_cloud9 as cloud9, aws_ec2 as ec2, aws_codecommit as codecommit

class Cloud9Stack(core.Stack):
  def __init__(self, app: core.App, id: str, **kwargs):
    super().__init__(app, id, **kwargs)

    vpc = ec2.Vpc(self, "sic020210618-vpc", max_azs=3)

    repo_existing = codecommit.Repository.from_repository_name(self, "RepoExisting", "sic-020210618-pipeline")

    #c9ec2 = cloud9.CfnEnvironmentEC2(self, "sic020210618-envec2-pipeline", owner_arn="arn:aws:iam::324320755747:user/jason.davis.labs", name="sic020210618-envec2", instance_type="t2.medium", repositories=[cloud9.CloneRepository.from_code_commit(repo_existing, "/git/sic-020210618-pipeline")])

    c9env = cloud9.Ec2Environment(self, "sic020210618-ec2-pipeline", vpc=vpc,
        cloned_repositories=[cloud9.CloneRepository.from_code_commit(repo_existing, "/git/sic-020210618-pipeline")]
        )

    core.CfnOutput(self, "URL", value=c9env.ide_url)
