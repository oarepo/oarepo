from subprocess import Popen, PIPE
import re
import packaging.version

VER = 'INVENIO_VERSION ='


def test_shell():
    # get invenio version from setup.py
    with open('setup.py', 'r') as f:
        setup_invenio_version = [x for x in f.readlines() if x.startswith(VER)][0]
    setup_invenio_version = setup_invenio_version[len(VER):].strip().strip('"').strip("'")
    setup_invenio_version = packaging.version.parse(setup_invenio_version)

    # try to run invenio shell and print invenio version from there
    p = Popen(['invenio', 'shell'], stdin=PIPE, stdout=PIPE, stderr=PIPE)
    output, err = p.communicate(
        b'from invenio import version; print ("Invenio version:", version.__version__)')
    assert p.returncode == 0

    output = [x.strip() for x in output.decode('utf-8').split('\n') if "Invenio version: " in x][0]
    installed_invenio_version = re.sub('.*Invenio version: ', '', output)
    installed_invenio_version = packaging.version.parse(installed_invenio_version)

    # assert that installed version is >= setup version
    assert installed_invenio_version >= setup_invenio_version

    # get next version not covered in setup
    next_invenio_setup_version = setup_invenio_version.base_version.split('.')
    next_invenio_setup_version[-1] = str(int(next_invenio_setup_version[-1]) + 1)
    next_invenio_setup_version = packaging.version.parse('.'.join(next_invenio_setup_version))

    # and assert that installed version is < than the next invenio release version
    # if not, we should create a new oarepo library
    assert next_invenio_setup_version > installed_invenio_version
