from subprocess import Popen, PIPE

def test_shell():
    p = Popen(['invenio', 'shell'], stdin=PIPE, stdout=PIPE, stderr=PIPE)
    output, err = p.communicate()
    assert p.returncode == 0
