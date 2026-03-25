from oarepo.config.base import set_constants_in_caller, get_constant_from_caller


def configure_oai():
    repo_name = get_constant_from_caller("REPOSITORY_NAME")
    if not repo_name:
        raise ValueError("REPOSITORY_NAME must be set, please configure UI before configuring OAI.")
    OAISERVER_REPOSITORY_NAME = str(repo_name)

    set_constants_in_caller(locals())