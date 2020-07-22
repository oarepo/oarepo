from subprocess import Popen, PIPE


def test_entrypoints():
    p = Popen(['invenio', 'instance', 'entrypoints'], stdin=PIPE, stdout=PIPE, stderr=PIPE)
    output, err = p.communicate()
    assert b'invenio_app = invenio_app:InvenioApp' in output
    assert p.returncode == 0
